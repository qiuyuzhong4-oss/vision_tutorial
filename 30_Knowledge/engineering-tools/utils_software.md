# 视觉组接触的软件

> 本文从《了解CV和RoboMaster视觉组.md》的“3.视觉组接触的软件”整理而来。图片仍链接到原教程目录下的 `Image_base/` 图片库，请保持本文与 `Image_base/` 位于同一目录。

> 进行视觉开发会用到各种各样的软件、开发环境、辅助工具等，所以很有必要了解一些相关的快捷键、命令、使用技巧。选择一款适合自己的IDE能够提高开发效率，方便版本管理。

## 3.1 Ubuntu

- 为什么使用Ubuntu

  - Ubuntu是一个Debian系分支的第一大系统，是当前**用户量最大的linux发行版**。因此，遇到任何问题一般都能够在用户社区[askubuntu](https://askubuntu.com/)中得到解答。它的安装也非常的方便，并且在更新到20.04后，ubuntu的桌面美观性也有提升。同时，ROS是在Ubuntu之下开发的。如果要使用ROS，Ubuntu是你的不二之选。

  - Linux下开发C++程序相比Windows有无与伦比的优势，可以方便的配置各种第三方库和依赖。常言道python好用是因为有大量开箱即用的第三方库，可以轻松通过pip安装，而Linux下通过yum/apt/pacman等包安装软件管理的软件包，实际上就是C/C++隐藏的库安装/管理利器！apt是Debian系发行版用于管理第三方库的一个软件，负责管理系统中安装的各类软件包，开发包，依赖库。可以通过apt轻松地安装各种软件（可执行文件）、开发库（头文件headers，.so动态链接库等。如果你曾经在Visual Studio中为项目配置繁杂的头文件、链接库路径等依赖，你一定会爱上Linux下用cmake管理c++环境的开发方式。

  - Linux的内核和上层系统都比Windows更加精简，故在**运行时占用的各类资源都要小于Windows**。在不打开任何应用的情况下，笔者的电脑在运行Windows10时占用的内存为4.2G，cpu占用率在10-20%左右，而运行Ubuntu20.04LTS的时候，只使用了2.2G的内存，cpu占用率只有10%不到。这样，在运行我们的视觉算法程序时，可以更充分地利用系统资源，最大程度压榨电脑的性能。（甚至可以在测试结束后实际运行时关闭图形界面，只保留终端！这样，系统内核作为唯一需要运行的基础程序，大概能将cpu占用率缩小到1-2%）

  - Linux对于深度学习的支持比Widnows更加友好，经常有sh脚本能够一键配置开发环境。此外Linux对一些设备驱动的支持也更完善，我们可以选择挂载自己需要的驱动和IO，并且精简属于自己的内核。

    <img src="Image_base/ubuntu2104.png" style="zoom: 50%;" />

    <center>原文截图保留；截至2026维护时，Ubuntu 24.04 LTS已发布，机器人开发中常见组合包括Ubuntu 22.04+ROS 2 Humble和Ubuntu 24.04+ROS 2 Jazzy</center>

- 想要安装Ubutnu，可以参阅这篇教程：[Ubutnu/Windows双系统的安装-排除各种问题！-NeoZng](https://blog.csdn.net/NeoZng/article/details/122779035)，当然，学习时使用虚拟机也是不错的选择，这能给你更大的试错空间，不用担心把系统搞奔溃。

  > 2026维护建议：如果你是新人并准备做ROS 2项目，优先在Ubuntu 22.04或24.04上开始；如果你要复现旧赛季开源代码，先看项目README锁定Ubuntu、ROS、OpenCV、CUDA、TensorRT/OpenVINO版本，再考虑Docker或双系统，避免把时间耗在无意义的环境错配上。

- 提到Linux就不得不提到**命令行的使用**，在Linux上进行开发常会使用到命令行，有些软件甚至只有命令行界面的版本。在一些时候，直接在命令行中用键盘操作可能要比数不清的鼠标点击快得多。你需要学习：

  - cd、ls 、pwd、mv、cp、touch、diff、rm、cat、mkdir、rmdir、echo、tar等文件系统的基本操作，grep、find 查找文件和目录
  - 帮助手册man和-help参数。
  - sudo、su、chmod等权限相关的操作。
  - ping、ifconfig、wget等网络相关的操作。
  - ***一定要亲手熟悉命令行的基本命令，切忌只看不动手！***学习以上命令，戳这里[Linux Commands](https://linuxconfig.org/linux-commands)，简版的教程推荐这个：[Linux Commands | Harry's Blog ](https://harry-hhj.github.io/posts/Linux-Commands/)

- **至少掌握一个**无GUI的文本编辑器的基本使用，如vi，vim，nano等。这能够帮助你在系统出现问题的时候快速修改一些配置文件，或是在使用ssh连接的时候简单地编写一些程序。当然，笔者**不推荐**你将这些文本编辑器作为主力IDE使用（即使是安装了各种各样的插件！）虽然一个熟练使用vim的程序员和一个熟练使用eclipse的程序员拥有相同的开发效率，但是vim的学习成本可不知道比eclipse高多少！

- Linux的设计哲学是**“一切皆文件”**。它将所有的IO设备如网络接口、usb接口、显示屏、相机、键盘鼠标、应用都视为文件，和这些“文件”的交互就是以规定的方式进行读写。因此，有必要了解Linux下的基本目录和文件组织方式，其目录结构请参考：[Linux文件目录结构一览表](http://c.biancheng.net/view/2833.html#:~:text=%E4%BD%BF%E7%94%A8%20Linux%20%E6%97%B6%EF%BC%8C%E9%80%9A%E8%BF%87%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%BE%93%E5%85%A5%20ls%20-l%20%2F%20%E5%8F%AF%E4%BB%A5%E7%9C%8B%E5%88%B0%EF%BC%8C%E5%9C%A8%20Linux,%E5%90%8C%E6%97%B6%EF%BC%8C%E5%90%84%E4%B8%80%E7%BA%A7%E7%9B%AE%E5%BD%95%E4%B8%8B%E8%BF%98%E5%90%AB%E6%9C%89%E5%BE%88%E5%A4%9A%E5%AD%90%E7%9B%AE%E5%BD%95%EF%BC%88%E7%A7%B0%E4%B8%BA%20%E4%BA%8C%E7%BA%A7%E7%9B%AE%E5%BD%95%20%EF%BC%89%EF%BC%8C%E6%AF%94%E5%A6%82%20%2Fbin%2Fbash%E3%80%81%2Fbin%2Fed%20%E7%AD%89%E3%80%82%20Linux%20%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E7%9B%AE%E5%BD%95%E6%80%BB%E4%BD%93%E5%91%88%E7%8E%B0%E6%A0%91%E5%BD%A2%E7%BB%93%E6%9E%84%EF%BC%8C%2F%20%E6%A0%B9%E7%9B%AE%E5%BD%95%E5%B0%B1%E7%9B%B8%E5%BD%93%E4%BA%8E%E6%A0%91%E6%A0%B9%E3%80%82)。对于文件**读写权限**的管理也非常重要的，这决定了用户/程序对某些文件是否有访问权限。要是对文件系统有一些了解，那便更好不过了。

- 在使用系统的时候，建议大家有良好的文件分类习惯，把代码库、软件、开发环境分开存放，避免出现home目录乱糟糟的情况。

  ![](Image_base/mdunderubuntu.png)

<center>这篇文章就是在Ubutnu下使用markdown编辑器完成的</center>

---

## 3.2 IDE

想要编写代码，光靠文本编辑器+gcc+gdb可不行，我们要充分利用技术进步带来的便利，谁不喜欢做懒人呢。这里推荐几款Linux下编写C++程序使用的IDE：

- [**VSCode**](https://code.visualstudio.com/Download)：微软的小儿子，啥系统都能用。丰富的插件生态只有你想不到没有你找不到，配置完之后使用起来非常方便，比如C++就有一个**C++ extensions pack**。官方文档也很详细，毕竟是微软主推的下一代编辑器。关键是好看啊！在使用了snippets和Visual Sutdio Intellicode这两个插件之后，智能提示也足够智能。想要写其他的语言也能够一条龙配齐，总之，上手容易且可定制化程度极高。

  ![](Image_base/vscode.png)

- [**Clion**](https://www.jetbrains.com/clion/download/#section=linux)：JetBrain家的IDE，界面很美观，智能提示也很智能。以前用过PyCharm或者其他jb系的IDE的同学可以继续使用。统一用cmake管理项目，对cmake扩展的支持非常到位。也提供了大量的可选插件。用.edu后缀的学校邮箱可以免费申请[教育资格](https://www.jetbrains.com/community/education/)，就可以免费用了。

  ![](Image_base/clion.png)

- [**Qt**](https://wiki.qt.io/Install_Qt_5_on_Ubuntu#:~:text=Installation%20Guide%20%28Ubuntu%20package%29%20Open%20a%20terminal.%20Type,or%2064-bit%20Linux%20installationdepending%20your%20version%20of%20Ubuntu.)：Qt也是一款跨平台的C/C++ IDE，在Qt上编写的GUI程序能够在所有平台上运行。用Qt可以方便地编写一些图形化的程序，比如串口调试助手、调参助手等。他的整体界面也算是比较清爽。

  ![](Image_base/qt.png)

- **这里需要特别提及的是CMakeLists的编写。**Linux没有Visual Studio这样保姆级的IDE，并不存在一款能够自动为你生成makefile的软件。所以至少要学习qmake和cmake中的一种工具。这里推荐cmake，虽然比qmake的语法稍微复杂一些，但是cmake的功能非常强大，拥有非常优良的跨平台支持。学习cmake还能帮助你进一步了解程序的编译、链接过程。关于程序是怎么从源代码到机器代码最后在电脑上运行起来和cmake的基本使用，请参考[《程序的生前死后-Cmake-noob-comein》-NeoZng]()这篇文章。

  ![](Image_base/cmake.png)

  对于那些不太复杂的项目，你还可以使用语法规则更简单的**xmake**，这是一款由国人研发的基于Lua的跨平台构建工具。

萝卜青菜各有所爱。虽然IDE把工具链都集成在了一起，极大地方便了我们的使用，但笔者还是推荐你学习一下**GNU工具链的使用和基本原理**，至少熟悉编译、汇编、链接的过程。这样可以更深入的了解软件的运行，以便在开发过程中出现问题的时候，快速定位问题所在并找到解决方法。

---

## 3.3 Git

团队协作开发需要一款优秀的代码管理工具，那**Git就是不二之选**，大家肯定都听过GitHub这个最大的提供gitlab服务的~~同性交友~~平台，它便是一个基于Git的代码托管平台。这里有个小故事，Git是Linux的元老Linus因为Linux社区被禁止使用BitKeepter这款版本控制软件后，一怒之下在一周之内用C写出来的程序哦。

我们实验室开始的时候都是用u盘拷贝程序，有时候在某个人的电脑上写一点有时候又在minipc上写一点，虽然在文件夹上标准了时间和版本号，然而这并没有什么用，这导致一次合并代码的时候有十多个版本的代码，根本不知道哪个能用哪个不能用，那时候又还不知道diff这个工具，弄得眼睛都快无了。

要学习Git，推荐这几个网站：[廖雪峰的git教程](https://www.liaoxuefeng.com/wiki/896043488029600)   [git简易指南-no deep shits!](https://www.bootcss.com/p/git-guide/)   [GitHub Guides](https://guides.github.com/)

在学习Git的时候，**一定要动手跟着一起实践，切忌光看不动！**俗话说熟能生巧。

![](Image_base/git.jpeg)

<center>git的标志性图标，分岔的icon表示强大的分支功能</center>

只要学会创建分支、合并冲突、建立远端仓库、合并分支和版本回退等基本操作即可，过于复杂的功能需要时查阅man和help，没必要强行记忆。

## 3.4 ROS

ROS是所谓的机器人操作系统。但实际上他并不是运行在硬件上的内核或操作系统，而是开发机器人所用的一套丰富完整的中间件，可以看作是完整的机器人框架和开发抽象层。

使用ROS可以免去许多线程间信息交互、传感器和执行器配置的烦恼，ROS已经提供了开箱即用的库，以及大量方便调试与可视化的工具如RViz和rqt等，还有精心设计的日志系统和配套的仿真环境gazebo。

学习ROS你只需要学习ROS的几个基本编程理念，如节点、服务、发布订阅的概念，以及ros的包管理和构建工具，之后就可以愉快的使用ROS了。

由于ROS1在实时性和安全性以及部分功能的易用性方面考虑得不是那么周到，在2017年ROS开始重构，就有了新的ROS2。与Python3和Python2的关系一样，你可以把ROS1和ROS2看作两套完全不同的系统，它们的功能大部分不兼容，即不能使用对方的库，若一定要这样做必须使用一个名为rosbridge的兼容库。但它们的设计理念是类似的，从ROS1迁移到ROS2只会让你感觉无比轻松方便。

若你对ROS不熟悉，请直接开始ROS2的学习。

2026维护：ROS 1 Noetic已经到达生命周期末期，新项目建议直接选择ROS 2。当前更常见的组合是Ubuntu 22.04+ROS 2 Humble或Ubuntu 24.04+ROS 2 Jazzy；如果必须复现ROS 1项目，建议使用Docker、虚拟机或独立旧系统环境，不要把旧依赖硬塞进新系统。

**通过ROS2，我们可以方便地构建视觉算法和建图定位、导航算法的框架，轻松接入各种传感器。**

---

## 3.5 其他常用软件和小工具

- [Microsoft Edge DEV for Linux](https://www.microsoftedgeinsider.com/en-us/download/?platform=linux) ：Edge浏览器Linux版，可以方便同步windows下的收藏夹、设置、插件等。集锦的功能非常好用。

  ![](Image_base/edge.png)

- [SimpleScreenRecorder](https://www.maartenbaert.be/simplescreenrecorder/#download) ：一款录制屏幕的软件

  ![](Image_base/simplescreenrecorder.png)

- VLC：一款多媒体播放器，方便录制调试视频后进行观看。若安装系统的时候选择最小安装，则不会预装媒体软件，因此需要自己安装。

  ![](Image_base/VLC.png)

- qv4l2：linux下相机驱动的图形界面，在Ubuntu软件商店可以找到，方便调节普通USB相机的参数。

  ![](Image_base/qv4l2appicon.png)

- Meld：一款diff软件的图形界面，方便对比文件的不同，在Git使用merge或pull的时候可能会用上,在Ubuntu软件商店可以找到。虽然vscode也预置了此功能（只需要安装git便会激活），但是只能在被git管理的repo文件夹里面启用。

  ![](Image_base/meld.png)

- [Fsearch](http://cboxdoerfer.github.io/fsearch/)：和Windows下的everything类似，提供超快速的文件检索功能。

  ![](Image_base/fsearch.png)

- [Typora](https://typora.io/#linux)：好看好用的markdown编辑器，本文就是使用typora编写的。**使用markdown编写代码的说明文档是一个很好的习惯**，这可以降低其他人阅读你编写的代码的难度，也有利于代码分享和代码的传承。同时，你的也可以使用markdown来记录自己的学习历程、一次艰难的问题解决之路。使用markdown可以提高你的记录效率。vscode内也有相关插件提供对markdown支持。现在似乎要收费了，可以在官网下载beta history版本，版本号为0.x的公测版仍然免费。

  <img src="Image_base/typora.png" style="zoom:135%;" />

- TigerVNC：一款局域网内可用的远程桌面软件，VNCViewer也可以作为替代。***强烈推荐使用远程桌面调车！***电控都有无线调试器，我们怎么能跪在地上呢（气抖冷）。在把运算平台安装到机器人上之后，我也曾经拿着一块小屏幕和键鼠，蹲在地上和机器人进行亲密交流，这不仅加深了我和机器人的感情，~~也加重了我的颈椎病和腰椎键盘突出。~~（最恐怖的是车车的云台或者底盘疯了的时候，线全部缠到机器人上**！！机器人甚至有可能对你造成伤害！！**~~都是电控的锅，你云台怎么又疯了~~）使用了vnc后，只要将minipc和你的笔记本连接到同一个局域网，你就可以优雅地拿着笔记本调车了。如果校园网的带宽不够，建议买一个路由器，或者和搭建裁判系统的路由器公用也可以。

  ![](Image_base/vnc.png)

  其他远程桌面如Xrdp（分辨率和画质最好）、**NoMachine**（最流畅，画质次之，可以实现局域网内IP自动搜索，强烈推荐！）也是很好的选择。

  > 配置Xrdp的步骤稍微有一点多，参考：[Ubuntu利用xrdp实现远程桌面连接](https://blog.csdn.net/NeoZng/article/details/123505127)；在此过程中可以熟悉linux系统的环境变量配置以及简单的计算机网络知识。

  >  上交的同学更是把这件事做到了极致，他们直接通过网页来修改机器人的各种参数并得到反馈信息，能做到不需要任何远程桌面就能实时调参，此想法以为妙绝！华南师范大学使用ROS会话进行网页可视化，也是一种选择。不过这些都需要了解包括动态网页的构建在内的一些基本前端知识。

- SSH：在外面不需要图形界面的时候，能够直接连接终端就是一件很方便的事情。并且在代码真正部署上车时通常我们为了最大程度降低额外开销会选择关闭图形界面，终端连接就成了不二之选。使用过SSH连接服务器的同学应该对此不陌生了，有兴趣的同学可以了解一下**非对称加密**的原理。linux下可以直接使用终端作为ssh的客户端，windows下Microsoft全新推出的windows terminal也十分美观。其他的如PuTTy等也可以尝试。

  VScode也有SSH connection插件，可以将连接端的文件夹映射到本地，同时还可以直接在code里**重用端口开启多个终端**！同时，通过宿主机安装的Code Server，所有的插件也支持在远端运行。关于SSH的原理及其在windows/linxu下的简单配置，[戳这里]()。

  <img src="Image_base/windowsterminal.png" style="zoom:140%;" />

- Docker：标志性的小蓝鲸logo。Docker可以把开发环境和依赖打包在一起并于Docker engine上运行，运行时完全和系统的环境隔离。就像一个**轻量级**的虚拟机。Docker能够将应用程序与基础架构（操作系统、开发环境、依赖等）分开，使用docker engine提供的抽象大大提高兼容性，不需要关心底层和外部复杂的关联从而专注于软件开发。相信很多同学都遇到开发的时候配环境时醉生梦死的情况，使用Docker镜像则可以免除这一切烦恼！华南师范大学PIONEER战队的[开源代码](https://github.com/chenjunnn/rm_vision)就提供了Docker的部署方案。这里也非常推荐他们开源的rm-vision视觉框架，这是一套基于ROS2构建的自瞄程序，代码层次分明易读，关键部分附有注释和文档，调试工具好看易用。

  <img src="Image_base/docker.png" style="zoom: 50%;" />

  <img src="Image_base/dockerhow.png" style="zoom: 80%;" />

  <center>Docker的架构</center>
