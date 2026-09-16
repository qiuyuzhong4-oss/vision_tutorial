# -*- coding: utf-8 -*-
"""配置导出:生成可直接使用的训练命令、hyp YAML、预设 JSON。

导出原则:只写与官方默认不同的增强参数(显式、简洁);
data/model/epochs 等留占位符,由用户在命令里替换。
"""
from __future__ import annotations

import json

from .params import PARAM_SPECS, build_hyp

# 官方默认值(与 default.yaml 对齐),用于判断"非默认才导出"
OFFICIAL_DEFAULTS = {
    k: spec[2] for k, spec in PARAM_SPECS.items()
}


def build_train_command(values: dict, imgsz: int, data: str = "your_data.yaml",
                        model: str = "yolo11n.pt", epochs: int = 100) -> str:
    """生成 yolo detect train 命令,只包含非默认增强参数。"""
    parts = [
        "yolo detect train",
        f"data={data}",
        f"model={model}",
        f"epochs={epochs}",
        f"imgsz={imgsz}",
    ]
    for key, value in values.items():
        if key not in OFFICIAL_DEFAULTS:
            continue
        if abs(float(value) - float(OFFICIAL_DEFAULTS[key])) > 1e-9:
            parts.append(f"{key}={value}")
    return " \\\n      ".join(parts)


def build_hyp_yaml(values: dict, imgsz: int) -> str:
    """生成 hyp 覆盖文件(可通过 cfg=hyp.yaml 方式使用)。"""
    lines = [f"# YOLO 增强工作台导出 | imgsz={imgsz}", "# 用法: yolo detect train cfg=this.yaml data=... model=..."]
    for key, value in values.items():
        if key in OFFICIAL_DEFAULTS:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def build_preset_json(values: dict, imgsz: int, name: str = "my_preset") -> str:
    """把当前滑块状态存为可复用的预设 JSON。"""
    payload = {
        "name": name,
        "imgsz": imgsz,
        "values": {k: v for k, v in values.items() if k in PARAM_SPECS},
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def load_preset_json(text: str) -> dict:
    """读取预设 JSON,容错:返回 {'name','imgsz','values'}。"""
    payload = json.loads(text)
    values = {k: v for k, v in payload.get("values", {}).items() if k in PARAM_SPECS}
    return {
        "name": payload.get("name", "imported"),
        "imgsz": int(payload.get("imgsz", 640)),
        "values": values,
    }
