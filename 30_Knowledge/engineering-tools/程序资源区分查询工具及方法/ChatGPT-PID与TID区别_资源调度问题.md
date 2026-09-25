# PID与TID区别

#### You:
一般pid就是代表进程,进程就是一个以文件为单位的程序是吗,然后tid就是线程,线程就是进程里面对进程里面的文件的程序里面内含细化的一个个对有内存需求,有运算需求的程序化的计算方程式子是吗

#### ChatGPT:
你的理解**抓到了 PID/TID 的层级关系，但“文件”和“程序化计算方程式”这两个比喻不太准确**。可以这样理解：

### 1. PID = Process ID，进程的编号

**进程（Process）≈ 一个正在运行的程序实例。**

比如你打开 Chrome：

```text
Chrome 程序文件
      ↓ 启动
一个 Chrome 进程
      ↓
PID = 1234
```

所以：

> **PID 不是代表文件，而是代表一个正在运行的进程。**

程序文件可以理解成“**程序的静态代码**”，进程则是“**这个程序已经被操作系统加载并运行起来的实例**”。

---

### 2. TID = Thread ID，线程的编号

一个进程里面通常可以有**多个线程**：

```text
进程 PID 1234
│
├── 线程 TID 1234
├── 线程 TID 1235
├── 线程 TID 1236
└── 线程 TID 1237
```

线程是**操作系统实际调度 CPU 执行的一条执行流**。

你说的“有内存需求、有运算需求的一个个程序化计算方程式”，可以稍微修正成：

> **线程 = 进程内部负责执行具体任务的一条执行路线。**

例如一个程序同时做：

```text
进程
├── 线程A：处理用户界面
├── 线程B：读取文件
├── 线程C：进行计算
└── 线程D：网络通信
```

这些线程**共享同一个进程的大部分资源**，尤其是内存空间、打开的文件等，但每个线程有自己的执行状态、寄存器和栈。

---

### 3. 你可以用这个关系记

```text
程序文件
   ↓ 运行
进程（Process）
   │
   ├── 线程（Thread）
   ├── 线程（Thread）
   └── 线程（Thread）
```

对应：

```text
PID → 进程的身份证
TID → 线程的身份证
```

**最关键的一点：**

> **进程是“资源/运行环境的容器”，线程是“真正执行代码的执行流”。**

所以以后你在看 `htop`、Perfetto、Chrome Tracing 之类的东西时，可以先形成这个概念：

**PID 看“哪个程序/进程”，TID 看“这个程序里面具体哪条执行流”。**


#### You:
线程的数量能通过我写代码的时候通过控制写的定义的函数,定义的类,引用的类和函数等来具体的去控制线程的名称和具体的数量吗,我记得线程号和进程号是由系统内核去自动分配的,还有线程名是直接去继承进程的名称,

#### ChatGPT:
对，你这次的理解已经比较接近了，但要把 **“线程数量、线程号、线程名”** 三件事分开。

### ① 线程数量：程序员可以控制

你写代码时可以主动创建线程：

```text
一个进程 PID=1000
│
├── TID=1000  主线程
├── TID=1001  线程A
├── TID=1002  线程B
└── TID=1003  线程C
```

例如你调用：

```python
threading.Thread(...)
```

每调用一次并启动，就可能产生一个新的线程。

所以：

> **线程“做多少个”主要由程序设计决定。**

函数、类、本身**不会自动等于线程**。只有你使用线程机制创建/启动线程，它才会成为线程。

---

### ② 线程号 TID：系统自动分配

这个你记得是对的。

你一般不会自己指定：

```text
TID = 12345
```

而是：

```text
程序创建线程
      ↓
操作系统内核
      ↓
分配 TID
```

所以：

> **PID/TID 是操作系统负责分配和管理的标识符。**

---

### ③ 线程名：可以由程序员设置

这个和 TID 不一样。

你可以给线程起一个有意义的名字，例如：

```text
PID 1000：MyProgram

TID 1001：DataLoader
TID 1002：Calculator
TID 1003：NetworkWorker
```

这样你在调试工具、性能分析工具里就更容易知道：

> “这个线程到底是干什么的？”

---

### ④ “线程名继承进程名”--不能简单这么说

这里需要纠正一下。

**线程默认名称在不同操作系统/语言运行时中有不同规则**，并不是简单地“线程直接继承进程名称”。

而且要区分：

```text
进程名称 ≠ PID

线程名称 ≠ TID
```

它们是不同东西：

| 东西  | 谁负责     | 作用     |
| --- | ------- | ------ |
| PID | 系统      | 标识进程   |
| TID | 系统      | 标识线程   |
| 进程名 | 程序/系统等  | 方便识别进程 |
| 线程名 | 程序/运行时等 | 方便识别线程 |

---

### 你可以最终记成这一张图

```text
程序
 ↓ 启动
进程
│
│ PID ← 内核分配
│
├── 主线程
│    └── TID ← 内核分配
│
├── 工作线程A
│    └── TID ← 内核分配
│
├── 工作线程B
│    └── TID ← 内核分配
│
└── 工作线程C
     └── TID ← 内核分配
```

而程序员主要控制的是：

**“我要创建多少线程、每个线程执行什么任务、给它叫什么名字、什么时候启动/结束。”**

**内核主要负责：**

**“给它编号、调度它什么时候获得 CPU、管理它的运行状态和资源。”**

这也正好解释了你之前问的 **Perfetto/Chrome Tracing**：它们经常可以沿着 **PID → TID → 具体线程执行的任务** 这条关系，把一个程序内部到底是谁在耗 CPU、谁在等待、谁在计算显示出来。


#### You:
你给我总结一个代码范式,教我命名线程名,大概用这个范式教我使用线程机制创建/启动线程,线程机制是什么,如何使用

#### ChatGPT:
可以。你现在先不要管太多底层细节，**把 Python 线程机制先记成一个固定范式**就够了。

## 一、线程机制到底是什么？

简单说：

> **线程机制 = 让一个进程内部同时存在多条“执行路线”。**

例如：

```text
一个 Python 进程
│
├── 主线程：main
│
├── 工作线程：data_worker
│
├── 工作线程：compute_worker
│
└── 工作线程：network_worker
```

每条线程都可以执行不同的函数。

---

# 二、最基本的代码范式

Python 使用 `threading` 模块：

```python
import threading

def worker():
    print("线程正在工作")


# 创建线程
t = threading.Thread(
    target=worker,
    name="MyWorker"
)

# 启动线程
t.start()

# 等待线程执行结束
t.join()
```

你先把这个范式记住：

```text
定义函数
   ↓
Thread(target=函数, name="线程名")
   ↓
创建线程对象
   ↓
start()
   ↓
线程真正开始运行
   ↓
join()
   ↓
等待线程结束
```

---

# 三、线程名怎么命名？

核心就是：

```python
threading.Thread(
    target=worker,
    name="DataLoader"
)
```

这里：

```text
target = 这个线程要执行什么
name   = 这个线程叫什么
```

例如：

```python
threading.Thread(
    target=load_data,
    name="DataLoader"
)

threading.Thread(
    target=calculate,
    name="Calculator"
)

threading.Thread(
    target=network_request,
    name="NetworkWorker"
)
```

这样你以后在 **Perfetto、调试器、日志**里看到：

```text
DataLoader
Calculator
NetworkWorker
```

就比看到：

```text
Thread-1
Thread-2
Thread-3
```

容易理解得多。

---

# 四、创建多个线程

这才是线程机制真正有意思的地方。

```python
import threading
import time


def download():
    print("下载任务开始")
    time.sleep(2)
    print("下载任务结束")


def calculate():
    print("计算任务开始")
    time.sleep(2)
    print("计算任务结束")


def save():
    print("保存任务开始")
    time.sleep(2)
    print("保存任务结束")


t1 = threading.Thread(
    target=download,
    name="DownloadWorker"
)

t2 = threading.Thread(
    target=calculate,
    name="CalculateWorker"
)

t3 = threading.Thread(
    target=save,
    name="SaveWorker"
)


t1.start()
t2.start()
t3.start()


t1.join()
t2.join()
t3.join()
```

这里实际上就是：

```text
PID = 一个 Python 进程
│
├── 主线程
│
├── TID → DownloadWorker
├── TID → CalculateWorker
└── TID → SaveWorker
```

注意：

**你没有指定 TID。**

你只指定：

```python
name="DownloadWorker"
```

而：

```text
TID
 ↓
操作系统自动分配
```

---

# 五、最容易犯的错误：`start()` 和 `run()`

这个非常重要。

### 正确：

```python
t.start()
```

### 不要把它理解成：

```python
t.run()
```

因为：

```python
t.start()
```

的含义是：

> **告诉线程机制：启动一条新的线程来执行 target。**

而直接：

```python
t.run()
```

本质上只是**在当前线程里调用这个函数**，并不会按照你想象的方式创建新的执行线程。

所以记住：

```text
Thread(...)
   ↓
创建线程对象

start()
   ↓
真正启动线程
```

---

# 六、如果函数需要参数

可以这样：

```python
import threading


def worker(name, number):
    print(name, number)


t = threading.Thread(
    target=worker,
    name="MyWorker",
    args=("Alice", 100)
)

t.start()
t.join()
```

这里：

```python
target=worker
```

表示：

> 我要这个线程执行 `worker`

而：

```python
args=("Alice", 100)
```

表示：

> 调用 `worker("Alice", 100)`

---

# 七、你可以形成一个固定“线程模板”

以后你自己写代码时，直接套这个：

```python
import threading


# ① 定义线程任务
def worker():
    # 线程具体要做的事情
    pass


# ② 创建线程
thread = threading.Thread(
    target=worker,
    name="Worker"
)


# ③ 启动线程
thread.start()


# ④ 等待线程结束
thread.join()
```

如果多个线程：

```python
threads = []

for i in range(5):

    thread = threading.Thread(
        target=worker,
        name=f"Worker-{i}"
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
```

这样就可以创建：

```text
Worker-0
Worker-1
Worker-2
Worker-3
Worker-4
```

对应操作系统会给它们分配不同的 TID。

---

## 最后给你一个最重要的关系图

```text
                 一个进程 PID
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Thread       Thread      Thread
          │           │           │
       TID系统分配   TID系统分配   TID系统分配
          │           │           │
       名称可设置    名称可设置    名称可设置
          │           │           │
       执行函数A     执行函数B     执行函数C
```

所以你可以把 Python 的线程机制浓缩成 **4 个关键词**：

> **定义任务 → 创建 Thread → `start()` 启动 → `join()` 等待**

其中：

> **`target` 决定“干什么”，`name` 决定“叫什么”，TID 决定“系统怎么编号”。**


#### You:
C++也是可以指定线程名称的是吗,在公司项目上面是否经常有人这么干,方便运维,

#### ChatGPT:
是的，**C++ 也可以给线程设置名称**，而且在实际工程中这是比较常见的做法，尤其是**中大型项目、服务端程序、性能分析和运维场景**。

不过有一个细节：C++ 标准库里的 `std::thread` **本身没有统一的标准 API 来设置线程名**，通常要调用操作系统 API，或者使用项目使用的线程库。

例如 Linux 下常见的是：

```cpp
#include <pthread.h>
#include <thread>

void worker()
{
    // ...
}

int main()
{
    std::thread t(worker);

    pthread_setname_np(t.native_handle(), "DataWorker");

    t.join();
}
```

这样系统里就可能看到：

```text
PID  1234
│
├── TID 1234  main
├── TID 1235  DataWorker
├── TID 1236  ComputeWorker
└── TID 1237  NetworkWorker
```

### 公司项目为什么喜欢这么做？

因为排查问题的时候非常有价值。

假设一个程序有 30 个线程：

```text
Thread-1
Thread-2
Thread-3
...
Thread-30
```

你看到 CPU 飙高、线程阻塞的时候，很难马上知道是谁。

如果命名成：

```text
Main
NetworkIO
DataLoader
Inference
Database
Logger
Monitor
```

那么在：

- `htop`
- `top`
- `gdb`
- Perfetto
- Linux `/proc`
- 各种性能分析工具
- 日志和监控系统

里面看到线程名，就能**直接判断这个线程负责什么**。

尤其是你之前问的 **Perfetto**，线程名在这种性能分析里特别有用：

```text
PID: AI_Server

TID       Thread Name       CPU
101       Main              2%
102       DataLoader       15%
103       Inference        78%  ← 一眼发现
104       Logger            1%
```

所以你可以把它理解成：

> **线程名不是为了让程序运行得更快，而是为了让“人”更容易理解和维护程序。**

而且工程上通常会形成比较规范的命名，例如：

```text
IOWorker
NetworkWorker
ComputeWorker
DatabaseWorker
InferenceWorker
RenderThread
```

而不是随便叫 `aaa`、`thread1`。

**所以你的“方便运维”这个理解是对的，不过更准确地说，是方便开发、调试、性能分析和运维共同排查问题。**


#### You:
在这里面就是没有指定线程名称的是吗,我记得他连线程库threading都没有引入,那他是怎么建立并且去执行线程的,是py的解释器本身就内置了一个类是线程库的东西去建立和执行线程是吗,我记得很多人写代码都是没有import threading的

#### ChatGPT:
对，你记得的现象是对的：**很多 Python 项目里确实完全看不到 `import threading`，但程序依然可能存在大量线程。**

你上传的这个 `node.py` 就是一个很好的例子。它没有 `import threading`，但它使用了 **ROS 2 的 `rclpy`**，线程机制被 ROS 2 的执行器（Executor）这一层封装掉了。比如这里的订阅回调：

### 关键区别：不是“Python 解释器自动给你创建线程”

更准确地说，是：

```text
你的 Python 代码
       ↓
调用某个框架/库
       ↓
框架内部创建和管理线程
       ↓
操作系统创建线程
```

而不是：

```text
Python解释器
    ↓
看到一个函数
    ↓
自动给函数创建线程
```

**普通 Python 函数不会自动变成线程。**

---

### 你这个 ROS 2 程序就是这种情况

你的代码：

```python
self.create_subscription(
    Image,
    ...,
    self.image_callback,
    ...
)
```

你只是告诉 ROS：

> “以后收到 Image 消息的时候，请调用 `image_callback`。”

然后：

```python
rclpy.spin(node)
```

让 ROS 进入持续处理消息的状态。你的文件中就是这样启动的：

所以你没有写：

```python
threading.Thread(...)
```

并不意味着：

> “程序没有线程。”

而是：

> **线程管理被 ROS 2 封装了。**

---

### 你可以把 Python 线程来源分成 3 种

```text
① 自己创建
   ↓
import threading
threading.Thread(...)
```

```text
② 第三方库/框架创建
   ↓
ROS 2 / PyTorch / OpenCV / 网络库等
   ↓
内部帮你创建线程
```

```text
③ Python/运行时/底层原生库内部使用
   ↓
你甚至可能完全看不到线程创建代码
```

所以以后你看到一个项目：

```python
import threading
```

**只能说明这个文件直接使用了 Python 的 threading API。**

不能由此判断：

> “这个程序有没有线程。”

---

还有一个非常重要的概念：

**“使用线程” ≠ “必须自己写 `threading.Thread`”。**

就像你开车：

```text
自己造发动机 → 自己管理线程
使用汽车 → 框架/库替你管理线程
```

在公司项目里，后者其实非常常见。

你这个 ROS 2 项目就是典型的\*\*“应用代码不直接管理线程，而是把并发执行交给框架”\*\*的结构。


#### You:
我在使用ros2这个框架下面也是能指定进程名的是吗

#### ChatGPT:
可以，但这里要区分 **ROS 2 的 Node 名称** 和 **Linux 进程名称**。这两个不是一回事。

你这个代码里已经指定了一个 **ROS 2 Node 名称**：

```python
super().__init__('target_detection')
```

也就是 Node 叫：

```text
target_detection
```

但这**不等于 Linux 的进程名**。

---

### 你可以这样理解

```text
Linux 系统
│
└── 进程 PID = 12345
      │
      │ 进程名：可能是 python3
      │
      └── ROS 2 Node
             └── 名称：target_detection
```

所以你现在代码里的：

```python
super().__init__('target_detection')
```

主要是在告诉 **ROS 2**：

> “我创建的这个 Node 叫 `target_detection`。”

它不是在告诉 Linux：

> “把我的进程名字改成 target\_detection。”

---

### 那 ROS 2 能不能控制进程？

可以通过**启动方式、启动文件以及进程/执行器相关机制**进行管理，但这是另一层概念。

比如你的程序：

```text
node.py
   ↓
python3 node.py
   ↓
Linux 进程
   ↓
PID = 系统自动分配
   ↓
ROS 2 Node = target_detection
```

所以你以后看 ROS 2 系统时，建议脑子里始终分成三层：

```text
① Linux
   PID / TID / Process Name / Thread Name

② ROS 2
   Node / Topic / Service / Action

③ Python
   class / function / threading.Thread
```

它们之间有关联，但**不能把 ROS 2 Node 名称直接等同于 Linux 进程名**。

如果你愿意，我下一步可以直接结合你这个 `node.py`，给你画一张 **“ROS 2 Node → Executor → Callback → Thread → TID → PID”** 的完整关系图。


#### You:
线程名也是可以的是吗

#### ChatGPT:
对，**线程名也是可以指定的**。

不过和刚才一样，要分清是哪一层：

```text
Linux 线程
├── TID：内核自动分配
└── Thread Name：可以由程序/框架设置
```

在 ROS 2 中，如果你使用的是多线程执行器（`MultiThreadedExecutor`），ROS 2 会创建多个执行线程。**线程本身可以有名字**，但你通常不是通过：

```python
self.create_subscription(...)
```

这种 API 直接指定线程名。

而是由 **ROS 2 / Python / 底层线程库**来管理线程。

所以你可以记成：

> **PID/TID：系统分配；进程名/线程名：程序或框架可以设置。**

而你现在这个 `node.py` 里：

```python
super().__init__('target_detection')
```

指定的是 **ROS 2 Node 名称**，不是线程名。

如果你后面用 Perfetto 分析这个 ROS 2 程序，那么你会看到类似：

```text
PID
└── ROS 2 Node: target_detection
     │
     ├── TID → 某个执行线程
     ├── TID → 某个执行线程
     └── TID → 某个执行线程
```

这几个概念一定要分开。


#### You:
所以在ros2里面指定的Node名称就是只是用于在ros2这个框架下面的话题服务,动作之间的通讯是吗,我想让AI帮我写代码,你觉得要怎么和AI说让他在写的过程中去指定线程名称,直接告诉他就好了是吗

#### ChatGPT:
对，**你的第一句话基本可以这么理解，但稍微扩大一点**。

### 1. ROS 2 的 Node 名称是 ROS 2 层面的身份

比如你代码里的：

```python
super().__init__('target_detection')
```

表示这个 ROS 2 节点叫 `target_detection`。

它主要用于 ROS 2 的资源组织和通信体系，比如：

```text
ROS 2
│
├── Node: target_detection
│      │
│      ├── Topic
│      ├── Service
│      └── Action
│
└── Node: camera
       │
       └── Topic
```

但**Node 名称 ≠ Linux 进程名 ≠ 线程名**。

---

## 2. 让 AI 写代码时，直接告诉它就可以

而且我建议你**不要只说一句“给线程命名”**，最好把要求说完整一点。

例如你让 AI 写 ROS 2 Python 代码，可以直接这样说：

:::writing{variant="chat\_message" id="58321" title="给 AI 的线程命名要求"}
请在这个 ROS 2 Python 项目中使用多线程执行时，为创建的每个工作线程设置明确、有意义的线程名称。

要求：

1. 不要使用默认的 Thread-1、Thread-2 之类的名称。
2. 根据线程实际负责的功能命名，例如 ImageProcessing、InferenceWorker、NetworkWorker、DataLoader。
3. 如果使用 ROS 2 MultiThreadedExecutor，请同时考虑 Executor 创建的线程，并尽可能让线程名称能够在 Linux、htop、Perfetto 等工具中识别。
4. PID 和 TID 不需要我手动指定，由操作系统自动分配。
5. ROS 2 Node 名称、Linux 进程名称和线程名称要区分开，不要混为一谈。
6. 在代码中明确说明线程是在哪里创建、在哪里启动，以及线程名称是在哪里设置的。
   :::

这样 AI 就不会只给你：

```python
threading.Thread(target=worker)
```

而会意识到你要求的是**工程级的可观测性**。

---

### 3. 如果是公司项目，我甚至建议你这样要求 AI

> **“所有长期运行的线程都必须设置具有业务含义的线程名，方便使用 htop、gdb、Perfetto 等工具进行定位和性能分析。”**

这句话非常实用。

比如你的视觉程序以后可能有：

```text
Main
ImageCallback
InferenceWorker
DepthWorker
TFWorker
Publisher
```

你看到 Perfetto：

```text
PID 8231
 ├─ TID 8232  Main
 ├─ TID 8233  ImageCallback
 ├─ TID 8234  InferenceWorker
 └─ TID 8235  Publisher
```

就能马上知道**哪条执行流在干什么**。

不过还有一个重要细节：**如果线程是 ROS 2 Executor 内部创建的，你不能简单要求 AI“给 `threading.Thread` 加 name”**。因为这些线程不是你直接创建的，而是 ROS 2/rclpy 创建的。此时应该要求 AI **研究当前 ROS 2 版本支持的 Executor/底层线程命名方式，并实际验证 Linux 下是否能看到这些名称**。

这也是为什么你以后给 AI 下这种工程任务时，最好说：

> **“不要只实现功能，要考虑线程可观测性，并验证线程名能否在 Linux/Perfetto 中实际显示。”**

这样比单纯说“给线程命名”靠谱得多。


#### You:
我一般是使用ros2的humble版本

#### ChatGPT:
那就更好办了。你如果**主要使用 ROS 2 Humble**，以后让 AI 写 ROS 2 代码时，可以把版本明确告诉它，因为 **Humble 的 `rclpy` / Executor 行为和其他 ROS 2 发行版可能存在差异**。

尤其是你现在关注的 **PID / TID / Node 名称 / Thread Name / Perfetto**，我建议你以后给 AI 的要求写成：

> **ROS 2 Humble + Ubuntu/Linux 环境。涉及多线程时，明确区分 ROS 2 Node 名称、Linux 进程名、Linux 线程名和 TID。凡是程序自己创建的线程，都设置有业务含义的线程名称；凡是 ROS 2 Executor 内部创建的线程，要使用 Humble 实际支持的方式进行命名，并验证线程名是否能在 Linux/Perfetto 中看到。不要假设 ROS 2 Node 名称就是线程名或进程名。**

这样 AI 在给你写代码时，就会按照 **Humble 的实际机制**来考虑，而不是拿新版本 ROS 2 的 API 硬套。

另外，你这个 `node.py` 目前使用的是：

```python
rclpy.spin(node)
```

这属于 ROS 2 的执行器机制。**如果你以后需要自己控制线程数量和线程名称，重点就应该研究 `Executor`，尤其是 `MultiThreadedExecutor`，而不是只研究 Python 的 `threading`。**

你可以把它们理解成：

```text
Python threading
      ↓
我自己创建线程
      ↓
我自己控制线程名/生命周期

ROS 2 Executor
      ↓
ROS 2 帮我调度 Callback
      ↓
Executor 管理执行线程
```

对于你这种 ROS 2 视觉节点，我会更推荐你**优先理解 Executor → Callback → Thread 这条链路**，这样以后看 Perfetto 的 TID 才真正能对应回你的 ROS 2 代码。


#### You:
进程的命名也是通过这个框架能指定是吗

#### ChatGPT:
可以，但这里我帮你把这个概念再卡准一点：

**ROS 2 Humble 可以管理和启动“进程”，但 ROS 2 Node 名称本身不是进程名称。**

例如你现在这个程序：

```text
Linux
└── PID 12345
     └── python3 node.py
          └── ROS 2 Node
               └── target_detection
```

你的代码：

```python
super().__init__('target_detection')
```

指定的是：

> **ROS 2 Node 名称 = `target_detection`**

而不是：

> **Linux Process Name = `target_detection`**

---

### 那 ROS 2 能不能指定进程名？

**可以通过 ROS 2 的启动/进程管理体系配合 Linux 的进程命名机制实现，但不是 `Node()` 的那个名字直接控制。**

所以你以后让 AI 写代码时，最好明确说：

> **“我使用 ROS 2 Humble + Ubuntu，请分别设置 ROS 2 Node 名称、Linux Process Name 和 Thread Name，并确保三者不要混淆；对于进程名和线程名，请使用 Humble/Linux 实际支持的机制。”**

这样 AI 才不会写成：

```python
Node("xxx")
```

然后告诉你：

> “进程名称已经设置成 xxx。”

这是不准确的。

你现在可以把整个体系记成：

```text
Linux层
│
├── Process
│    ├── PID ← 内核分配
│    └── Process Name ← 可以设置
│
└── Thread
     ├── TID ← 内核分配
     └── Thread Name ← 可以设置


ROS 2层
│
└── Node
     └── Node Name ← 例如 target_detection
```

**四个名字/编号不要混在一起：PID、进程名、TID、线程名、Node 名。**

尤其你后面要用 **Perfetto 看 ROS 2 性能**，把这几个层级分清楚非常重要。
