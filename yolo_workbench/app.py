# -*- coding: utf-8 -*-
"""YOLO 数据增强工作台 —— Streamlit 入口

Tab1 增强工作台:上传图片+标签 → 滑块调参 → 官方管道实时预览 → 一键导出训练配置
Tab2 半自动标注:种子集检查 → 快速训练(子进程) → 伪标签生成 → 人工审核 → 导出数据集

启动: streamlit run app.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import cv2
import numpy as np
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wb.autolabel import (  # noqa: E402
    build_data_yaml, draw_review, export_approved, find_latest_weights,
    generate_pseudo_labels, label_path_for, list_images, load_review_state,
    parse_class_names, save_review_state, scan_seed,
)
from wb.dataset import Sample, parse_yolo_label  # noqa: E402
from wb.device import diagnose, preflight_for_training, status_line  # noqa: E402
from wb.exporter import (  # noqa: E402
    build_hyp_yaml, build_preset_json, build_train_command, load_preset_json,
)
from wb.params import PARAM_GROUPS, PARAM_SPECS  # noqa: E402
from wb.preview import draw_boxes, run_pipeline, variants  # noqa: E402
from wb.presets import DEFAULT_PRESET_NAME, all_presets  # noqa: E402

WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autolabel_work")
TRAIN_PROJECT = os.path.join(WORK_DIR, "runs")

st.set_page_config(page_title="YOLO 增强工作台", page_icon="🛠️", layout="wide")

if "first_run" not in st.session_state:
    st.session_state.first_run = True
    for k, spec in PARAM_SPECS.items():
        st.session_state[f"p_{k}"] = spec[2]  # 官方默认
    st.session_state.imgsz = all_presets()[DEFAULT_PRESET_NAME]["imgsz"] \
        if DEFAULT_PRESET_NAME in all_presets() else 640
    st.session_state.seed = 7


# ============================================================== 侧栏:设备状态
def device_panel():
    with st.sidebar:
        st.subheader("🖥️ 本机设备")
        if "device_diag" not in st.session_state or st.button("🔄 重新检测 GPU"):
            st.session_state.device_diag = diagnose()
        d = st.session_state.device_diag
        st.markdown(f"**{status_line(d)}**")
        shower = {"ok": st.success, "warn": st.warning, "error": st.error}[d["level"]]
        for h in d["hints"]:
            shower(h)
        st.divider()


def _proc_running(proc: dict | None) -> bool:
    """检查子进程是否还活着(不真正发信号)。"""
    if not proc:
        return False
    try:
        os.kill(proc["pid"], 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _show_proc_log(proc: dict | None, height_lines: int = 25):
    """展示子进程日志尾部与训练产物状态。"""
    w = find_latest_weights(TRAIN_PROJECT)
    if _proc_running(proc):
        st.warning(f"训练进行中(pid={proc['pid']})。日志实时写入,点『刷新状态』更新。")
    if w:
        st.success(f"最新权重:{w}")
        st.session_state.al_weights = w
    if proc and os.path.isfile(proc["log"]):
        with open(proc["log"]) as f:
            tail = f.readlines()[-height_lines:]
        st.code("".join(tail), language="log")


# ============================================================== Tab1 增强工作台
def tab_augment():
    st.caption("预览直接调用 ultralytics 官方训练管道(v8_transforms),所见即训练所得。"
               "建议上传几张真实采集图 + 对应 YOLO 标签,效果最有参考价值。")

    ctrl, main = st.columns([1, 2.2], gap="large")

    # ---------------- 左侧控制面板 ----------------
    with ctrl:
        st.subheader("🎛️ 参数面板")

        presets = all_presets()
        preset_name = st.selectbox("场景预设(含 presets_user/ 积累库)", list(presets.keys()),
                                   index=list(presets.keys()).index(DEFAULT_PRESET_NAME)
                                   if DEFAULT_PRESET_NAME in presets else 0)
        st.caption(presets[preset_name]["note"])
        c1, c2 = st.columns(2)
        if c1.button("应用预设", use_container_width=True, type="primary"):
            for k, v in presets[preset_name]["values"].items():
                st.session_state[f"p_{k}"] = v
            st.session_state.imgsz = presets[preset_name]["imgsz"]
            st.rerun()
        if c2.button("恢复官方默认", use_container_width=True):
            for k, spec in PARAM_SPECS.items():
                st.session_state[f"p_{k}"] = spec[2]
            st.rerun()

        st.session_state.imgsz = st.select_slider("imgsz 输入尺寸",
                                                  options=[320, 416, 480, 512, 640, 800, 960, 1080, 1280, 1536],
                                                  value=st.session_state.imgsz,
                                                  help="尽量与最终部署时相机取流喂给模型的分辨率一致")
        mode = st.radio("预览模式", ["单图增强(看参数效果)", "完整训练管道(含Mosaic)", "批量网格(每图3变体)"],
                        help="单图模式关闭 mosaic/mixup,便于看清单个参数的作用;完整模式与训练完全一致")
        cc1, cc2 = st.columns([1, 1])
        st.session_state.seed = cc1.number_input("随机种子", 0, 9999, st.session_state.seed)
        if cc2.button("🎲 换个随机", use_container_width=True):
            st.session_state.seed = int(np.random.randint(0, 10000))
            st.rerun()

        st.divider()
        for group, keys in PARAM_GROUPS.items():
            with st.expander(group, expanded=(group == "🎨 颜色 / 光照")):
                for k in keys:
                    lo, hi, default, step, name, desc = PARAM_SPECS[k]
                    st.slider(name, lo, hi, key=f"p_{k}", step=step, help=desc)

    values = {k: st.session_state[f"p_{k}"] for k in PARAM_SPECS}

    # ---------------- 右侧:上传与预览 ----------------
    with main:
        up_imgs = st.file_uploader("上传图片(建议 1~6 张真实采集图)",
                                   type=["jpg", "jpeg", "png", "bmp", "webp"],
                                   accept_multiple_files=True)
        up_lbls = st.file_uploader("上传对应 YOLO 标签(可选,同名 .txt 匹配;上传后可看到框的同步变换)",
                                   type=["txt"], accept_multiple_files=True)
        class_names = [s for s in st.text_input("类别名(逗号分隔,画框图例用)",
                                                value="red,blue").split(",") if s.strip()]
        if not up_imgs:
            st.info("👈 请先上传图片。没有标签也能预览图片级效果(颜色/几何),有标签才能看到框的同步变换。"
                    "下方的**导出配置**和**在本机训练**不依赖预览图,可直接使用。")

        label_map = {}
        for f in up_lbls or []:
            label_map[os.path.splitext(f.name)[0]] = f.read().decode("utf-8", "ignore")

        samples, missing = [], []
        for f in (up_imgs or []):
            img = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                continue
            stem = os.path.splitext(f.name)[0]
            if stem in label_map:
                cls, boxes = parse_yolo_label(label_map[stem])
            else:
                cls, boxes = np.zeros(0), np.zeros((0, 4))
                missing.append(f.name)
            samples.append(Sample(f.name, img, cls, boxes))

        if missing:
            st.warning(f"这些图片没找到同名标签(只预览图片效果): {', '.join(missing)}")

        enable_mix = "完整训练" in mode or "批量" in mode
        if up_imgs:
            st.divider()

        if mode.startswith("单图") or mode.startswith("完整"):
            for s, res in zip(samples, run_pipeline(samples, values, st.session_state.imgsz,
                                                    st.session_state.seed, enable_mix)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**原图** · {s.name}")
                    orig = draw_boxes(s.img, s.bboxes * np.array([s.img.shape[1], s.img.shape[0]] * 2),
                                      s.cls, class_names)
                    st.image(orig)
                with col2:
                    st.markdown(f"**增强后** · {len(res['boxes'])} 框 · 类别 {res['cls']}")
                    st.image(res["aug_rgb"])
        else:  # 批量网格
            vs = variants(samples, values, st.session_state.imgsz, st.session_state.seed, n=3)
            for vi, batch in enumerate(vs):
                st.markdown(f"**变体 {vi + 1}**(种子 {st.session_state.seed + vi * 101})")
                cols = st.columns(max(min(len(batch), 3), 1))
                for ci, res in enumerate(batch):
                    with cols[ci % len(cols)]:
                        st.image(res["aug_rgb"], caption=f"{res['name']} · {len(res['boxes'])}框")

        # ---------------- 导出 ----------------
        st.divider()
        st.subheader("📤 一键导出训练配置")
        data_yaml = st.text_input("data.yaml 路径(命令占位,可后改)", value="your_data.yaml")
        model_pt = st.text_input("预训练权重", value="yolo11n.pt")
        epochs = st.number_input("epochs", 10, 500, 100, 10)
        cmd = build_train_command(values, st.session_state.imgsz, data_yaml, model_pt, int(epochs))
        st.code(cmd, language="bash")
        dc1, dc2, dc3 = st.columns(3)
        dc1.download_button("下载 hyp YAML", build_hyp_yaml(values, st.session_state.imgsz),
                            file_name="aug_hyp.yaml", mime="text/yaml", use_container_width=True)
        preset_json = build_preset_json(values, st.session_state.imgsz, name=preset_name)
        dc2.download_button("下载当前预设 JSON", preset_json,
                            file_name="aug_preset.json", mime="application/json",
                            use_container_width=True)
        imp = dc3.file_uploader("导入预设 JSON", type=["json"])
        if imp is not None:
            loaded = load_preset_json(imp.read().decode("utf-8"))
            if st.button(f"应用导入的预设:{loaded['name']}"):
                for k, v in loaded["values"].items():
                    st.session_state[f"p_{k}"] = v
                st.session_state.imgsz = loaded["imgsz"]
                st.rerun()

        # ---------------- 一键训练(最终目标:选定算法后直接用本机 GPU 练) ----------------
        st.divider()
        st.subheader("🚀 在本机训练")
        st.caption("用上面调好的增强参数直接开训(参数会作为覆盖项传给训练,与导出脚本完全一致)。"
                   "GPU 掉线会自动预检重试,不行再降级 CPU 并提示。")
        if not os.path.isfile(data_yaml):
            st.warning(f"data.yaml 不存在:{data_yaml} —— 请先准备数据集配置"
                       "(可用『半自动标注』标签页导出生成)")
        device_pref = st.text_input("device(auto=自动 / cpu / 0 / 0,1)", value="auto")
        batch = st.number_input("batch(-1=按显存自适应,8GB 卡推荐)", -1, 64, -1, 1)
        workers = st.number_input("dataloader workers", 0, 16, 4, 1)

        proc_aug = st.session_state.get("train_proc_aug")
        tA, tB = st.columns([1, 1])
        can_start = os.path.isfile(data_yaml) and not _proc_running(proc_aug)
        if tA.button("🚀 启动训练", type="primary", use_container_width=True,
                     disabled=not can_start):
            aug_file = os.path.join(WORK_DIR, "aug_override.json")
            os.makedirs(WORK_DIR, exist_ok=True)
            with open(aug_file, "w") as f:
                json.dump({k: v for k, v in values.items()}, f)
            log_path = os.path.join(WORK_DIR, "train_aug.log")
            logf = open(log_path, "w")
            p = subprocess.Popen(
                [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "train_runner.py"),
                 "--data", data_yaml, "--model", model_pt, "--epochs", str(int(epochs)),
                 "--imgsz", str(st.session_state.imgsz), "--device", device_pref,
                 "--project", os.path.join(TRAIN_PROJECT, "aug"),
                 "--batch", str(int(batch)), "--workers", str(int(workers)),
                 "--aug", aug_file],
                stdout=logf, stderr=subprocess.STDOUT, cwd=WORK_DIR,
            )
            st.session_state.train_proc_aug = {"pid": p.pid, "log": log_path}
            st.success(f"训练已启动(pid={p.pid})。训练期间可以关页面,进程在后台跑;"
                       f"日志:{log_path}")
            st.rerun()
        if tB.button("🔄 刷新状态", use_container_width=True):
            st.rerun()
        _show_proc_log(proc_aug)


# ============================================================== Tab2 半自动标注
def tab_autolabel():
    st.caption("伪标签流程:人工标种子集 → 快速训练 → 模型自动标注 → 人工审核 → 导出。"
               "**审核环节不可省略**,错误标签会污染后续训练。")
    os.makedirs(WORK_DIR, exist_ok=True)

    with st.expander("① 数据目录与类别", expanded=True):
        img_dir = st.text_input("种子集图片目录(已人工标注)", value=st.session_state.get("al_img", ""),
                                key="al_img")
        lbl_dir = st.text_input("种子集标签目录(YOLO txt)", value=st.session_state.get("al_lbl", ""),
                                key="al_lbl",
                                help="留空则按惯例取 ../labels(与 images 同级)")
        unl_dir = st.text_input("待标注图片目录", value=st.session_state.get("al_unl", ""), key="al_unl")
        names_txt = st.text_input("类别名(逗号分隔,顺序=类别id)", value=st.session_state.get("al_names", "red,blue"),
                                  key="al_names")
        if not lbl_dir and img_dir:
            lbl_dir = os.path.join(os.path.dirname(img_dir.rstrip("/")), "labels")
        names = parse_class_names(names_txt)

        if st.button("🔍 检查种子集"):
            st.session_state.seed_scan = scan_seed(img_dir, lbl_dir)
        if "seed_scan" in st.session_state:
            sc = st.session_state.seed_scan
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("图片数", sc["n_images"])
            m2.metric("有标签", sc["n_labeled"])
            m3.metric("缺标签", sc["n_missing"])
            m4.metric("小目标占比", f"{sc['small_ratio']:.0%}")
            if sc["class_hist"]:
                st.bar_chart({names[k] if k < len(names) else f"cls{k}": v
                              for k, v in sorted(sc["class_hist"].items())})
                if len(sc["class_hist"]) == 1:
                    st.warning("只发现 1 个类别:请确认类别 id 是否覆盖完整")
            if sc["n_images"] == 0:
                st.error("种子集目录没有图片,请检查路径")
            elif sc["n_missing"]:
                st.warning(f"{sc['n_missing']} 张图缺标签:训练会跳过,建议补齐")
            if sc["n_images"] and sc["n_images"] < 100:
                st.info("种子集 <100 张:可以跑通流程,但建议 100~500 张、类别覆盖均匀")

    with st.expander("② 快速训练初始模型", expanded=False):
        t1, t2 = st.columns([1, 1])
        model_name = t1.selectbox("模型大小", ["yolo11n.pt", "yolo11s.pt", "yolo11m.pt"], index=0)
        device = t1.text_input("device", value=st.session_state.get("al_dev", "0"), key="al_dev",
                               help="GPU 用 0 / 0,1;CPU 用 cpu")
        epochs = t2.number_input("epochs(快训建议 30~60)", 5, 200, 50, 5)
        tr_imgsz = t2.select_slider("训练 imgsz", options=[320, 416, 480, 640, 800, 960, 1280], value=640)
        proc = st.session_state.get("train_proc")
        running = _proc_running(proc)

        colA, colB = st.columns(2)
        if colA.button("🚀 启动快速训练", disabled=running, type="primary"):
            if not os.path.isdir(img_dir) or not st.session_state.get("seed_scan"):
                st.error("请先完成 ① 中的种子集检查")
            else:
                data_yaml = build_data_yaml(img_dir, lbl_dir, names,
                                            os.path.join(WORK_DIR, "data.yaml"))
                log_path = os.path.join(WORK_DIR, "train.log")
                logf = open(log_path, "w")
                p = subprocess.Popen(
                    [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "train_runner.py"),
                     "--data", data_yaml, "--model", model_name, "--epochs", str(int(epochs)),
                     "--imgsz", str(tr_imgsz), "--device", device, "--project", TRAIN_PROJECT],
                    stdout=logf, stderr=subprocess.STDOUT, cwd=WORK_DIR,
                )
                st.session_state.train_proc = {"pid": p.pid, "log": log_path}
                st.success(f"训练已启动(pid={p.pid})。训练期间可做别的,回来点『刷新状态』")
                st.rerun()
        if colB.button("🔄 刷新状态"):
            st.rerun()

        _show_proc_log(proc)

    with st.expander("③ 生成伪标签", expanded=False):
        weights = st.text_input("权重路径(默认取最新训练结果)", value=st.session_state.get("al_weights", ""))
        conf = st.slider("置信度阈值(宁漏勿错,建议 0.6~0.85)", 0.1, 0.95, 0.7, 0.05)
        if st.button("🏷️ 对未标注目录推理", type="primary"):
            if not (weights and os.path.isfile(weights)):
                st.error("权重不存在:先完成 ② 训练,或手动填入 .pt 路径")
            elif not os.path.isdir(unl_dir):
                st.error("待标注目录无效")
            else:
                bar = st.progress(0.0, text="推理中...")
                state = generate_pseudo_labels(weights, unl_dir, WORK_DIR, conf,
                                               progress=lambda p: bar.progress(p, text=f"推理中 {p:.0%}"))
                n_box = sum(len(i["boxes"]) for i in state["items"].values())
                n_empty = sum(1 for i in state["items"].values() if not i["boxes"])
                bar.empty()
                st.success(f"完成:{len(state['items'])} 张图,共 {n_box} 框,"
                           f"{n_empty} 张无检出(需人工补标)")
                st.rerun()

    state = load_review_state(WORK_DIR)
    with st.expander("④ 人工审核(必须)", expanded=bool(state)):
        if not state:
            st.info("先在 ③ 生成伪标签,再在这里逐张审核。")
        else:
            review_ui(state)

    with st.expander("⑤ 导出数据集", expanded=False):
        out_root = st.text_input("导出目录", value=os.path.join(WORK_DIR, "export"))
        if st.button("📦 导出审核通过的图片+标签", type="primary"):
            state = state or load_review_state(WORK_DIR)
            if not state:
                st.error("没有审核状态:先完成 ③④")
            else:
                r = export_approved(state, out_root)
                if r["images"] == 0:
                    st.warning("没有『通过』的图片,先去 ④ 审核")
                else:
                    st.success(f"导出 {r['images']} 张图 / {r['boxes']} 框 → {r['root']}"
                               f"(含 images/train、labels/train、data.yaml)")
                    st.info("提示:导出集可与种子集合并后回到 ② 再训练一轮,迭代提升")


def review_ui(state: dict):
    names = state.get("names") or []
    if isinstance(names, dict):
        names = [names[k] for k in sorted(names, key=int)]
    items = state["items"]
    keys = list(items.keys())
    stats = {"pending": 0, "approved": 0, "rejected": 0}
    for it in items.values():
        stats[it["status"]] = stats.get(it["status"], 0) + 1
    m1, m2, m3 = st.columns(3)
    m1.metric("待审核", stats.get("pending", 0))
    m2.metric("已通过", stats.get("approved", 0))
    m3.metric("已拒绝", stats.get("rejected", 0))

    if "al_idx" not in st.session_state or st.session_state.al_idx >= len(keys):
        st.session_state.al_idx = 0
    idx = st.number_input("图片序号", 0, max(len(keys) - 1, 0), st.session_state.al_idx, key="al_idx_input")
    key = keys[int(idx)]
    item = items[key]

    img = cv2.imdecode(np.fromfile(item["path"], dtype=np.uint8), cv2.IMREAD_COLOR) \
        if os.path.isfile(item["path"]) else None
    if img is None:
        st.error(f"读不到图片:{item['path']}(目录被移动过?重新执行 ③)")
        return
    st.image(draw_review(img, item["boxes"], names),
             caption=f"{key} · 状态:{item['status']} · {len(item['boxes'])} 框")

    for bi, b in enumerate(item["boxes"]):
        cx, cy, w, h = b["xywhn"]
        c1, c2, c3, c4 = st.columns([0.3, 0.3, 0.25, 0.15])
        b["keep"] = c1.checkbox("保留", value=b["keep"], key=f"keep_{key}_{bi}")
        b["cls"] = c2.selectbox("类别", range(len(names)) if names else [0],
                                index=min(b["cls"], max(len(names) - 1, 0)) if names else 0,
                                format_func=lambda i: names[i] if names else str(i),
                                key=f"cls_{key}_{bi}")
        c3.caption(f"conf {b['conf']:.2f} · 框 {cx:.2f},{cy:.2f},{w:.2f},{h:.2f}")
        if c4.button("删", key=f"del_{key}_{bi}"):
            item["boxes"].pop(bi)
            save_review_state(state, WORK_DIR)
            st.rerun()

    with st.expander("➕ 补一个漏检框(归一化 cx cy w h)"):
        n1, n2, n3, n4, n5 = st.columns(5)
        ncx = n1.number_input("cx", 0.0, 1.0, 0.5, 0.01, key=f"acx_{key}")
        ncy = n2.number_input("cy", 0.0, 1.0, 0.5, 0.01, key=f"acy_{key}")
        nw = n3.number_input("w", 0.0, 1.0, 0.1, 0.01, key=f"aw_{key}")
        nh = n4.number_input("h", 0.0, 1.0, 0.1, 0.01, key=f"ah_{key}")
        ncls = n5.number_input("类别id", 0, max(len(names) - 1, 0), 0, key=f"acls_{key}")
        if st.button("添加该框", key=f"aadd_{key}"):
            item["boxes"].append({"cls": int(ncls), "conf": 1.0,
                                  "xywhn": [ncx, ncy, nw, nh], "keep": True})
            save_review_state(state, WORK_DIR)
            st.rerun()

    a1, a2 = st.columns(2)
    if a1.button("✅ 通过并下一张", type="primary", use_container_width=True):
        item["status"] = "approved"
        st.session_state.al_idx = min(int(idx) + 1, len(keys) - 1)
        save_review_state(state, WORK_DIR)
        st.rerun()
    if a2.button("❌ 拒绝并下一张", use_container_width=True):
        item["status"] = "rejected"
        st.session_state.al_idx = min(int(idx) + 1, len(keys) - 1)
        save_review_state(state, WORK_DIR)
        st.rerun()


# ============================================================== 入口
device_panel()
tab1, tab2 = st.tabs(["🎨 增强工作台", "🏷️ 半自动标注"])
with tab1:
    tab_augment()
with tab2:
    tab_autolabel()
