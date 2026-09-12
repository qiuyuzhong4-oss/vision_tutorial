🧠 推理框架 / 推理引擎

用来干什么？
它不是用来训练模型的，而是把训练好的模型运行起来并加速的工具。可以理解为模型的“播放器”+“涡轮增压器”。
🔄 ONNX / ONNX Runtime

    ONNX（Open Neural Network Exchange）：一种开放的模型格式，好比一个“万能转换器”，让模型可以在不同框架（PyTorch、TensorFlow等）之间自由转换。

    ONNX Runtime：微软推出的推理引擎，能高效运行 .onnx 格式的模型，支持CPU、GPU、ARM等多种硬件。

⚡ TensorRT

英伟达（NVIDIA）专门为自家GPU打造的推理加速引擎。它能让模型在NVIDIA显卡上跑得飞快，但不能在非NVIDIA硬件（如你的NUC11的Intel核显）上使用。
🎯 YOLO / YOLOv8

    YOLO（You Only Look Once）：一种目标检测算法，能在一张图里快速认出多个物体（人、车、猫等）。特点是速度快、精度不错。

    YOLOv8：YOLO系列的一个具体版本（目前很流行），由Ultralytics公司维护。

📦 PyTorch

一个非常流行的深度学习训练框架（类似TensorFlow）。我们用PyTorch来训练模型，得到 .pt 格式的模型文件。
🚀 Ultralytics

一家公司，也是他们开发的YOLO工具库。你写的 from ultralytics import YOLO 就是用它。它把PyTorch、模型导出、训练、推理等功能打包成非常简单的API，几行代码就能玩转YOLO。
💡 OpenVINO

英特尔推出的AI推理加速工具。它能充分利用Intel CPU、核显（iGPU）的性能，让你的YOLO模型在NUC这类Intel硬件上跑得飞快。它是你的NUC11的最佳选择。
🖥️ NUC11

英特尔推出的一款迷你电脑（Next Unit of Computing，第11代）。它通常搭载Intel CPU和Iris Xe核显，没有NVIDIA显卡。
📄 模型导出格式（.pt、.onnx、.engine、.xml/.bin）

    .pt：PyTorch原生格式，像“源代码”，方便修改但运行不是最快。

    .onnx：ONNX格式，可在多种设备上高效运行。

    .engine：TensorRT专用格式，只能在NVIDIA GPU上用。

    .xml / .bin：OpenVINO格式，xml是结构描述，bin是权重数据，你的NUC11上推荐使用。

🔢 FP16 / INT8 量化

    FP16（半精度浮点数）：把模型里的数字从32位精度缩减到16位，体积减半、速度提升，精度损失极小。

    INT8（8位整数）：进一步压缩到8位整数，速度更快，但可能轻微掉精度。适合追求极致速度的场景。

⚖️ 吞吐量模式（THROUGHPUT） / 延迟模式（LATENCY）

    THROUGHPUT模式：优先保证单位时间内处理尽可能多的图片，资源占用更平稳，适合多任务共存的场景（比如边跑YOLO边跑雷达）。

    LATENCY模式：优先保证每一帧处理得尽可能快，但可能会占满硬件，影响其他任务。

🔧 NUM_STREAMS / CPU_THREADS_NUM

    NUM_STREAMS：并行推理的“流”数量。设为1表示一次只做一件事，资源占用最小。

    CPU_THREADS_NUM：限制推理时使用的CPU线程数。比如设为2，最多只用2个CPU核心，给雷达留出其他核心。

🎚️ 优先级（priority LOW/MEDIUM/HIGH）

给推理任务设置一个“插队”等级。如果设为LOW，当CPU/GPU忙时，YOLO任务会被延后处理，优先保证雷达任务。
🎨 核显（iGPU）/ Iris Xe

    核显：集成在CPU内部的显卡，没有独立显存，但性能足够跑YOLO推理。

    Iris Xe：Intel第11代CPU上常见的一种核显型号，性能较强，配合OpenVINO能大幅加速。

🧩 算子融合（Operator Fusion）

一种优化技术：把连续的好几个计算步骤（比如“卷积 + 归一化 + 激活函数”）合并成一个步骤，减少数据搬运，提升速度。
📈 动态计算图

PyTorch默认的工作方式：每次运行都动态构建计算步骤，非常灵活但有额外开销。推理引擎（如TensorRT、OpenVINO）会把模型提前固定成静态图，省去这个开销。
⏳ 异步推理（Asynchronous Inference）

一种编程方式：发起推理请求后，不等待结果返回，先去干别的事（比如继续处理雷达数据），等结果准备好了再回来拿。可以更高效地利用硬件，避免空等。
📊 mAP（平均精度均值）

评估目标检测模型准确度的指标。mAP越高，说明模型找得越准（既不错报也不漏报）。通常在模型验证时查看。
🧰 OpenVINO Core API

OpenVINO提供的原生Python接口，比Ultralytics封装的YOLO类更底层、更灵活，可以让你精细控制线程数、优先级等参数。

如果你还有哪个词觉得不够清楚，或者想深入了解某个概念的具体用法，随时再问我～

