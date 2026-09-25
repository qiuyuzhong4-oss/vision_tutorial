# C++程序运行依赖

#### You:
c++里面我使用make命令构建完src的程序之后如果要运行程序不是运行的我构建产生的文件吗,这个是不需要源码以及之前下载的库的是吗

#### ChatGPT:
对，**基本可以这样理解，但有一个关键区别：运行时是否还需要库，取决于你的程序是静态链接还是动态链接。**

你用 `make` 构建 C++ 项目，大致经历：

```text
源代码
src/
├── main.cpp
├── xxx.cpp
└── xxx.hpp

        ↓ make / g++

编译 + 链接

        ↓

可执行文件
build/
└── my_program
```

运行时：

```bash
./build/my_program
```

### 1. 源码：运行时通常不需要

例如：

```text
src/main.cpp
src/xxx.cpp
```

这些源码主要是**编译阶段**使用的。

程序编译完成后，运行：

```bash
./my_program
```

并不会重新读取 `main.cpp`。

所以你完全可以：

```text
电脑A：
源码 + 编译环境 + 库
        ↓
      make
        ↓
    my_program

        ↓ 拷贝

电脑B：
    my_program
```

电脑B不一定需要你的 `.cpp`、`.hpp` 源码。

---

### 2. 但是：第三方库不一定可以完全不要

这取决于链接方式。

#### 静态链接

如果你的程序把库静态链接进去了：

```text
my_program
├── 你的代码
├── fmt
├── xxx库
└── xxx库
```

那么运行时通常不需要再安装这些库。

例如：

```bash
./my_program
```

直接运行。

---

#### 动态链接

如果使用 `.so` 动态库：

```text
my_program
   ↓
libxxx.so
```

那么运行时就需要 `.so` 文件。

例如：

```text
工控机：

my_program
libxxx.so
```

否则可能出现：

```text
error while loading shared libraries:
libxxx.so: cannot open shared object file
```

所以：

> **源码一般是编译时需要；动态库是运行时仍然可能需要。**

---

### 3. 你现在用 vcpkg 的情况尤其要注意

比如你的项目：

```text
项目
├── src/
├── CMakeLists.txt
├── vcpkg.json
└── build/
    └── my_program
```

vcpkg 安装的库可能最终以：

```text
vcpkg_installed/
├── include/
├── lib/
└── bin/
```

存在。

你的 `my_program` 如果动态链接了：

```text
vcpkg_installed/lib/libxxx.so
```

那么**编译完成后把 `my_program` 单独拿到工控机上，不一定能运行**。

你需要把对应的 `.so` 一起部署，或者让工控机本身安装对应的运行库。

---

所以你可以记住这个非常实用的关系：

```text
                编译阶段              运行阶段
源码 .cpp/.hpp     ✅                   ❌
静态库 .a          ✅                   ❌（已链接进去）
动态库 .so         ✅                   ✅
可执行文件         生成                  ✅
```

**因此，“`make` 完以后只拿构建出来的可执行文件就能运行”并不是绝对的。**

你现在如果是在考虑**把 PC 上用 vcpkg 配好的 C++ 项目直接部署到工控机**，最关键的就是继续搞清楚：**你的可执行文件到底依赖哪些 `.so`，以及这些 `.so` 是否已经包含/存在于工控机上。**
