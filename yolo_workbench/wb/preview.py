# -*- coding: utf-8 -*-
"""预览管道:直接调用官方 v8_transforms,保证预览与训练完全一致。

两种预览模式:
- 单图增强:把 mosaic/mixup/cutmix/copy_paste 概率置 0,只看 HSV/几何/翻转
  对这张图(和它的框)做了什么,便于理解每个参数。
- 完整训练管道:与训练完全相同的管道(含 mosaic 等),看真实训练分布。

随机性控制:每次渲染前固定 random/numpy 种子,同一 seed 下拖动滑块
结果可对照;点击"换个随机"换 seed。
"""
from __future__ import annotations

import random

import cv2
import numpy as np

from ultralytics.data.augment import v8_transforms
from ultralytics.utils import IterableSimpleNamespace

from .dataset import PreviewDataset, Sample
from .params import build_hyp

# 画框配色(按类别序号循环)
PALETTE = [
    (85, 67, 232), (48, 201, 60), (36, 168, 232), (60, 76, 231),
    (196, 72, 60), (164, 78, 181), (112, 84, 172), (0, 168, 138),
]


def draw_boxes(img_bgr: np.ndarray, boxes_xyxy, classes, class_names=None) -> np.ndarray:
    """在 BGR 图上画 xyxy 像素框,返回副本(RGB)。"""
    img = img_bgr.copy()
    for (x1, y1, x2, y2), c in zip(np.asarray(boxes_xyxy).reshape(-1, 4), np.asarray(classes).reshape(-1)):
        x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
        c = int(c)
        color = PALETTE[c % len(PALETTE)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = class_names[c] if class_names and c < len(class_names) else str(c)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        y_text = max(y1 - 6, th + 2)
        cv2.rectangle(img, (x1, y_text - th - 4), (x1 + tw + 4, y_text + 2), color, -1)
        cv2.putText(img, label, (x1 + 2, y_text - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


MIX_KEYS = ("mosaic", "mixup", "cutmix", "copy_paste")


def run_pipeline(samples: list[Sample], values: dict, imgsz: int, seed: int,
                 enable_mix: bool = True) -> list[dict]:
    """对每个 sample 跑一遍官方增强管道。

    返回 list of {"name", "img_rgb"(画框后), "n_boxes", "boxes", "cls"}。
    """
    if not samples:
        return []
    hyp = build_hyp(values)
    if not enable_mix:
        for k in MIX_KEYS:
            hyp[k] = 0.0

    dataset = PreviewDataset(samples, imgsz)
    transforms = v8_transforms(
        dataset, imgsz=imgsz, hyp=IterableSimpleNamespace(**hyp)
    )

    random.seed(seed)
    np.random.seed(seed % (2**32))

    results = []
    for i in range(len(samples)):
        labels = dataset.get_image_and_label(i)
        out = transforms(labels)
        inst = out["instances"]
        # RandomPerspective 结束时 instances 为 xywh 像素格式,统一转 xyxy 再画框
        inst.convert_bbox(format="xyxy")
        boxes = inst.bboxes
        cls = out["cls"].reshape(-1).tolist() if out["cls"] is not None else []
        results.append({
            "name": samples[i].name,
            "img_rgb": None,  # 由调用方按需画框(原图不画)
            "aug_rgb": draw_boxes(out["img"], boxes, cls, None),
            "boxes": np.asarray(boxes).reshape(-1, 4),
            "cls": cls,
        })
    return results


def variants(samples: list[Sample], values: dict, imgsz: int, seed: int, n: int,
             enable_mix: bool = True) -> list[list[dict]]:
    """对同一批图连续跑 n 遍(不同随机),用于批量网格预览。"""
    all_results = []
    for v in range(n):
        all_results.append(run_pipeline(samples, values, imgsz, seed + v * 101, enable_mix))
    return all_results
