---
name: ros2-thread-naming
description: Thread and process naming and observability for ROS2 Humble on Ubuntu/Linux - pthread_setname_np, PID vs TID vs ROS node name vs Linux thread name, htop setup to show custom thread names, CPU/resource anomaly debugging. Use when writing multi-threaded C++/Python/rclcpp/rclpy nodes, giving AI engineering tasks about threads, or debugging high CPU usage and "I named my threads but htop doesn't show them". Trigger whenever the user mentions 线程命名, 进程命名, 线程名, htop, TID, PID, pthread_setname_np, prctl, executor 线程, CPU 占用, 资源异常, 可观测性, thread name, process name, perfetto, humble, rclpy, rclcpp.
---

# ROS2 进程/线程命名与可观测性

## 最高优先级：给 AI 下任务的标准话术（直接复制）

> 你在写代码的过程中要给进程和线程命名。我使用 ROS 2 Humble + Ubuntu/Linux 环境。涉及多线程时，明确区分 ROS 2 Node 名称、Linux 进程名、Linux 线程名和 TID。凡是程序自己创建的线程，都设置有业务含义的线程名称；凡是 ROS 2 Executor 内部创建的线程，要使用 Humble 实际支持的方式进行命名，并验证线程名能否在 Linux/htop/Perfetto 中实际显示。不要假设 ROS 2 Node 名称就是线程名或进程名。我会使用 htop 来看具体哪个进程哪个线程使用了多少资源。

## 四个名字，不要混淆

| 名字 | 位置 | 长度限制 | 设置方式 | 默认显示工具 |
|------|------|----------|----------|--------------|
| Linux 线程名 | `/proc/<pid>/task/<tid>/comm` | **15 字符**（超长静默截断） | `pthread_setname_np` / `prctl(PR_SET_NAME)` | htop（需开选项）、`ps -o comm` |
| Linux 进程名 | `/proc/<pid>/comm` | 15 字符 | 主线程名即进程名 | top、htop |
| 进程命令行 | `/proc/<pid>/cmdline` | argv 长度 | 修改 argv[0] / setproctitle | `ps aux`、htop 默认 Command 列 |
| ROS 2 Node 名 | ROS 图（graph）里的名字 | — | 节点构造参数 | `ros2 node list` |

关键事实：
- **htop 默认显示 cmdline 而不是线程 comm 名**——名字已生效但看不到，是没开显示选项，不是没设置成功。
- rclpy/rclcpp 只是 POSIX 的执行者，内部直接调 POSIX 创建线程；**Executor 内部创建的线程不能靠 `threading.Thread(name=)` 命名**，要用 Humble 实际支持的机制，并实际验证能在 Linux/Perfetto 看到。
- Python `threading.Thread(name=...)` 默认**不**设置操作系统线程名，需要 ctypes 调 libpthread。

## 代码片段

C++（线程名 ≤15 字符）：
```cpp
#include <pthread.h>
void set_thread_name(std::thread& t, const char* name) {   // 必须 ≤15 字符
    pthread_setname_np(t.native_handle(), name);
}
void set_current_thread_name(const char* name) {
    pthread_setname_np(pthread_self(), name);              // 或 prctl(PR_SET_NAME, name, 0, 0, 0);
}
// 用法：std::thread t([]{ set_current_thread_name("ctrl_loop"); ... });
```

Python：
```python
import ctypes, threading
def set_thread_name(name: str):
    name = name[:15].encode('ascii', 'replace')
    libpthread = ctypes.CDLL("libpthread.so.0")
    libpthread.pthread_setname_np.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    libpthread.pthread_setname_np(libpthread.pthread_self(), name)
# 传入 target 前/线程内部调用；Executor 内部线程按 Humble 机制处理
```

## htop 开启自定义线程名显示（一次性设置）

1. 打开 htop，按 **F2**（Setup）（或直接鼠标点左下角 Setup）
2. 进入 **Display options**
3. 勾选 **Show custom thread names**
4. 保存退出——注意：本机按 F10 保存可能不生效，Ctrl+C 也可能直接退出，**实测按 Esc 取消键即可生效**
5. 按 **H** 显示/隐藏用户线程，**F5** 树状视图更清晰；自定义线程名显示为粗体蓝色

命令行验证：
```bash
ps -T -p <PID> -o pid,tid,comm,cmd
cat /proc/<PID>/task/<TID>/comm
```

工具族：htop、atop、btop（本笔记以 htop 为主）。

## references

- `references/CPU资源查询工具.md` —— 源笔记（含给 AI 话术的原始出处）
- `references/程序资源区分查询工具及方法/` —— htop 设置全过程截图 + PID/TID 与资源调度详解（含 ChatGPT 对话全文）
