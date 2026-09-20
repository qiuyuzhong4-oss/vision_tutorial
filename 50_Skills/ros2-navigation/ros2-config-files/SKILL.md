---
name: ros2-config-files
description: ROS2 project configuration file responsibilities - what belongs in package.xml, CMakeLists.txt, launch files, YAML params, device JSON, RViz configs, URDF/Xacro, maps, msg/srv/action, plugin XML, behavior trees, Gazebo world/SDF, calibration files, shell scripts, setup.py, and colcon build/install/log dirs. Use when creating or reviewing ROS2 packages (C++ or Python), deciding where a setting belongs, or debugging "code works but launch can't find resources", TF/frame mismatches, parameter loading, and colcon build issues. Trigger whenever the user mentions package.xml, CMakeLists, launch.py, 参数文件, yaml, rviz 配置, urdf, xacro, msg, srv, action, 插件, plugin, 行为树, behavior tree, gazebo, world, sdf, 标定, calibration, colcon, setup.py, COLCON_IGNORE, 配置文件, ROS2, humble.
---

# ROS2 配置文件职责速查

## 最高优先级：一条判断标准

**源码负责「算法和行为」，配置负责「环境、依赖、启动方式、参数、资源和模块连接关系」。**
写程序前先问：这个值会随比赛/场地/硬件/调试阶段变吗？会 → 配置文件；不会 → 源码。

## 什么信息放哪里

| 文件 | 放什么 | 典型排障 |
|------|--------|----------|
| `package.xml` | 包的身份证：依赖的 ROS2 包/第三方库，colcon 构建顺序 | 依赖找不到、构建顺序错 |
| `CMakeLists.txt`（C++ 包） | 编译目标、链接库、msg/srv 生成、**launch/config/rviz/urdf 的安装规则** | 编译找不到头文件、install 后 launch 找不到资源 → 回来查安装规则 |
| `launch/*.launch.py` | 系统如何启动：多节点组合、加载参数文件、话题重映射、命名空间、组合其他 launch | 节点没起来、参数没加载；不要把"如何接入系统"塞进节点源码 |
| `config/*.yaml` | 会调的参数：相机曝光/增益/分辨率、串口、雷达、导航/定位/滤波/规划参数，按实车/仿真/R1/R2 分套 | 调参要重新编译 = 参数没抽出来 |
| 设备 `*.json` | 厂商 SDK 私有配置（如 Livox/MID360 的 IP、输出模式），驱动读，不走 ROS2 参数系统 | 强依赖厂商驱动的配置放 JSON，普通节点参数放 YAML |
| `*.rviz` | 调试布局：图像/点云/栅格/TF/路径叠加显示、topic、颜色、坐标系、视角 | 写了新节点要同步维护 rviz 配置，别人才能快速看输出 |
| `urdf/*.xacro` | 连杆/关节/传感器安装位/坐标系静态关系，给 robot_state_publisher、RViz、Gazebo、Nav2 用 | **很多"算法问题"其实是 URDF 里 frame 名或安装位置不对** |
| `map/*.yaml` `*.pgm` `*.posegraph` `PCD/*.pcd` | 2D 栅格图/位姿图/点云地图；路径由 launch 或参数指定，**不写死在源码** | 换场地 = 换一套地图资源，不改代码 |
| `msg/*.msg` `srv/*.srv` `action/*.action` | 节点间长期共享的数据结构（底盘/机械臂/裁判系统/导航事件） | 别用字符串/临时数组凑合，抽象成接口文件 |
| `*_plugin.xml` | 让 Nav2/BehaviorTree/pluginlib 动态加载你的类 | 普通节点不需要；换局部规划器/代价地图转换器才要 |
| `bt_xml/*.xml` | 决策流程编排（巡航/取矿/避障/重试）；C++ 只实现单个动作/条件节点 | 改流程不动 C++，改动作不动 XML |
| `*.world` `*.sdf` `model.config` | 仿真场地/模型/材质/插件；实车与仿真共算法、差异放仿真配置与 launch | 仿真行为怪先查 world/sdf |
| 标定 YAML | 相机内参外参、畸变、标定板尺寸/角点 | 涉及三维位姿/投影/测距先确认标定文件加载对了 |
| 根目录 `*.sh` | 工程入口封装：source 环境 + colcon build + 各模式启动；**脚本自定位根目录，不写死绝对路径** | sh 只做入口，核心参数仍放 launch/YAML |
| `setup.py` `setup.cfg`（Python 包） | 包名、入口点、资源安装；没注册入口 `ros2 run` 找不到 | Python 节点能手动跑但工具链找不到 = 入口/资源没装 |
| `.pre-commit-config.yaml` `.vscode/` CI 文件 | 开发流程，与机器人运行无关，别和运行参数混 | — |
| `build/ install/ log/` | colcon 生成物，**不手动维护**；install 缺资源回查 CMakeLists 安装规则 | 报错在生成目录 → 回源码侧修 |

## 抽象原则（原文照录）

- 包依赖/安装规则/编译目标 → `package.xml` + `CMakeLists.txt`（Python 包再加 `setup.py/setup.cfg`）
- 节点如何组合启动 → `launch/*.launch.py`
- 经常调的算法/硬件/话题/frame 参数 → YAML 参数文件
- 厂商驱动设备连接信息 → JSON 或专用配置
- 节点间长期共享的数据结构 → `msg/srv/action`
- 机器人结构/传感器安装/TF 静态关系 → URDF/Xacro
- 可视化调试布局 → RViz 配置
- 地图/点云/位姿图 → 作为运行资源由参数或 launch 指定
- 仿真世界/模型/材质 → world、SDF、model.config、material
- 复杂任务流程 → 行为树 XML，具体动作实现留在代码里

## references

- `references/ros2_profile.md` —— 完整 18 节详解（以 ~/RC2026 为样例），本文件的上游文档，冲突时以它为准。
