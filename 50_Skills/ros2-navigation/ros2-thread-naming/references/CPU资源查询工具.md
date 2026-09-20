写代码时候的准备:指定进程和线程的名称



**如果线程是 ROS 2 Executor 内部创建的，你不能简单要求 AI“给 `threading.Thread` 加 name”**。因为这些线程不是你直接创建的，而是 ROS 2/rclpy 创建的。此时应该要求 AI **研究当前 ROS 2 版本支持的 Executor/底层线程命名方式，并实际验证 Linux 下是否能看到这些名称**。

这也是为什么你以后给 AI 下这种工程任务时，最好说：

> ### **“你在写代码的过程中要给进程和线程命名,我一般是使用ros2的humble版本,你给线程和进程命名的时候不要只实现功能，同时要考虑线程可观测性，并验证线程名能否在 Linux/Perfetto 中实际显示,我会使用htop来看具体的那个进程那个线程使用了多少资源。”**

尤其是你现在关注的 **PID / TID / Node 名称 / Thread Name / Perfetto**，我建议你以后给 AI 的要求写成：

> #### **ROS 2 Humble + Ubuntu/Linux 环境。涉及多线程时，明确区分 ROS 2 Node 名称、Linux 进程名、Linux 线程名和 TID。凡是程序自己创建的线程，都设置有业务含义的线程名称；凡是 ROS 2 Executor 内部创建的线程，要使用 Humble 实际支持的方式进行命名，并验证线程名是否能在 Linux/Perfetto 中看到。不要假设 ROS 2 Node 名称就是线程名或进程名。**

这样 AI 在给你写代码时，就会按照 **Humble 的实际机制**来考虑，而不是拿新版本 ROS 2 的 API 硬套。



加指定进程名**“我使用 ROS 2 Humble + Ubuntu，请分别设置 ROS 2 Node 名称、Linux Process Name 和 Thread Name，并确保三者不要混淆；对于进程名和线程名，请使用 Humble/Linux 实际支持的机制。”**







一些工具比如说:
htop,atop,btop

这里主要讲的是htop
