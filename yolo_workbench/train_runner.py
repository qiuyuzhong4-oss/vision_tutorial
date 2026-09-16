# -*- coding: utf-8 -*-
"""训练子进程入口:由 app.py 通过 subprocess 启动,输出写到日志文件。

用法:
  python train_runner.py --data data.yaml --model yolo11n.pt \
      --epochs 50 --imgsz 640 --device 0 --project runs/autolabel \
      [--aug aug.json]   # 增强超参 JSON 文件(model.train 的覆盖参数)

启动前做 GPU 预检(驱动层带重试,应对 5060 偶发掉卡),CUDA 不可用自动降级 CPU。
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--model", default="yolo11n.pt")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--device", default="")
    ap.add_argument("--project", default="runs/autolabel")
    ap.add_argument("--batch", type=int, default=-1)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--aug", default="", help="增强超参 JSON 文件路径")
    args = ap.parse_args()

    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0] or ".")
    from wb.device import preflight_for_training

    device, warns = preflight_for_training(args.device)
    for w in warns:
        print(f"[device警告] {w}", flush=True)
    print(f"[device] 使用 {device} 开始训练", flush=True)

    aug_overrides = {}
    if args.aug:
        with open(args.aug) as f:
            aug_overrides = json.load(f)

    from ultralytics import YOLO

    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        device=device,
        project=args.project,
        name="seed",
        exist_ok=True,
        batch=args.batch if args.batch > 0 else None,  # -1 = auto,按显存自适应
        workers=args.workers,
        verbose=True,
        **aug_overrides,
    )
    print("TRAIN_DONE")


if __name__ == "__main__":
    main()
