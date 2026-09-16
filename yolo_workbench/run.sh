#!/usr/bin/env bash
# ============================================================
# YOLO 增强工作台 启动/管理脚本
#
# 用法:
#   ./run.sh            启动(后台,首次自动装依赖+GPU预检)
#   ./run.sh stop       停止
#   ./run.sh restart    重启
#   ./run.sh status     运行状态 + GPU 状态
#   ./run.sh log        跟踪日志(Ctrl+C 退出,不影响服务)
#
# 端口:环境变量 WORKBENCH_PORT 覆盖(默认 8638)
# ============================================================
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PORT="${WORKBENCH_PORT:-8638}"
LOG="$DIR/workbench.log"
PID_FILE="$DIR/workbench.pid"
URL="http://127.0.0.1:$PORT"

# ---------- GPU 预检(复用 wb/device.py 的分层诊断) ----------
gpu_check() {
  python3 - <<'PYEOF' 2>/dev/null
import sys
sys.path.insert(0, ".")
from wb.device import diagnose, status_line
d = diagnose()
print("[GPU] " + status_line(d))
if d["level"] == "error":
    for h in d["hints"]:
        print("  !! " + h)
PYEOF
  # 诊断失败不阻断启动(工作台内会降级 CPU 并提示)
  return 0
}

# ---------- 运行状态判断:pid 文件优先,端口探活兜底 ----------
is_running() {
  if [ -f "$PID_FILE" ]; then
    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
    rm -f "$PID_FILE"
  fi
  curl -sf "$URL/_stcore/health" >/dev/null 2>&1
}

do_start() {
  if is_running; then
    echo "已在运行: $URL  (日志: $LOG)"
    return 0
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "错误: 未找到 python3" >&2
    exit 1
  fi
  if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "首次运行:安装依赖(streamlit/ultralytics 等,可能需要几分钟)..."
    pip install -r requirements.txt || { echo "依赖安装失败,请手动执行: pip install -r requirements.txt" >&2; exit 1; }
  fi

  gpu_check

  nohup streamlit run app.py --server.headless true --server.port "$PORT" > "$LOG" 2>&1 &
  echo $! > "$PID_FILE"

  # 等待就绪(最多 30 秒,首次导入 ultralytics 较慢)
  for _ in $(seq 1 30); do
    if curl -sf "$URL/_stcore/health" >/dev/null 2>&1; then
      echo "启动成功: $URL"
      echo "        日志: $LOG   停止: ./run.sh stop"
      return 0
    fi
    sleep 1
  done
  echo "启动失败,日志尾部:" >&2
  tail -20 "$LOG" >&2
  exit 1
}

do_stop() {
  local stopped=""
  if [ -f "$PID_FILE" ]; then
    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [ -n "$pid" ] && kill "$pid" 2>/dev/null; then
      stopped="$pid"
    fi
    rm -f "$PID_FILE"
  else
    # 兜底:按命令特征清理(例如 pid 文件丢失)
    if pkill -f "streamlit run app.py.*--server.port $PORT" 2>/dev/null; then
      stopped="(按端口 $PORT)"
    fi
  fi

  if [ -z "$stopped" ]; then
    echo "未在运行"
    return 0
  fi
  # 等待端口真正释放(进程收尾需 1~2 秒),最多 10 秒后强杀
  for _ in $(seq 1 10); do
    if ! curl -sf "$URL/_stcore/health" >/dev/null 2>&1; then
      echo "已停止 $stopped"
      return 0
    fi
    sleep 1
  done
  pkill -9 -f "streamlit run app.py.*--server.port $PORT" 2>/dev/null || true
  echo "已强制停止 $stopped"
}

do_status() {
  if is_running; then
    echo "服务: 运行中  $URL"
    [ -f "$PID_FILE" ] && echo "      pid: $(cat "$PID_FILE")  日志: $LOG"
  else
    echo "服务: 未运行 (启动: ./run.sh)"
  fi
  gpu_check
}

do_log() {
  [ -f "$LOG" ] || { echo "暂无日志: $LOG"; exit 0; }
  tail -n 50 -f "$LOG"
}

case "${1:-start}" in
  start)   do_start ;;
  stop)    do_stop ;;
  restart) do_stop; sleep 1; do_start ;;
  status)  do_status ;;
  log)     do_log ;;
  *)
    echo "用法: $0 {start|stop|restart|status|log}"
    echo "  (无参数 = start;端口用环境变量 WORKBENCH_PORT 覆盖,默认 $PORT)"
    exit 1
    ;;
esac
