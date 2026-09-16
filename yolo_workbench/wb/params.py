# -*- coding: utf-8 -*-
"""增强参数注册表:定义每个参数的滑块范围、默认值与中文说明。

默认值与 ultralytics/default.yaml 保持一致,保证"重置"后即官方默认。
"""

# 每个参数: key -> (min, max, default, step, 中文名, 说明)
# 说明中包含推荐范围,便于用户直接照着调
PARAM_SPECS = {
    # ---- 颜色类(模拟光照变化) ----
    "hsv_h": (0.0, 0.1, 0.015, 0.001, "hsv_h 色调偏移",
              "色调随机偏移幅度。RoboMaster 红蓝装甲板靠颜色区分,此项不要调大(≤0.01),"
              "否则红蓝可能互相偏移导致类别混淆。默认 0.015"),
    "hsv_s": (0.0, 0.9, 0.7, 0.05, "hsv_s 饱和度变化",
              "饱和度随机变化幅度。模拟现场灯光色温变化、色彩衰减。默认 0.7"),
    "hsv_v": (0.0, 1.0, 0.4, 0.05, "hsv_v 明度/曝光变化",
              "明度随机变化幅度,模拟曝光变化、灯光忽明忽暗、逆光。"
              "RoboMaster 场地灯光复杂,建议 0.5~0.8。默认 0.4"),
    # ---- 几何类 ----
    "degrees": (0.0, 45.0, 0.0, 1.0, "degrees 平面旋转(°)",
                "2D 平面内随机旋转角度。装甲板随机器人运动会出现各种朝向,建议 5~15。"
                "默认 0(官方默认不开)。注意:这是平面旋转,不是 roll/pitch/yaw 三维旋转"),
    "translate": (0.0, 0.5, 0.1, 0.01, "translate 平移",
                  "随机平移(占图片比例)。模拟目标偏离画面中心。默认 0.1"),
    "scale": (0.0, 0.9, 0.5, 0.05, "scale 缩放抖动",
              "随机缩放幅度。scale=0.5 表示目标可被缩到 0.5~1.5 倍,是模拟远近/小目标"
              "最直接的参数。小目标场景建议 0.5~0.9。默认 0.5"),
    "shear": (0.0, 10.0, 0.0, 0.1, "shear 剪切(°)",
              "随机剪切角度,模拟视角倾斜。默认 0"),
    "perspective": (0.0, 0.001, 0.0, 0.0001, "perspective 透视变换",
                    "透视变换强度,轻微模拟 3D 视角变化(相机与装甲板不垂直的情况)。"
                    "默认 0,可试 0.0005 以内"),
    # ---- 翻转 ----
    "fliplr": (0.0, 1.0, 0.5, 0.05, "fliplr 水平翻转概率",
               "水平翻转。装甲板左右翻转后仍可识别时建议开(默认 0.5)"),
    "flipud": (0.0, 1.0, 0.0, 0.05, "flipud 垂直翻转概率",
               "垂直翻转。常规地面机器人场景不开(机器人不会倒立),航拍/俯视可开。默认 0"),
    # ---- 高级组合 ----
    "mosaic": (0.0, 1.0, 1.0, 0.05, "mosaic 四图拼接概率",
               "四图拼成一张训练,显著增加小目标上下文多样性,RoboMaster 强烈建议保持 1.0。"
               "训练结束前 close_mosaic 个 epoch 会自动关闭。默认 1.0"),
    "mixup": (0.0, 1.0, 0.0, 0.05, "mixup 两图混合概率",
              "两张图线性叠加。默认 0,一般 0.1~0.2 试探性使用"),
    "cutmix": (0.0, 1.0, 0.0, 0.05, "cutmix 区域混合概率",
               "把另一张图的矩形区域贴进来。默认 0"),
    "copy_paste": (0.0, 1.0, 0.0, 0.05, "copy_paste 复制粘贴概率",
                   "目标复制粘贴。注意:检测任务需要分割标注才生效,bbox 训练时此参数无效。默认 0"),
    "close_mosaic": (0, 30, 10, 1, "close_mosaic 末尾关闭 mosaic",
                     "训练最后 N 个 epoch 关闭 mosaic,让模型适应真实单图画面。默认 10"),
    # ---- 其他训练相关(影响增强效果呈现) ----
    "erasing": (0.0, 1.0, 0.4, 0.05, "erasing 随机擦除概率",
                "分类任务的随机擦除(检测任务默认 0.4 但主要作用于分类分支)。默认 0.4"),
}

# 参数分组(面板展示顺序)
PARAM_GROUPS = {
    "🎨 颜色 / 光照": ["hsv_h", "hsv_s", "hsv_v"],
    "📐 几何变换": ["degrees", "translate", "scale", "shear", "perspective"],
    "🔄 翻转": ["fliplr", "flipud"],
    "🧩 高级组合": ["mosaic", "mixup", "cutmix", "copy_paste", "close_mosaic"],
    "⚙️ 其他": ["erasing"],
}

# 导出训练命令时要包含的参数(全部导出,显式优于隐式)
EXPORT_KEYS = [k for k in PARAM_SPECS]

# 进入官方 transforms 管道所需的完整 hyp(v8_transforms 会访问这些键;
# 未暴露成滑块的键使用官方默认值)
_HYP_FIXED = {
    "hsv_h": 0.015, "hsv_s": 0.7, "hsv_v": 0.4,
    "degrees": 0.0, "translate": 0.1, "scale": 0.5,
    "shear": 0.0, "perspective": 0.0,
    "fliplr": 0.5, "flipud": 0.0,
    "mosaic": 1.0, "mixup": 0.0, "cutmix": 0.0, "copy_paste": 0.0,
    "copy_paste_mode": "flip",
    "close_mosaic": 10, "erasing": 0.4,
    "augmentations": None,
}


def build_hyp(values: dict) -> dict:
    """把滑块取值合并进完整 hyp 字典(未提供的键取官方默认)。"""
    hyp = dict(_HYP_FIXED)
    hyp.update({k: v for k, v in values.items() if k in _HYP_FIXED})
    return hyp
