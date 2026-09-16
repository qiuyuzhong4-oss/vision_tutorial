# YOLO 数据增强工作台

针对 **RoboMaster 装甲板检测(小目标 + 光照多变)** 场景设计的本地数据准备工具,两个模块形成数据闭环:

**数据准备 → 增强调参 → 半自动标注 → 再训练**

- 🎨 **增强工作台**:上传自己的图 + YOLO 标签 → 滑块调参 → **官方训练管道(v8_transforms)实时预览** → 一键导出 `yolo train` 命令 / hyp YAML / 预设 JSON
- 🚀 **在本机训练**(最终目标):选定参数后不离开工作台直接用本机 GPU 开训(参数作为覆盖项传给训练,GPU 掉线自动预检重试/CPU 降级)
- 🏷️ **半自动标注**:种子集检查 → 快速训练 → 伪标签生成 → 人工审核 → 导出标准 YOLO 数据集

预览与训练的一致性:直接调用 `ultralytics.data.augment.v8_transforms()`(与 `YOLO.train()` 内部同一条管道),bbox 同步变换已通过数值校验(letterbox/翻转零误差,mosaic 模式 13/13 框对齐)。

## 本机硬件适配(RTX 5060 Laptop 8GB)

侧栏自动显示 GPU 状态,分层诊断"有时连不上"的原因:

| 现象 | 原因 | 处理 |
|------|------|------|
| nvidia-smi 无响应(自动重试 3 次) | 驱动掉卡:笔记本休眠/供电波动 | 等 10 秒刷新 → 重启程序 → 重启系统 |
| nvidia-smi 正常但 torch 看不到 CUDA | torch 构建不含 sm_120 支持 | 必须 cu128+:`pip install torch --index-url https://download.pytorch.org/whl/cu128` |
| CUDA 可用但设备查询异常 | 显存被占满 | 关掉占显存的进程再刷新 |

训练启动前驱动探活带重试,失败自动降级 CPU 并明确提示。8GB 显存:batch=-1 自适应,imgsz 1280 时 batch 4~8。

## 长期积累:场景 → 算法

- 预设库:[wb/presets_user/](wb/presets_user/README.md) 每个验证过的场景一个 JSON,启动自动并入预设下拉框
- 参数与痛点映射:[../30_Knowledge/computer-vision/YOLO训练参数手册.md](../30_Knowledge/computer-vision/YOLO训练参数手册.md)(活文档:群里问的、AI 推荐的、已有程序里看到的,持续回填)

## 启动(run.sh)

```bash
cd yolo_workbench
./run.sh            # 启动(后台运行,首次自动装依赖+GPU预检)
./run.sh status     # 状态 + GPU 诊断
./run.sh log        # 跟踪日志
./run.sh stop       # 停止
./run.sh restart    # 重启
# 换端口: WORKBENCH_PORT=9000 ./run.sh
```

启动时自动做 GPU 分层预检(复用 wb/device.py),掉卡时提前看到提示;服务在后台运行,日志写 `workbench.log`。

手动方式:`pip install -r requirements.txt && streamlit run app.py`

## 增强工作台使用建议

1. 上传 1~6 张**真实采集图**(建议含远距离小目标)+ 同名 `.txt` 标签
2. 选预设 **「RoboMaster 装甲板(小目标+光照多变)」** 应用
3. 预览模式:
   - *单图增强*:关闭 mosaic/mixup,看单个参数对图和框做了什么
   - *完整训练管道*:与训练完全一致(含 mosaic 四图拼接)
   - *批量网格*:每图 3 个变体,看参数的随机分布
4. 同一"随机种子"下拖滑块结果可对照;点🎲换随机
5. 满意后复制导出的训练命令,或下载 hyp YAML

### RoboMaster 预设的参数依据

| 参数 | 值 | 原因 |
|------|-----|------|
| hsv_v=0.6 | 明度抖动加大 | 场地灯光多变、逆光、曝光变化 |
| hsv_h=0.01 | 色调抖动压小 | 红/蓝是类别依据,防止偏色混淆 |
| scale=0.9 | 缩放抖动拉满 | 模拟远距离小目标 |
| degrees=10 | 平面旋转 | 装甲板各朝向 |
| mosaic=1.0 | 四图拼接 | 小目标上下文多样性 |
| perspective=0.0005 | 轻微透视 | 相机与装甲板不垂直 |

显存允许时把 imgsz 提到 1280,小目标收益明显。

## 半自动标注使用建议

1. 人工标注种子集(建议 100~500 张,类别覆盖均匀、框贴紧边界)
2. 填目录 → 检查(看类别直方图/缺标/小目标占比)→ 启动快训(n/s 模型、30~60 epochs)
3. 训练在子进程跑,不阻塞页面;完成后对未标注目录推理(阈值建议 0.7,**宁漏勿错**)
4. **逐张人工审核**:删错框、改类别、补漏检框 → 通过/拒绝
5. 导出审核通过的部分,与种子集合并再训一轮,迭代提升

> ⚠️ 审核环节不可省略:伪标签错误会污染后续训练。

## 目录结构

```
yolo_workbench/
├── app.py            # Streamlit 入口(两个标签页 + 侧栏 GPU 面板)
├── train_runner.py   # 训练子进程(设备预检+增强参数透传,避免卡死界面)
├── wb/
│   ├── params.py     # 参数注册表(范围/默认/中文说明)
│   ├── presets.py    # 场景预设 + presets_user/ 用户预设库加载
│   ├── device.py     # GPU 适配:5060 分层诊断/驱动重试/CPU 降级
│   ├── dataset.py    # 内存 dataset 适配器(喂给官方管道)
│   ├── preview.py    # 官方管道预览 + 画框
│   ├── exporter.py   # 训练命令/YAML/预设 导出
│   ├── autolabel.py  # 伪标签:扫描/训练/推理/审核/导出
│   └── presets_user/ # 长期积累:场景→算法 参数库(JSON)
└── autolabel_work/   # 运行时生成:data.yaml、train.log、runs/、review_state.json、export/
```

设计文档见 [YOLO增强工作台项目计划.md](../30_Knowledge/computer-vision/YOLO增强工作台项目计划.md),
参数手册见 [YOLO训练参数手册.md](../30_Knowledge/computer-vision/YOLO训练参数手册.md)。
