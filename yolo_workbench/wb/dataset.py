# -*- coding: utf-8 -*-
"""内存版 dataset 适配器:把用户上传的图片+标签包装成 ultralytics
v8_transforms() 所需的 dataset 接口,使预览与真实训练走同一条增强管道。

官方管道对 dataset 的要求(ultralytics 8.4.x):
- __len__
- cache 属性(设为 "ram" 可跳过 Mosaic 的 buffer 逻辑)
- data 字典(v8_transforms 读 data["flip_idx"])
- use_keypoints 属性
- get_image_and_label(i) -> labels dict,格式仿照 YOLODataset:
    img:           HWC uint8 BGR(load_image 已按 imgsz 缩放长边)
    ori_shape:     (h, w) 原图
    resized_shape: (h, w) 缩放后
    ratio_pad:     (r, r)
    instances:     Instances,归一化 xyxy(normalized=True,与训练流一致,
                   LetterBox/Mosaic 内部会自行 denormalize)
    cls:           (n,1) tensor
"""
from __future__ import annotations

import cv2
import numpy as np
import torch

from ultralytics.utils.instance import Instances


def parse_yolo_label(text: str):
    """解析 YOLO 格式标签文本 'cls cx cy w h'(每行一框,归一化坐标)。

    返回 (cls ndarray(n,), xyxy 归一化 ndarray(n,4));空/坏行跳过。
    """
    cls_list, boxes = [], []
    for line in text.strip().splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        try:
            c, cx, cy, w, h = (float(x) for x in parts[:5])
        except ValueError:
            continue
        cls_list.append(int(c))
        boxes.append([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])  # xyxy
    return np.asarray(cls_list, dtype=np.float32), np.asarray(boxes, dtype=np.float32).reshape(-1, 4)


class Sample:
    """一张上传的样例:原图(BGR)+ 归一化 xyxy 框 + 类别。"""

    def __init__(self, name: str, img_bgr: np.ndarray, cls: np.ndarray, bboxes_norm_xyxy: np.ndarray):
        self.name = name
        self.img = img_bgr
        self.cls = cls
        self.bboxes = bboxes_norm_xyxy


class PreviewDataset:
    """把 Sample 列表适配成官方 v8_transforms 可用的 dataset。"""

    def __init__(self, samples: list[Sample], imgsz: int):
        self.samples = samples
        self.imgsz = imgsz
        # Mosaic.__init__ 读取 self.dataset.cache;"ram" 使其走随机取样路径
        self.cache = "ram"
        # v8_transforms 读取 dataset.data["flip_idx"]
        self.data = {"flip_idx": [], "channels": 3, "nc": 0}
        self.use_keypoints = False
        self.use_segments = False
        self.use_obb = False

    def __len__(self):
        return len(self.samples)

    def _load_image(self, sample: Sample) -> tuple[np.ndarray, tuple, tuple]:
        """仿 BaseDataset.load_image:长边缩到 imgsz,augment 下用线性插值。"""
        im = sample.img
        s0, s1 = im.shape[:2]
        r = self.imgsz / max(s0, s1)
        if r != 1:
            im = cv2.resize(im, (int(s1 * r), int(s0 * r)), interpolation=cv2.INTER_LINEAR)
        return im, (s0, s1), im.shape[:2]

    def get_image_and_label(self, index: int) -> dict:
        sample = self.samples[index]
        img, ori_shape, resized_shape = self._load_image(sample)
        # 每次返回全新 Instances(官方实现用 deepcopy,变换会原地修改坐标)
        # segments 须为空数组而非 None:真实流程 update_labels_info 如此,
        # CopyPaste 会对 labels["instances"].segments 直接 len()
        instances = Instances(
            bboxes=sample.bboxes.copy(),
            segments=np.zeros((0, 1000, 2), dtype=np.float32),
            bbox_format="xyxy",
            normalized=True,
        )
        return {
            "img": img,
            "ori_shape": ori_shape,
            "resized_shape": resized_shape,
            "ratio_pad": (resized_shape[0] / ori_shape[0], resized_shape[1] / ori_shape[1]),
            "instances": instances,
            "cls": torch.as_tensor(sample.cls, dtype=torch.float32).reshape(-1, 1),
            "im_file": sample.name,
        }
