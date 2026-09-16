# -*- coding: utf-8 -*-
"""场景预设:一键切换一组增强参数 + 建议 imgsz。

预设只覆盖与默认不同的关键项,未覆盖的项保持 ultralytics 官方默认。
"""

# 每个预设: name -> (参数覆盖, 建议imgsz, 设计说明)
PRESETS = {
    "RoboMaster 装甲板(小目标+光照多变)": {
        "values": {
            # 光照多变:加大明度抖动,模拟场地灯光、曝光变化、逆光
            "hsv_v": 0.6,
            "hsv_s": 0.7,
            # 颜色是红/蓝装甲板的类别依据,色调抖动必须压小防混淆
            "hsv_h": 0.01,
            # 装甲板随机器人运动出现在各种平面朝向
            "degrees": 10.0,
            "translate": 0.15,
            # 缩放抖动拉满,模拟远距离小目标(场上最远约 10m+)
            "scale": 0.9,
            # 轻微透视,模拟相机与装甲板不垂直
            "perspective": 0.0005,
            "fliplr": 0.5,
            # 小目标核心增强:mosaic 保持开启
            "mosaic": 1.0,
            "mixup": 0.1,
            "close_mosaic": 10,
        },
        "imgsz": 640,
        "note": "为 RoboMaster 装甲板检测定制:hsv_v=0.6 应对场地灯光多变;"
                "scale=0.9 + mosaic=1.0 强化远距离小目标;degrees=10 覆盖各朝向;"
                "hsv_h 压到 0.01 防止红蓝颜色偏移造成类别混淆。"
                "显存允许时可把 imgsz 提到 1280,小目标收益明显。",
    },
    "远距离小目标(通用)": {
        "values": {
            "scale": 0.9,
            "mosaic": 1.0,
            "degrees": 5.0,
            "translate": 0.15,
            "hsv_v": 0.5,
            "close_mosaic": 10,
        },
        "imgsz": 1280,
        "note": "最大化模拟远距离:scale 抖动拉满 + 高分辨率训练。"
                "注意 imgsz=1280 显存和训练时间约为 640 的 4 倍。",
    },
    "夜间 / 低光照": {
        "values": {
            "hsv_v": 0.8,
            "hsv_s": 0.6,
            "degrees": 5.0,
            "scale": 0.6,
            "mosaic": 1.0,
            "mixup": 0.1,
        },
        "imgsz": 640,
        "note": "大明度抖动模拟夜间/逆光/曝光剧烈变化。"
                "若实测夜间掉点严重,应优先补充真实夜间数据。",
    },
    "官方默认(通用)": {
        "values": {},
        "imgsz": 640,
        "note": "ultralytics 官方默认参数,不做任何修改,可作为对照组。",
    },
}

DEFAULT_PRESET_NAME = "RoboMaster 装甲板(小目标+光照多变)"


# ---------------------------------------------------------------- 长期积累:用户预设库
# 场景→算法的长期积累:每个场景一个 JSON 放进 presets_user/,启动时自动并入预设列表。
# 格式与工作台导出的"当前预设 JSON"完全一致,可以从工作台导出后微调再放回来:
#   {"name": "夜间哨兵", "imgsz": 640, "values": {"hsv_v": 0.8, ...}, "note": "可选说明"}
import glob
import json
import os as _os

USER_PRESET_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "presets_user")


def load_user_presets() -> dict:
    """读取 presets_user/*.json,坏文件跳过不崩溃。"""
    out = {}
    if not _os.path.isdir(USER_PRESET_DIR):
        return out
    for p in sorted(glob.glob(_os.path.join(USER_PRESET_DIR, "*.json"))):
        try:
            with open(p) as f:
                payload = json.load(f)
            name = payload.get("name") or _os.path.splitext(_os.path.basename(p))[0]
            out[name] = {
                "values": {k: v for k, v in payload.get("values", {}).items()
                           if k in ("hsv_h", "hsv_s", "hsv_v", "degrees", "translate",
                                    "scale", "shear", "perspective", "fliplr", "flipud",
                                    "mosaic", "mixup", "cutmix", "copy_paste",
                                    "close_mosaic", "erasing")},
                "imgsz": int(payload.get("imgsz", 640)),
                "note": payload.get("note", f"(用户预设库 { _os.path.basename(p) })"),
            }
        except Exception:
            continue
    return out


def all_presets() -> dict:
    """内置预设 + 用户预设库(用户在后,重名时用户覆盖内置)。"""
    merged = dict(PRESETS)
    merged.update(load_user_presets())
    return merged
