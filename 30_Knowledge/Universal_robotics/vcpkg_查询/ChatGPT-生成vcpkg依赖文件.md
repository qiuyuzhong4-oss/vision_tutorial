# 生成vcpkg依赖文件

#### You:
这个是我需要安装的依赖在ros2或者是vcpkg体系里面有没有工具帮我把他转化成vcpkg安装的json文件,

#### ChatGPT:
有，而且你这个项目其实**非常适合从现有的 `CMakeLists.txt` + README 依赖列表整理成 vcpkg manifest (`vcpkg.json`)**。

不过需要先区分一件事：

### 1. ROS2 本身没有一个“一键转 vcpkg.json”的工具

因为两套体系管理的东西不完全一样：

- ROS2：`rosdep` / `apt` / ROS package
- vcpkg：C/C++ 第三方库

你这个项目 README 里列出的依赖，例如：

```text
OpenCV
fmt
Eigen
spdlog
yaml-cpp
nlohmann-json
Ceres
```

这些属于比较典型的 **C/C++ 第三方依赖**，很适合交给 vcpkg 管理。README 中也确实把它们列在 `apt install` / 第三方 SDK 安装部分。

而你的 `CMakeLists.txt` 也明确验证了其中几个：

```cmake
find_package(OpenCV REQUIRED)
find_package(fmt REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(spdlog REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(OpenVINO REQUIRED)
```

---

### 2. vcpkg 本身可以帮你生成 `vcpkg.json`

如果你现在就在这个项目目录：

```bash
cd /home/liantian/projects/sp_vision_25
```

可以使用：

```bash
vcpkg add port fmt
```

它会自动修改/创建：

```text
vcpkg.json
```

然后继续：

```bash
vcpkg add port opencv4
vcpkg add port eigen3
vcpkg add port spdlog
vcpkg add port yaml-cpp
vcpkg add port nlohmann-json
vcpkg add port ceres
```

最后：

```bash
vcpkg install
```

不过你前面已经遇到过 **manifest mode**，所以你现在这个项目本身如果已经有 `vcpkg.json`，更推荐直接编辑这个文件，而不是：

```bash
vcpkg install fmt
```

因为 manifest 模式下，依赖应该写进 `vcpkg.json`，然后统一：

```bash
vcpkg install
```

---

### 3. 你这个项目我可以直接帮你整理

根据你给我的两个文件，目前可以得到一个比较明确的候选列表：

| 项目             | vcpkg 是否适合           |
| -------------- | -------------------- |
| OpenCV         | ✅                    |
| fmt            | ✅                    |
| Eigen3         | ✅                    |
| spdlog         | ✅                    |
| yaml-cpp       | ✅                    |
| nlohmann-json  | ✅                    |
| Ceres          | ✅                    |
| OpenVINO       | ⚠️ 需要单独确认            |
| HikRobot SDK   | ❌ 不属于普通 vcpkg 依赖     |
| MindVision SDK | ❌                    |
| ROS2           | ❌ 不应该塞进这个 vcpkg.json |
| g++            | ❌ 系统工具链              |
| cmake          | ❌ 系统工具               |
| can-utils      | ❌ 系统工具               |
| openssh-server | ❌ 系统软件               |
| screen         | ❌ 系统软件               |

也就是说，**不能把 README 里的 `apt install` 一股脑全部转换成 vcpkg**。

更合理的架构是：

```text
Ubuntu
│
├── apt
│   ├── gcc/g++
│   ├── cmake
│   ├── can-utils
│   ├── openssh-server
│   └── screen
│
├── ROS2
│   └── rclcpp / std_msgs / ...
│
├── vcpkg
│   ├── opencv4
│   ├── fmt
│   ├── eigen3
│   ├── spdlog
│   ├── yaml-cpp
│   ├── nlohmann-json
│   └── ceres
│
└── 厂商 SDK
    ├── HikRobot SDK
    └── MindVision SDK
```

而且你这个项目的 CMake 已经做了一个很好的区分：ROS2 是**可选的**，只有检测到 `ament_cmake/rclcpp/std_msgs/...` 后才编译 ROS2 相关程序。

**所以你的目标最好不是“把所有依赖转换成 vcpkg”，而是把 C++ 第三方库这一层转换成 `vcpkg.json`。**

如果你愿意，我可以直接根据你这份 **README + CMakeLists.txt**，给你整理出一份可以直接放进项目里的完整 `vcpkg.json`，并把 **哪些依赖由 vcpkg 管、哪些由 apt 管、哪些必须手动装** 一起对应好。


#### You:
我的意思是在我的cmakelist.txt文件里面不是已经写好需要安装什么库了吗,能不能直接通过这个映射直接改vcpkg.json文件

#### ChatGPT:
对，你这个理解是对的。**你问的是：能不能让工具直接分析 `CMakeLists.txt` 里的 `find_package(...)`，然后自动映射成 vcpkg 的 package 名称，生成/修改 `vcpkg.json`。**

答案是：

**可以做到“半自动”，但 vcpkg 本身没有一个通用命令可以直接 `CMakeLists.txt → vcpkg.json`。**

你这个项目尤其适合自己做一个小脚本，因为你的 CMake 里已经把主要依赖写得很清楚：

```cmake
find_package(OpenCV REQUIRED)
find_package(fmt REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(spdlog REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(OpenVINO REQUIRED)
```

例如可以建立这样的映射：

```text
CMakeLists.txt              vcpkg
────────────────────────────────────
find_package(OpenCV)   →    opencv4
find_package(fmt)      →    fmt
find_package(Eigen3)   →    eigen3
find_package(spdlog)   →    spdlog
find_package(yaml-cpp) →    yaml-cpp
find_package(nlohmann_json)
                       →    nlohmann-json
find_package(Ceres)    →    ceres
```

然后自动生成：

```json
{
  "dependencies": [
    "opencv4",
    "fmt",
    "eigen3",
    "spdlog",
    "yaml-cpp",
    "nlohmann-json",
    "ceres"
  ]
}
```

### 但这里有一个关键问题

**`find_package()` 的名字和 vcpkg port 名称并不保证一一对应。**

例如：

```cmake
find_package(Eigen3)
```

对应：

```json
"eigen3"
```

比较直接。

但有些库可能是：

```cmake
find_package(OpenCV)
```

对应：

```json
"opencv4"
```

所以不能简单地把：

```cmake
find_package(XXX)
```

机械地变成：

```json
"XXX"
```

需要一个**映射表**。

---

### 你这个项目可以进一步自动化

实际上可以做成：

```text
CMakeLists.txt
      │
      ▼
提取所有 find_package()
      │
      ▼
CMake package name
      │
      ▼
vcpkg package 映射表
      │
      ▼
自动生成/更新 vcpkg.json
```

例如你运行：

```bash
python3 cmake_to_vcpkg.py
```

它自动读取当前目录：

```text
CMakeLists.txt
```

发现：

```text
OpenCV
fmt
Eigen3
spdlog
yaml-cpp
nlohmann_json
OpenVINO
```

然后生成：

```text
vcpkg.json
```

同时它还可以把：

```text
OpenVINO
```

这种**暂时不能直接按普通 vcpkg dependency 处理的东西**列出来提醒你，而不是错误地塞进 JSON。

---

所以如果你的问题是：

> **“我已经在 CMakeLists.txt 里面写了依赖，为什么还要我再手动把依赖一个个写进 vcpkg.json？有没有办法直接从 CMakeLists.txt 映射过去？”**

**有办法，而且很适合写一个几十行的小工具自动完成。**

而且你现在这个 `sp_vision_25` 项目正好可以拿来做这个工具的第一次测试。你给我的 `CMakeLists.txt` 已经足够作为输入源。


#### You:
我发现使用vcpkg来管理安装C++库他是直接在我vcpkg的pakage文件夹里面放置的,如果说我需要不同版本的同名C++库,那么他也是直接放在我这个pakage文件夹里面,然后为了防止这个同名冲突,同名的版本号后缀不同是吗

#### ChatGPT:
你的理解有一部分是对的，但**vcpkg 管理不同版本的同名 C++ 库，并不是简单地给同名库添加不同版本号后缀，然后全部放在 `packages` 文件夹里。**

需要区分几个目录和概念。

### 1. `packages` 文件夹是干什么的？

假设你的 vcpkg 位于：

```text
/home/liantian/vcpkg/
```

里面可能有：

```text
vcpkg/
├── packages/
├── installed/
├── buildtrees/
├── downloads/
└── ports/
```

其中：

| 目录            | 作用                      |
| ------------- | ----------------------- |
| `packages/`   | 存放构建后、准备安装的临时打包内容       |
| `installed/`  | 存放实际安装好的库、头文件、CMake 配置等 |
| `buildtrees/` | 存放库的构建过程文件              |
| `downloads/`  | 存放下载的源码压缩包等             |
| `ports/`      | 存放各个库的构建配方              |

**你最终编译项目时，主要使用的是 `installed/` 里面的库，而不是 `packages/`。**

---

### 2. 如果安装不同版本的同名库，会怎样？

例如你需要：

```text
fmt 10.x
fmt 11.x
```

vcpkg 的普通版本管理机制不是：

```text
packages/
├── fmt-10
└── fmt-11
```

而是通过 **版本约束（versioning）和依赖基线（baseline）** 来确定项目使用哪个版本。

例如在 `vcpkg.json` 中：

```json
{
  "dependencies": [
    {
      "name": "fmt",
      "version>=": "10.2.1"
    }
  ]
}
```

这表示项目要求 `fmt` 至少达到某个版本。

但是，**同一个 vcpkg 安装实例、同一个 triplet 下，通常不能同时安装两个不同版本的同名库，并让它们都作为普通 `fmt` 被使用。**

因为它们可能都包含：

```text
include/fmt/format.h
lib/fmt.lib
```

或者 Linux 下的：

```text
lib/libfmt.so
```

文件路径会发生冲突。

---

### 3. 那么 vcpkg 如何让不同项目使用不同版本？

这是 vcpkg 比较重要的设计。

假设你有两个项目：

```text
项目A：需要 fmt 10.x
项目B：需要 fmt 11.x
```

可以使用不同的 vcpkg 环境或不同的版本配置：

```text
vcpkg/
├── 项目A环境
│   └── fmt 10.x
│
└── 项目B环境
    └── fmt 11.x
```

或者使用不同的 vcpkg 实例：

```text
/home/liantian/vcpkg_old/
/home/liantian/vcpkg_new/
```

分别管理不同版本。

需要注意，vcpkg 的版本选择还涉及注册表、版本数据库和 manifest 配置，不能仅靠复制文件夹来实现完整的版本隔离。

---

### 4. 对你现在的项目有什么影响？

你现在的目标是：

```text
自己的电脑
    │
    ├── vcpkg
    │    ├── OpenCV
    │    ├── fmt
    │    ├── Eigen
    │    └── yaml-cpp
    │
    └── sp_vision_25
```

然后把环境部署到工控机。

这里建议你记住：

> **vcpkg 的核心不是简单地把所有库放在一个文件夹里，而是通过 manifest、版本约束、triplet 和安装目录来管理项目依赖。**

如果你希望不同项目使用不同版本的同名库，应该优先考虑项目级依赖配置和隔离环境，而不是手动修改库文件夹名称。


#### You:
![image](data:image/png;base64,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)
![image](data:image/png;base64,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)
两个回答我都不喜欢,我的意思是在我vcpkg源码里面不是有一个pakage的文件夹来存放我使用cmake的时候根据vcpkg.json来安装的包的源码的吗还是说你的意思是这些包的源码是放在这个vcpkg_installed里面的,这个里面放的不是应该只是一个引用吗,

#### ChatGPT:
对，你这次问的这个点我明白了。**你说的 `vcpkg/packages` 确实是 vcpkg 源码目录里的一个重要目录，但我上一条把它的作用说得不准确。**

你现在看到的两个位置，其实是**完全不同层次的东西**：

```text
~/vcpkg/packages/
```

和

```text
你的项目/
└── build/
    └── vcpkg_installed/
```

### 先直接回答你的核心问题

**不是 `vcpkg_installed` 里面只是一个“引用”。**

`vcpkg_installed` 是这个项目实际使用的**已安装库文件**。

而：

```text
~/vcpkg/packages/
```

主要是 vcpkg 在构建过程中产生的**打包/暂存目录**，也不是“源码仓库”。

真正下载下来的源码，主要涉及：

```text
~/vcpkg/downloads/
~/vcpkg/buildtrees/
```

所以可以把整个过程理解成：

```text
                 vcpkg 源码仓库
                       │
                       │ vcpkg install
                       ▼
              ┌─────────────────┐
              │    downloads/   │ ← 下载的源码压缩包等
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   buildtrees/   │ ← 解压、编译、构建过程
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    packages/    │ ← 构建完成后的“暂存/打包”结果
              └────────┬────────┘
                       │
                       ▼
              ┌──────────────────────┐
              │   vcpkg_installed/  │ ← 项目真正使用的安装结果
              │                      │
              │ include/             │
              │ lib/                │
              │ bin/                │
              │ share/              │
              │ ...
              └──────────────────────┘
```

---

## 你第二张图尤其容易产生误解

你现在这个：

```text
sp_vision_25/
└── build/
    └── vcpkg_installed/
        └── vcpkg/
            ├── info/
            ├── manifest-info.json
            ├── updates/
            └── vcpkg-running.lock
```

**这个 `vcpkg_installed/vcpkg` 本身不是库文件所在的位置。**

你应该再往上/旁边看看有没有类似：

```text
build/vcpkg_installed/
└── x64-linux/
    ├── include/
    ├── lib/
    ├── bin/
    ├── share/
    └── ...
```

如果你的 triplet 是 `x64-linux`，真正的库通常就在：

```text
build/vcpkg_installed/x64-linux/
```

例如：

```text
build/vcpkg_installed/x64-linux/include/fmt/
build/vcpkg_installed/x64-linux/include/opencv4/
build/vcpkg_installed/x64-linux/lib/
```

这些才是**你的项目编译时真正拿来用的文件**。

---

## 那 `packages` 到底是什么？

假设你安装：

```bash
vcpkg install fmt
```

vcpkg 会经历类似：

```text
下载 fmt 源码
      ↓
buildtrees/fmt-xxx/
      ↓
编译
      ↓
packages/fmt_x64-linux/
      ↓
安装到
vcpkg_installed/x64-linux/
```

所以：

### `buildtrees`

偏向：

> **“我怎么把这个库编译出来？”**

里面可以看到源码解压、CMake 构建、编译日志等等。

### `packages`

偏向：

> **“我刚刚编译出来的这个库，整理成一个待安装的包是什么样？”**

例如里面可能有：

```text
packages/fmt_x64-linux/
├── include/
├── lib/
├── share/
└── ...
```

### `vcpkg_installed`

偏向：

> **“这个项目最终实际安装并使用的库是什么？”**

所以你说的：

> “`vcpkg_installed` 里面放的不是应该只是一个引用吗？”

**不是。**

它不是类似：

```text
fmt → /home/liantian/vcpkg/packages/xxx
```

这样的软链接/引用关系。

而是**实际的头文件、`.a`、`.so`、CMake 配置文件等已经安装进去的结果**。

---

### 你可以自己马上验证

在你的项目里面：

```bash
find build/vcpkg_installed -name "format.h"
```

如果安装了 fmt，应该能找到类似：

```text
build/vcpkg_installed/x64-linux/include/fmt/format.h
```

再看看：

```bash
find build/vcpkg_installed -name "libfmt*"
```

你会看到实际的库文件。

所以你现在这个项目的 **manifest 模式**实际上形成了一个很有意思的结构：

```text
~/vcpkg/
    ↓
vcpkg 本体 + 下载/构建缓存

sp_vision_25/
├── vcpkg.json
└── build/
    └── vcpkg_installed/
         ↓
    这个项目自己的依赖安装结果
```

这也是为什么你之前问的\*\*“能不能把项目 + vcpkg 环境一起搬到工控机”\*\*这个问题，答案需要重新细分：**项目的 `vcpkg_installed` 和你 `~/vcpkg` 里的 `packages`、`buildtrees`、`downloads`，作用并不一样。**
