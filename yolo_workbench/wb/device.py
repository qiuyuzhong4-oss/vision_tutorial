# -*- coding: utf-8 -*-
"""GPU 设备适配层:针对本机 RTX 5060 Laptop(sm_120, Blackwell)。

5060 "有时连不上"的常见原因,按层诊断:
1. 驱动层:nvidia-smi 都失败 —— 笔记本休眠/供电掉卡/驱动崩溃 → 提示重启或重插
2. 构建层:nvidia-smi 正常但 torch.cuda.is_available()=False
   —— sm_120 要求 torch 为 cu128 及以上构建(cu126 会报 no kernel image)
3. 运行层:is_available()=True 但初始化失败 —— 显存被占满/驱动半死
4. 版本层:算力 sm>=12.0 但 torch.version.cuda < 12.8 → 明确不兼容

所有函数都不抛异常,返回结构化状态,UI 直接展示。
"""
from __future__ import annotations

import re
import subprocess

import torch

# sm_120 需要 CUDA 12.8+ 构建
MIN_CUDA_FOR_SM120 = (12, 8)


def _run(cmd: list[str], timeout: float = 6.0) -> tuple[bool, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode == 0, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, str(e)


def probe_driver(retries: int = 2, delay: float = 1.5) -> dict:
    """探测 nvidia-smi(驱动层),失败时带重试——对应'有时候连不上'。"""
    import time

    last_out = ""
    for attempt in range(retries + 1):
        ok, out = _run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
                        "--format=csv,noheader"])
        if ok and out.strip():
            m = re.match(r"\s*([^,]+),\s*([^,]+),\s*([^\s]+)", out.strip())
            return {"ok": True, "attempts": attempt + 1,
                    "name": m.group(1).strip() if m else "?",
                    "vram": m.group(2).strip() if m else "?",
                    "driver": m.group(3).strip() if m else "?"}
        last_out = out
        if attempt < retries:
            time.sleep(delay)
    return {"ok": False, "attempts": retries + 1, "error": last_out.strip()[:300]}


def probe_torch() -> dict:
    """探测 torch CUDA(构建层+运行层),不抛异常。"""
    info = {
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda or "none",
        "available": False,
        "name": None, "vram_gb": None, "sm": None,
        "error": None,
    }
    try:
        info["available"] = torch.cuda.is_available()
    except Exception as e:  # 驱动半死时 is_available 也可能抛
        info["error"] = f"{type(e).__name__}: {e}"[:300]
        return info
    if not info["available"]:
        return info
    try:
        p = torch.cuda.get_device_properties(0)
        info["name"] = p.name
        info["vram_gb"] = round(p.total_memory / 2**30, 1)
        info["sm"] = f"{p.major}.{p.minor}"
    except Exception as e:
        info["error"] = f"{type(e).__name__}: {e}"[:300]
    return info


def diagnose() -> dict:
    """完整诊断:驱动层 + torch 层 + 结论/建议。"""
    drv = probe_driver()
    tp = probe_torch()
    hints: list[str] = []
    level = "ok"  # ok | warn | error

    if not drv["ok"]:
        level = "error"
        hints.append("nvidia-smi 无响应(重试后仍失败):大概率驱动掉卡。"
                     "笔记本常见于休眠唤醒/供电波动;依次尝试:等 10 秒再刷新 → "
                     "重启程序 → 重启系统;台式机检查供电线与 PCIe 供电。")
    elif not tp["available"]:
        level = "error"
        hints.append(f"驱动正常({drv['name']})但 torch 看不到 CUDA。"
                     f"当前 torch={tp['torch']}(CUDA 构建 {tp['torch_cuda']})。"
                     "5060 是 Blackwell(sm_120),必须 cu128 及以上构建;装成 cu126 会报 "
                     "'no kernel image'。修复: pip install torch --index-url "
                     "https://download.pytorch.org/whl/cu128")
    else:
        if tp["sm"]:
            major, minor = (int(x) for x in tp["sm"].split("."))
            cuda_build = tp["torch_cuda"]
            build_parts = tuple(int(x) for x in cuda_build.split(".")[:2]) if \
                cuda_build not in (None, "none") else (0, 0)
            if major >= 12 and build_parts < MIN_CUDA_FOR_SM120:
                level = "error"
                hints.append(f"GPU 算力 sm_{tp['sm'].replace('.', '')} 需要 CUDA≥12.8 构建,"
                             f"当前 torch 构建 {cuda_build},训练会报 no kernel image。"
                             "请升级: pip install torch --index-url "
                             "https://download.pytorch.org/whl/cu128")
        if tp["error"]:
            level = max(level, "warn", key=lambda x: {"ok": 0, "warn": 1, "error": 2}[x])
            hints.append(f"CUDA 可用但设备查询异常(可能显存被占满): {tp['error']}")
        elif not hints:
            hints.append(f"GPU 正常:{tp['name']} {tp['vram_gb']}GB(sm_{tp['sm'].replace('.', '')}),"
                         f"驱动 {drv.get('driver', '?')},torch {tp['torch']}。"
                         "8GB 显存建议 batch=auto、imgsz≤960;1280 训练需把 batch 降到 4~8。")

    return {"level": level, "driver": drv, "torch": tp, "hints": hints}


def resolve_device(pref: str = "") -> tuple[str, list[str]]:
    """把用户设备偏好解析成可用设备;CUDA 不可用时降级 CPU 并说明。

    返回 (device_str, warnings)。pref: ""/"auto"=自动, "cpu"=强制CPU, "0"/"0,1"=指定卡
    """
    d = diagnose()
    warns = []
    if pref.strip().lower() == "cpu":
        return "cpu", ["按设置强制使用 CPU(训练会慢很多)"]
    if pref and pref != "auto" and d["level"] == "ok":
        return pref.strip(), []
    if d["level"] == "ok":
        return "0", []
    # 不可用 → CPU 降级
    warns.append("CUDA 不可用,已降级为 CPU 训练(速度大幅下降)。")
    warns += d["hints"]
    return "cpu", warns


def preflight_for_training(pref: str = "", attempts: int = 3, delay: float = 3.0) -> tuple[str, list[str]]:
    """训练启动前的最终预检:驱动层带重试(应对瞬时掉卡)。"""
    import time

    warns = []
    if pref.strip().lower() != "cpu":
        drv = probe_driver(retries=attempts - 1, delay=delay)
        if not drv["ok"]:
            warns.append(f"nvidia-smi 连续 {attempts} 次无响应,放弃 GPU。")
            dev, w = resolve_device("cpu")
            return dev, warns + w
        if drv.get("attempts", 1) > 1:
            warns.append(f"驱动第 {drv['attempts']} 次探测才成功(GPU 之前瞬时不响应),"
                         "建议尽快重启系统排查。")
    return resolve_device(pref)


def status_line(d: dict | None = None) -> str:
    """一行状态摘要,供 UI 标题展示。"""
    d = d or diagnose()
    if d["level"] == "ok":
        tp = d["torch"]
        return f"GPU 就绪:{tp['name']} {tp['vram_gb']}GB"
    if d["level"] == "warn":
        return "GPU 可用(有警告,见诊断)"
    return "GPU 不可用(CPU 降级,见诊断)"
