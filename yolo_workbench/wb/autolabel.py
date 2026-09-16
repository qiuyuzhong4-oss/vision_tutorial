# -*- coding: utf-8 -*-
"""半自动标注(伪标签)模块:种子集检查 → 快速训练 → 推理生成伪标签 → 审核状态管理 → 导出。

训练放在子进程跑(见 train_runner.py),避免卡死 Streamlit;
推理在当前进程流式跑,便于展示进度。
"""
from __future__ import annotations

import glob
import json
import os
import shutil

import cv2
import numpy as np
import yaml

IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


# ---------------------------------------------------------------- 种子集检查
def list_images(folder: str) -> list[str]:
    if not folder or not os.path.isdir(folder):
        return []
    out = []
    for ext in IMG_EXTS:
        out += glob.glob(os.path.join(folder, f"*{ext}"))
        out += glob.glob(os.path.join(folder, f"*{ext.upper()}"))
    return sorted(set(out))


def label_path_for(img_path: str, label_dir: str) -> str:
    base = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
    return os.path.join(label_dir, base)


def scan_seed(img_dir: str, label_dir: str) -> dict:
    """统计种子集:图片数、有标签数、类别直方图、尺寸分布简况。"""
    imgs = list_images(img_dir)
    n_labeled, class_hist, sizes = 0, {}, []
    for p in imgs:
        lp = label_path_for(p, label_dir)
        if not os.path.isfile(lp):
            continue
        n_labeled += 1
        with open(lp) as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 5:
                    c = int(float(parts[0]))
                    class_hist[c] = class_hist.get(c, 0) + 1
                    w, h = float(parts[3]), float(parts[4])
                    sizes.append(min(w, h))  # 短边占比,粗略衡量目标大小
    return {
        "n_images": len(imgs),
        "n_labeled": n_labeled,
        "n_missing": len(imgs) - n_labeled,
        "class_hist": class_hist,
        "small_ratio": float(np.mean([s < 0.03 for s in sizes])) if sizes else 0.0,  # <3% 视为小目标
    }


def parse_class_names(text: str) -> list[str]:
    """'red,blue' 或 '0:red,1:blue' → ['red','blue']。"""
    names = []
    for tok in text.replace(",", ",").replace(",", ",").split(","):
        tok = tok.strip()
        if not tok:
            continue
        if ":" in tok:
            tok = tok.split(":", 1)[1].strip()
        names.append(tok)
    return names


def build_data_yaml(img_dir: str, label_dir: str, names: list[str], out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cfg = {
        "path": os.path.abspath(os.path.dirname(img_dir) or "."),
        "train": os.path.abspath(img_dir),
        "val": os.path.abspath(img_dir),  # 快速训练用种子集自验证,足够出可用检测器
        "names": {i: n for i, n in enumerate(names)},
    }
    with open(out_path, "w") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True)
    return out_path


# ---------------------------------------------------------------- 快速训练(子进程)
def find_latest_weights(project_dir: str) -> str | None:
    cands = sorted(glob.glob(os.path.join(project_dir, "*", "weights", "best.pt")),
                   key=os.path.getmtime)
    return cands[-1] if cands else None


# ---------------------------------------------------------------- 伪标签生成
def generate_pseudo_labels(weights: str, img_dir: str, work_dir: str, conf: float,
                           imgsz: int = 640, device: str = "",
                           progress=None) -> dict:
    """推理生成伪标签 + 审核状态文件。返回审核 state(同时存盘)。"""
    from ultralytics import YOLO

    os.makedirs(work_dir, exist_ok=True)
    model = YOLO(weights)
    imgs = list_images(img_dir)
    state = {
        "img_dir": os.path.abspath(img_dir),
        "weights": weights,
        "conf": conf,
        "names": model.names,
        "items": {},
    }
    for i, p in enumerate(imgs):
        result = model.predict(source=p, conf=conf, imgsz=imgsz, device=device or None, verbose=False)[0]
        boxes = []
        xywhn = result.boxes.xywhn.cpu().numpy() if result.boxes is not None else np.zeros((0, 4))
        cls = result.boxes.cls.cpu().numpy().astype(int) if result.boxes is not None else np.zeros(0, int)
        conff = result.boxes.conf.cpu().numpy() if result.boxes is not None else np.zeros(0)
        for (cx, cy, w, h), c, cf in zip(xywhn, cls, conff):
            boxes.append({"cls": int(c), "conf": round(float(cf), 3),
                          "xywhn": [round(float(v), 6) for v in (cx, cy, w, h)], "keep": True})
        state["items"][os.path.basename(p)] = {"path": p, "status": "pending", "boxes": boxes}
        if progress:
            progress((i + 1) / max(len(imgs), 1))
    state_path = os.path.join(work_dir, "review_state.json")
    with open(state_path, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    return state


def load_review_state(work_dir: str) -> dict | None:
    p = os.path.join(work_dir, "review_state.json")
    if not os.path.isfile(p):
        return None
    with open(p) as f:
        return json.load(f)


def save_review_state(state: dict, work_dir: str) -> None:
    with open(os.path.join(work_dir, "review_state.json"), "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- 审核辅助
def draw_review(img_bgr: np.ndarray, boxes: list[dict], names: list) -> np.ndarray:
    """按 keep 状态画伪标签框:保留=类别色实线,删除=灰色虚线感(细线)。"""
    from .preview import PALETTE
    img = img_bgr.copy()
    for b in boxes:
        cx, cy, w, h = b["xywhn"]
        H, W = img.shape[:2]
        x1, y1 = int((cx - w / 2) * W), int((cy - h / 2) * H)
        x2, y2 = int((cx + w / 2) * W), int((cy + h / 2) * H)
        color = PALETTE[b["cls"] % len(PALETTE)] if b["keep"] else (120, 120, 120)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2 if b["keep"] else 1)
        label = f'{names[b["cls"]] if b["cls"] < len(names) else b["cls"]} {b["conf"]:.2f}'
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        y_text = max(y1 - 6, th + 2)
        cv2.rectangle(img, (x1, y_text - th - 4), (x1 + tw + 4, y_text + 2), color, -1)
        cv2.putText(img, label, (x1 + 2, y_text - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# ---------------------------------------------------------------- 导出
def export_approved(state: dict, out_root: str) -> dict:
    """审核通过的图 + 保留框 → 标准 YOLO 数据集结构,并生成 data.yaml。"""
    img_out = os.path.join(out_root, "images", "train")
    lbl_out = os.path.join(out_root, "labels", "train")
    os.makedirs(img_out, exist_ok=True)
    os.makedirs(lbl_out, exist_ok=True)

    names = state.get("names") or []
    if isinstance(names, dict):
        names = [names[k] for k in sorted(names, key=int)]
    n_img = n_box = 0
    for item in state["items"].values():
        if item["status"] != "approved":
            continue
        kept = [b for b in item["boxes"] if b.get("keep")]
        if not kept:
            continue
        shutil.copy2(item["path"], os.path.join(img_out, os.path.basename(item["path"])))
        with open(os.path.join(lbl_out, os.path.splitext(os.path.basename(item["path"]))[0] + ".txt"), "w") as f:
            for b in kept:
                cx, cy, w, h = b["xywhn"]
                f.write(f'{b["cls"]} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n')
        n_img += 1
        n_box += len(kept)

    with open(os.path.join(out_root, "data.yaml"), "w") as f:
        yaml.safe_dump({
            "path": os.path.abspath(out_root),
            "train": os.path.abspath(img_out),
            "val": os.path.abspath(img_out),
            "names": {i: n for i, n in enumerate(names)},
        }, f, allow_unicode=True)
    return {"images": n_img, "boxes": n_box, "root": out_root}
