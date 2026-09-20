---
name: yolo-training-params
description: YOLO (ultralytics) training parameter cheat sheet with RoboMaster-specific recommendations - data augmentation (hsv, mosaic, scale, degrees, copy_paste), training params (imgsz, batch, epochs, amp, cache), scene-pain-point to algorithm mapping (small targets, lighting changes, red-blue confusion, motion blur), and RTX 5060 8GB Blackwell cu128 environment notes. Use when configuring YOLO training for RM armor detection, tuning augmentation for small/distant targets, debugging GPU/torch "no kernel image" issues on consumer Blackwell GPUs, or deciding augmentation values. Trigger whenever the user mentions YOLO, yolo11, ultralytics, 训练参数, 数据增强, mosaic, hsv, imgsz, batch, 装甲板检测, 小目标, SAHI, 显存, 5060, cu128, 黑苹果, no kernel image, RM, RoboMaster, 训练.
---

# YOLO 训练参数速查（RM 场景）

## ⚠️ 活文档声明（最高优先级）

权威来源是**活文档**：`~/vision_tutorial/30_Knowledge/computer-vision/YOLO训练参数手册.md`（持续补充、标注来源与验证状态），配套可视化预览工具 `~/yolo_workbench`。
回答训练参数问题前**先读活文档最新版**；本 skill 只沉淀已验证的稳定结论。新结论回填活文档，不要只改这里。

## 验证闭环（所有结论都这么来）

猜测 → 工作台预览看增强效果 → 训练实测 mAP → 回填结论。
每条参数标注来源：✅实测 / 🗣️群结论 / 📦代码确认 / ⚠️未验证。警惕 AI 编造，没实测的标 ⚠️。

## RM 关键规则（已验证/官方确认）

| 参数 | RM 建议 | 原因 |
|------|---------|------|
| `hsv_h` | **≤0.01**（默认 0.015 压小） | 红蓝是类别依据，调大会类别混淆 |
| `hsv_v` | 0.5~0.8 | 场地灯光多变、逆光、曝光变化 |
| `scale` | 0.5~0.9 | 模拟远近，**小目标场景核心参数** |
| `degrees` | 5~15 | 装甲板各朝向；三维姿态官方不支持，需 Albumentations 自写 |
| `flipud` | 0 | 地面机器人不会倒立；航拍/俯视才开 |
| `mosaic` | 保持 1.0（`close_mosaic`=10） | 小目标上下文多样性 |
| `copy_paste` | 检测任务 bbox-only 数据集**无效** | 需分割标注才生效（📦官方代码确认） |
| `imgsz` | 小目标多可 960/1280 | 8GB 显存 1280 需 batch 4~8 |
| `batch` | **-1（自适应）** | 8GB 卡防 OOM |
| `amp` | True 保持开启 | FP16 省显存提速，精度基本无损 |
| `cache` | 别开 | 8G 内存 + 8G 显存 |
| `workers` | 4 | 笔记本 CPU |
| `model` | 先 n/s 验证流程，m 涨点再说 | — |
| `epochs` | 100~300；伪标签快训 30~60 | — |

## 场景痛点 → 手段映射（长期积累表）

| 痛点 | 数据侧 | 增强参数 | 推理侧 |
|------|--------|----------|--------|
| 小目标/远距离 | 补远距样本、标注贴紧 | scale=0.9、mosaic=1.0、imgsz↑ | **SAHI 切片推理**、两阶段 ROI（⚠️待实测） |
| 红蓝混淆 | — | **hsv_h 压小** | — |
| 光照多变 | 补多时段数据 | hsv_v↑、hsv_s↑ | — |
| 运动模糊 | 采集含运动帧 | ⚠️官方无内置 → Albumentations MotionBlur | — |
| 灯条过曝 | 补真实过曝样本（增强可能模拟不了） | hsv_v 抖动覆盖 | — |
| 视角倾斜 | — | degrees、perspective、shear | — |
| 长尾类别 | 过采样、定向补采 | mosaic 间接帮助 | — |

## 环境硬约束（本机 RTX 5060 Laptop 8GB）

- 算力 sm_120（Blackwell）→ **torch 必须 cu128+ 构建**，cu126 报 `no kernel image`；当前 torch 2.10.0+cu128 ✅
- "有时连不上"分层诊断：`nvidia-smi` 失败 = 驱动掉卡（休眠/供电，重启）；nvidia-smi 正常但 torch 看不到 = 构建层问题；显存被占满 = 运行层
- 训练启动前预检：驱动探活带重试，失败自动降级 CPU 并明确提示
