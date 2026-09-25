# 管理C++库安装位置

#### You:
那么我之前直接把C++的包安装到系统里面,是不会把包copy到项目的build目录里面的是吗,如果说我想管理之前安装在系统环境里面的C++库,那么这些库应该放在那里,

#### ChatGPT:
对，你这个理解是对的。

### 1. 直接安装到系统的 C++ 库，不会被复制到项目 `build/` 里

比如你执行：

```bash
sudo apt install libfmt-dev
```

或者 ROS/`rosdep` 最终通过 `apt` 安装依赖。

它通常会把库安装到**系统目录**，例如：

```text
/usr/include/          ← 头文件
/usr/lib/x86_64-linux-gnu/  ← .so / .a 库文件
/usr/lib/              ← 其他库文件
/usr/share/            ← CMake 配置、pkg-config 等
```

你的项目可能是：

```text
my_project/
├── src/
├── include/
├── CMakeLists.txt
└── build/
```

执行：

```bash
cmake ..
make
```

`build/` 主要放的是：

```text
build/
├── CMakeCache.txt
├── CMakeFiles/
├── Makefile
└── 你的可执行程序
```

它**不是系统第三方库的仓库**。

例如：

```text
/usr/lib/.../libfmt.so
        ↑
        │
        │ CMake/编译器链接
        │
build/my_program
```

而不是：

```text
build/
└── libfmt.so
```

---

### 2. 如果你想“管理”以前安装到系统里的 C++ 库

这里要分两种情况。

#### 情况 A：你用 apt 安装的

例如：

```bash
sudo apt install libfmt-dev
```

那么就让 **apt 管理**：

```bash
apt list --installed | grep fmt
```

删除：

```bash
sudo apt remove libfmt-dev
```

查看安装了哪些文件：

```bash
dpkg -L libfmt-dev
```

这种库的实际文件就应该待在：

```text
/usr/include
/usr/lib
/usr/share
```

**不要自己把它们搬到项目里。**

---

#### 情况 B：你用 vcpkg 管理

这时候库一般不再依赖系统 `/usr`，而是在你的 vcpkg 环境里。

比如：

```text
/home/liantian/vcpkg/
├── ports/
├── buildtrees/
├── packages/
└── installed/
```

其中真正给你的项目使用的安装结果主要在：

```text
vcpkg/installed/
```

例如：

```text
vcpkg/installed/x64-linux/
├── include/
├── lib/
├── bin/
├── share/
└── ...
```

你的项目：

```text
my_project/
├── src/
├── CMakeLists.txt
├── vcpkg.json
└── build/
```

通过 vcpkg 后，大致关系是：

```text
                  vcpkg
                    │
             ┌──────┴──────┐
             │             │
          packages/     installed/
          源码/构建       实际安装结果
                           │
                           ↓
                     C++项目使用
```

---

### 3. 所以你可以把它理解成三层

这是你现在最需要建立的概念：

```text
① 系统包管理器
   apt / rosdep
        ↓
   /usr/include
   /usr/lib
   /usr/share


② 项目级依赖管理
   vcpkg
        ↓
   vcpkg/installed/


③ 项目自己的构建产物
   CMake + make
        ↓
   project/build/
```

**不要把这三个目录混在一起理解。**

尤其是：

> `build/` ≠ 第三方 C++ 库仓库

`build/`主要是**这个项目编译过程中产生的中间文件和最终程序**。

---

如果你现在的目标是\*\*“我的开发电脑已经把 C++ 环境配置好了，怎么把这套环境比较完整地搬到工控机”\*\*，那么就要进一步区分 **apt/rosdep 管理的库** 和 **vcpkg 管理的库**，两种搬迁方式是不一样的。
