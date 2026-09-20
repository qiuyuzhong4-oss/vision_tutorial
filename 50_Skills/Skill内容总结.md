# Skill 内容总结(v1.0):全库 23 个 skill 各自讲了什么

> 定位:《Skill分类总结.md》回答「**什么项目用哪些 skill**」,本文档回答「**每个 skill 里面有什么内容、改它时要注意什么**」。
> 权威数据永远是各 skill 的 `SKILL.md` 本体,本文档是内容索引 + 跨 skill 一致性对照;安装方法见《装skill方法总结.md》。
> 机器人 10 个 skill 来源:`~/robotics-agent-skills` 克隆(上游 arpitg1304/robotics-agent-skills),2026-09-17 已逐字节校验与本库副本一致。

## 全库一览

| 分类 | Skill | 行数 | 一句话内容 | 来源 |
|------|-------|-----:|-----------|------|
| ros2-navigation | [ros2](ros2-navigation/ros2/SKILL.md) | 994 | ROS2 通用开发:QoS、生命周期、launch、组件、colcon、DDS 调优 | 仓库 |
| ros2-navigation | [ros1](ros2-navigation/ros1/SKILL.md) | 407 | ROS1 开发 + ROS1→ROS2 迁移对照 | 仓库 |
| ros2-navigation | [robotics-software-principles](ros2-navigation/robotics-software-principles/SKILL.md) | 896 | 12 条机器人软件设计原则 + 代码评审清单 | 仓库 |
| ros2-navigation | [robotics-design-patterns](ros2-navigation/robotics-design-patterns/SKILL.md) | 609 | 系统架构:分层栈、行为树/状态机、HAL、安全体系、sim-to-real、数据录制 | 仓库 |
| ros2-navigation | [robot-bringup](ros2-navigation/robot-bringup/SKILL.md) | 1806 | 量产启动:systemd、分层 launch、有序启动、udev、多机 DDS、优雅停机 | 仓库 |
| ros2-navigation | [robotics-testing](ros2-navigation/robotics-testing/SKILL.md) | 577 | 测试金字塔:pytest+ROS2、launch_testing、mock 硬件、金样回归、CI | 仓库 |
| ros2-navigation | [docker-ros2-development](ros2-navigation/docker-ros2-development/SKILL.md) | 1102 | 多阶段 Dockerfile、compose、跨容器 DDS、GPU/USB 透传、CI | 仓库 |
| ros2-navigation | [robotics-security](ros2-navigation/robotics-security/SKILL.md) | 890 | SROS2/DDS 安全、网络分段、机密管理、物理-网络安全交叉 | 仓库 |
| ros2-navigation | [robotics-ai-coding-rules](ros2-navigation/robotics-ai-coding-rules/SKILL.md) | 134 | AI 改代码先复述确认 + 机器人领域检查项 | 桌面 skill 迁入 |
| ros2-navigation | [publish-git-repositories](ros2-navigation/publish-git-repositories/SKILL.md) | 212 | git 仓库发布/排障:PAT、deploy key、大文件、历史重写 | 桌面 skill 迁入 |
| ros2-navigation | [ros2-config-files](ros2-navigation/ros2-config-files/SKILL.md) | 50 | 18 类 ROS2 配置文件职责速查 +「配置问题伪装成算法问题」 | 提炼自 ros2_profile.md |
| ros2-navigation | [ros2-thread-naming](ros2-navigation/ros2-thread-naming/SKILL.md) | 70 | 进程/线程命名与可观测性(htop/htop 设置/给 AI 话术) | 提炼自 CPU资源查询工具等 |
| ros2-navigation | [ros-team-code-framework](ros2-navigation/ros-team-code-framework/SKILL.md) | 52 | RM 视觉组代码框架 + 开发纪律 + 去绝对路径化 | 提炼自源笔记 |
| ros2-navigation | [personal-dev-workflow](ros2-navigation/personal-dev-workflow/SKILL.md) | 48 | 个人开发流程:需求五要素、文档分离、README 三阶段 | 提炼自工作台文档 |
| camera-perception | [robot-perception](camera-perception/robot-perception/SKILL.md) | 1654 | 感知工程:标定、帧流、深度/点云、融合、跟踪、时延预算 | 仓库 |
| camera-perception | [yolo-training-params](camera-perception/yolo-training-params/SKILL.md) | 53 | YOLO(RM 场景)训练参数速查 + 验证闭环 | 提炼自 YOLO 参数手册(活文档) |
| general-tools | [ros2-web-integration](general-tools/ros2-web-integration/SKILL.md) | 1430 | rosbridge/FastAPI 桥、WebSocket 视频流、限流、Web 安全 | 仓库 |
| general-tools | [document-processing-workflows](general-tools/document-processing-workflows/SKILL.md) | 105 | 文档处理路由:MinerU/OCR/Office 转换如何选、如何排障 | 桌面 skill 迁入 |
| general-tools | [fix-linux-proxy-dns](general-tools/fix-linux-proxy-dns/SKILL.md) | 116 | 「不开代理网页打不开」诊断修复:系统代理/DNS 分裂脑 | 桌面 skill 迁入 |
| general-tools | [configure-codex-profile-keys](general-tools/configure-codex-profile-keys/SKILL.md) | 81 | Codex 多 profile + 按 profile 独立 API key 文件的 shim | 桌面 skill 迁入 |
| general-tools | [migrate-codex-skills](general-tools/migrate-codex-skills/SKILL.md) | 231 | skill 跨机迁移:目录形状、装法选择、软链 vs 复制、依赖、校验 | 桌面 skill 迁入 |
| knowledge-curation | [pdf-converter](knowledge-curation/pdf-converter/SKILL.md) | 138 | MinerU 文档转换本体:flash-extract/extract 两模式、语言、分页 | npx skills add 安装 |
| knowledge-curation | [knowledge-base-curation-rules](knowledge-curation/knowledge-base-curation-rules/SKILL.md) | 141 | RM_Knowledge 三模块信任模型 + 整理工作流 + 写入边界 | 桌面 skill 迁入 |

---

## 一、ROS2 导航 / 整车类(ros2-navigation/)

### 1. ros2 — ROS2 通用开发

- **讲什么**:生产级 ROS2 全流程——节点模式、QoS 正确性(自称第一大 bug 来源)、生命周期节点、Python launch、组件化零拷贝、DDS/RMW 配置、colcon 构建体系、调试工具箱、量产部署清单。
- **核心规则**:
  - QoS 兼容性:BEST_EFFORT 发布端 + RELIABLE 订阅端 = 静默连不上,用 `ros2 topic info -v` 排查。预设:传感器(相机/雷达)用 SensorDataQoS;指令用 RELIABLE depth 10;地图/静态数据用 RELIABLE+TRANSIENT_LOCAL(替代 ROS1 latch)。生产禁用默认 QoS。
  - 关键组件用生命周期节点,launch 事件句柄编排 configure→activate;参数先声明再建发布/订阅,`add_on_set_parameters_callback` 做运行时改参。
  - 大消息用组件容器 + 进程内通信 + `UniquePtr` 零拷贝;固定 `RMW_IMPLEMENTATION`(推荐 CycloneDDS),设 `ROS_DOMAIN_ID`、单机 `ROS_LOCALHOST_ONLY=1`。
  - colcon:先 source underlay;source `install/setup.bash` 而非 `build/`;Python 用 `--symlink-install`;迭代用 `--packages-up-to`;构建前 `rosdep install`。
- **反模式**:静默 QoS 不匹配、跳过 rosdep、Python 包漏 `rosidl_default_runtime`、overlay 重名包、deactivate 不销毁订阅。
- **附带模板**:rclpy/rclcpp 节点、完整生命周期节点、launch/组合、ActionServer、DDS XML、package.xml/CMakeLists/setup.py、msg/srv/action 定义、调试命令速查。

### 2. ros1 — ROS1 开发与迁移

- **讲什么**:ROS1 系统设计(节点/话题/launch/TF/actionlib)、常见运行时故障(时间同步、回调阻塞、参数作用域)、nodelets 零拷贝、调试工具箱,以及 ROS1→ROS2 迁移对照清单。
- **核心规则**:单一职责节点;高频率传感器 `queue_size=1`、禁 0(无限队列);低频变化数据用 latch;TF 一父一帧、带超时查找并捕获异常;actionlib 显式 `start()` + 执行循环里查抢占;多传感器用 `ApproximateTimeSynchronizer`;重活离开单线程 spinner。
- **迁移映射(核心资产)**:rospy→rclpy、catkin→colcon、nodelets→components、dynamic_reconfigure→参数回调、latch→TRANSIENT_LOCAL、roscore→DDS 发现;先迁叶子节点,用 `ros1_bridge` 双栈过渡。

### 3. robotics-software-principles — 机器人软件设计原则

- **讲什么**:把 SOLID 及机器人特有原则落到代码——12 条原则每条配「坏 vs 好」Python 对照,附 12 行评审清单。强调机器人特殊性:物理后果、硬实时、传感器噪声、硬件多样性、sim-to-real、安全攸关。
- **核心规则**:模块描述含「和」就拆;高层代码永不 import 具体驱动,双方依赖 ABC(仿真/实车可互换的根基);加传感器走插件注册不改 if/elif;速率分离表(安全监控 1000 Hz → 关节控制 500–1000 Hz 硬实时 → 规划/日志尽力而为),慢系统只经缓冲/队列与快回路通信;失效安全默认(爬速、碰撞检查开、显式 enable);magic number 进 YAML;命令幂等(move_to + 指令 ID 去重);结构化遥测;行为由原技能组合并支持分级降级到 safe_stop。
- **反模式**:上帝模块、高层 import 驱动、感知阻塞控制回路、非幂等相对位移、printf 日志。

### 4. robotics-design-patterns — 系统架构模式

- **讲什么**:整机架构:六层机器人软件栈、行为树 vs 状态机选型、感知管线、HAL、四层安全体系、sim-to-real 切换、面向学习的数据录制;末尾 8 反模式 + 10 问架构决策清单。
- **核心规则**:信息上行、决策下行,应用层永不直接碰硬件(经 HAL 工厂按配置选真机/仿真实现);决策框架默认行为树(模块化/可复用/可调试),动作节点走 setup/initialise/update/terminate 生命周期、黑板共享状态、必带安全 fallback 分支;频率规则:控制器 > 规划器 > 传感器;四层安全:硬线急停 → SIL 控制器硬件看门狗 → 软件心跳看门狗 → 应用层每次指令前限位检查;数据在源头打时间戳、控制用单调钟;episode 事件触发录制(MCAP/Zarr/HDF5/RLDS)。
- **反模式**:上帝节点、轮询代替事件、无失败恢复分支、只在仿真跑过就上真机、丢时间戳、不录数据。

### 5. robot-bringup — 量产启动(最大 skill,1806 行)

- **讲什么**:把 ROS2 栈作为长期运行的生产服务:分层启动栈映射到 systemd + 可组合 launch、带健康检查的有序启动、udev 稳定设备名、多机 DDS 网络、看门狗心跳、日志轮转、优雅停机。面向 Ubuntu 22.04/24.04 + Humble/Iron/Jazzy。
- **核心规则**:
  - systemd 服务禁依赖 `.bashrc`:用 `EnvironmentFile=/etc/robot/ros2.env` + `ExecStart=/bin/bash -c 'source … && exec ros2 launch …'`。
  - 按层拆服务,`After=/Requires=/PartOf=` 组织驱动→感知→应用,反序停止;`Type=notify` + `WatchdogSec` + 进程内 `sd_notify(WATCHDOG=1)`;重启限速(`Restart=on-failure`/`StartLimitBurst`)+ `OnFailure=` 告警 + 资源限额。
  - 等 `network-online.target` 而非 `network.target`;`ExecStartPre` 轮询设备/节点健康;用 lifecycle manager 做有序 configure/activate。
  - udev 按 idVendor/idProduct/serial 建稳定别名 `/dev/robot/*`,禁硬编码 `/dev/ttyUSB0`。
  - 多机 DDS:netplan 静态 IP、CycloneDDS 显式 peer、关组播、防火墙按 `7400 + 250×domain_id` 放行、每机器人独立 domain ID。
  - 每个执行器节点注册 SIGINT/SIGTERM 处理:退出前发零速度 + 抱闸;logrotate + journald 限额。
- **反模式**:`.bashrc` 当 systemd 环境、无启动顺序、无限 `Restart=always`、根用户跑全栈、无停机处理(机器人带最后速度滑行)。

### 6. robotics-testing — 机器人测试

- **讲什么**:机器人测试金字塔(单元→集成→仿真→HIL→现场)与「让机器人测试确定性、可进 CI」的完整做法。
- **核心规则**:每模块一次 `ros_context` fixture,每测试新建/销毁节点;运动学/四元数抽成纯函数脱离 ROS 测;Hypothesis 属性测试不变量(插值端点、单调进度、变换逆往返、单位四元数);集成用 `launch_testing` + 有超时的事件驱动等待(禁 `time.sleep()`);mock 硬件给确定性合成数据;金样轨迹回归(`assert_allclose` + 无碰撞断言);仿真固定种子、断言任务位姿/步数预算/零接触;GitHub Actions 分层(单元→集成→仿真)跑 `ros:humble` 容器。
- **反模式**:测试里 sleep(脆)、只测 happy path、规划器随机不播种。

### 7. docker-ros2-development — 容器化 ROS2

- **讲什么**:ROS2 容器化:镜像选型、多阶段构建、compose 多服务、跨容器 DDS 发现、GPU/USB/显示透传、devcontainer、CI,附 12 项部署清单。
- **核心规则**:选满足依赖的最小基础镜像;多阶段 deps→dev→build→runtime,runtime 只拷 `install/`;层缓存顺序:先拷 package.xml → rosdep → 再拷 src/;bridge 网络会挡 DDS 组播——用 host/macvlan 或显式单播 peer 列表,共享 `/dev/shm` 且 `shm_size` ≥256MB(图像 512MB);只 bind-mount `src/`,build/install/log 放命名卷;非 root 运行 + 最小组;compose 健康检查 + `depends_on: service_healthy`;udev 稳定设备名透传;`ROS_DOMAIN_ID` 走环境变量;禁部署无版本 `latest`,保留上一版镜像可回滚。
- **反模式**:单容器跑全部子系统、bridge 网络不配单播(节点互相发现不了)、runtime 里编译(+1–2GB)、整工作区 bind mount、层序错误、domain ID 写死。

### 8. robotics-security — 安全加固

- **讲什么**:六大攻击面(网络/中间件/应用/物理/固件/供应链)纵深防御,主题是「网络漏洞在机器人上会变物理威胁」:SROS2/DDS 安全、网络分段、机密管理、容器与安全启动、审计、物理-网络安全交叉;附 8 反模式 + 14 项清单。
- **核心规则**:
  - 生产恒用 `ROS_SECURITY_STRATEGY=Enforce`;按节点 enclave 最小授权(permissions XML `default: DENY`——被攻破的相机驱动发不了 `/cmd_vel`);CA 私钥 root-only 600。
  - 三平面 VLAN 分段(控制仅有线 / 数据 / 管理走 VPN+跳板);防火墙默认拒,UDP 7400–7700 只放行控制平面;关 DDS 组播发现改单播 peer。
  - SSH 仅密钥 + 每机器人独立密钥或 SSH CA 短时证书 + fail2ban;机密走 systemd `EnvironmentFile`,gitleaks 扫描,证书按月轮换。
  - **急停必须硬线**——软件/网络全死也能停;无线急停用专用射频不用 WiFi;安全控制器放独立裸机 MCU(无 ROS2/Linux)经 CAN/UART 校验速度/加速度/限位;驱动层速度安全门(钳位、加速度限制、超时零速)。
  - 容器非 root + `read_only` + `cap_drop: ALL`,trivy 扫描 + cosign 签名 + SBOM;固件 ECDSA 验签 + TPM2 绑定 LUKS + 只读根;auditd 监控 + `/cmd_vel` z-score 异常检测。
- **反模式**:裸奔的 `/cmd_vel`、全队共享 SSH key、全节点 root、平铺网络、图省事「临时」关安全(最常见失效——CI 必须在 Enforce 开启下通过)。

### 9. robotics-ai-coding-rules — AI 协作规则(自有)

- **讲什么**:机器人/视觉/电控项目里 AI 改代码的纪律。最高优先级:**动手前先复述需求 + 方案 + 文件结构,等用户确认**;只问不答改。
- **要点**:方案要标明改什么、必须保持什么、受影响模块、验证步骤;禁止未经请求的「聪明改动」(加依赖/抽象/自动调参/硬件假设);违反工程常识或安全(关急停/看门狗/限位、忽略坐标系/单位/标定、硬编码电机方向/CAN ID/相机内参)必须**警告两次**再等确认;改前先读代码(rg 全树扫描),说不清影响面就先问;结尾报告改了什么、保住了什么、跑了什么验证、剩余风险(硬件/标定/时序/安全)。
- **附带**:新项目五目录骨架(perception/control/communication/config/tests)、机器人领域检查清单(相机管线、TF/坐标系、控制回路频率/PID、通信协议字节序 CRC 等)。

### 10. publish-git-repositories — 仓库发布(自有)

- **讲什么**:GitHub/Gitea 推送、认证、排障与验证。安全红线:不在聊天/文件/命令历史出现 PAT 与私钥;`git add .` 前查 .gitignore/大文件/疑似密钥;历史重写与强推需用户明确批准;个人知识库默认**白名单发布**。
- **要点**:首次推送标准流程(remote add → add → commit → push -u);PAT 只做临时引导(变量注入、用完撤 URL、泄露即吊销);长期用 SSH/deploy key(`core.sshCommand` 写 `.git/config` 不进跟踪文件);SSH 22 不通用 GitHub 443 兜底;大文件(模型权重/点云/视频/数据集)与隐私内容不入普通 git;Gitea 413 用 git-filter-repo 清历史(警告会改哈希);push 后用 `git ls-remote` 对哈希验证。
- **常见故障**:`fetch first` → pull --rebase 或 force-with-lease;`Permission denied (publickey)` 五种原因排查。

### 11. ros2-config-files — 配置文件职责速查(自有)

- **讲什么**:一条判断标准(值会随比赛/场地/硬件/调试阶段变吗?会→配置,不会→源码)+ 18 类文件职责表:package.xml(身份证/依赖)、CMakeLists(编译目标 + **launch/config/urdf 安装规则**)、launch(系统怎么启动)、YAML(会调的参数,按实车/仿真分套)、厂商设备 JSON(不走 ROS 参数系统)、rviz(调试布局)、URDF/Xacro(**很多「算法问题」其实是 frame 名或安装位置不对**)、地图资源、msg/srv/action、plugin XML、行为树 XML(改流程不动 C++)、world/SDF、标定 YAML、sh 入口(自定位根目录)、setup.py 入口点、build/install/log 不手维护。
- **定位**:是 ros2 skill 构建系统章节的「赛场速查版」,上游详版 `references/ros2_profile.md` 冲突时以它为准。

### 12. ros2-thread-naming — 线程命名与可观测性(自有)

- **讲什么**:ROS2 Humble 下四个名字别混淆:Linux 线程名(15 字符截断)/ 进程名 / cmdline / ROS Node 名。关键事实:htop 默认显示 cmdline 不是 comm 名(是没开选项不是没生效);Executor 内部线程不能靠 `threading.Thread(name=)` 命名。
- **要点**:开头附「给 AI 下任务的标准话术」可直接复制;C++ `pthread_setname_np`(≤15 字符)/ Python ctypes 调 libpthread 代码片段;htop 开启 custom thread names 的一次性设置(F2 → Display options → 勾选,**实测 Esc 才能保存**);`ps -T`/`/proc/<pid>/task/<tid>/comm` 验证。

### 13. ros-team-code-framework — 视觉组代码框架(自有)

- **讲什么**:RM 视觉组雷达导航/相机视觉两条线,写码前先对齐框架。推荐仓库骨架(docs、script/utils、src 下 decision/driver/localization/msg/nav_bringup/perception/simulation,每包 config+launch,sh 统一入口做 source+conda+调度)。
- **要点**:开发纪律——每次开发写开发文档 + 提交本地 git;BUG 记录三要素(原因+修复手法+截图);里程碑完成即标记;工程强制约定——**去绝对路径化**(path/os 相对路径,clone 即编译)、gitignore 挡地图/缓存/编译产物、pdf 转 md 才能上传。
- **注意**:开发纪律部分与 personal-dev-workflow §4 同源,改动需两处同步(见重叠表)。

### 14. personal-dev-workflow — 个人开发流程(自有)

- **讲什么**:从工作台四份开发文档提炼的流程规范:①新项目需求文档五要素(使用场景/解决的问题/接口定义/阶段性目标/最终目标);②需求完善流程(草稿→外部 AI 讨论借鉴项目→完善→AI 复述确认→开发文档,含可借鉴项目/技术链/框架/独立技术链路文档);③文档职责分离(总文档三件套少改;单次需求进 single;讨论稿进 archive 只读;rules 只放规则条目不放 skill 实体);④每次开发纪律(开发文档+git、BUG 三要素、里程碑即时标记);⑤README 三阶段(最简→补充→交付打磨);⑥现阶段 skill 约定(只用纯知识/规则类 skill、不在项目内装常驻 skill、项目内引用靠工作台拖入扁平化)。
- **活文档声明**:来源为工作台 docs 四件套,更新以它们为准。

---

## 二、相机视觉 / 感知类(camera-perception/)

### 15. robot-perception — 感知工程(仓库,最大 1654 行)

- **讲什么**:可靠实时感知的工程学(非 ML 训练):传感器选型对比表、标定(内参/外参/双目/相机-雷达/手眼)、帧流纪律、RGB/深度/点云处理、融合跟踪、时延预算。含约 20 个可复用 Python 类模板(OpenCV/Open3D)。
- **核心规则**:
  - 采集线程在采集时刻打时间戳(`time.monotonic()`),绝不在处理时刻;采集与处理解耦(专用采集线程 + `deque(maxlen=2)` 只处理最新帧),禁 sleep 节拍。
  - 同步优先硬件(主从同步、PTP <1µs);软件时间戳匹配容差 ~33ms(30Hz 一帧)。
  - 标定门槛:内参 RMS <0.5px(≥20 张覆盖角落/倾斜);双目 <1px;相机-雷达重投影 <3px;手眼 ≥15 位姿 ≥3 旋转轴、验证 <5mm(操作)/<10mm(导航);碰撞/重新对焦/温漂后重标。
  - 几何计算前先去畸变(映射表预计算一次);深度清理顺序:距离滤波→飞点→修补→双边;反投影取 5×5 中值并验 `0<z<max_range`;点云顺序:裁 ROI→离群剔除→体素降采样→法线→RANSAC/DBSCAN;ICP 必须有粗配准初值(FPFH+RANSAC),fitness<0.3 判失败。
  - 检测结果先变换到 base/world 系再指挥机器人;感知+规划时延 < 控制周期,全管线 <100ms;重模型抽帧跑,不跟传感器帧率;丢弃前 ~30 帧自动曝光预热。
- **反模式**:单线程采集+处理、无界帧缓冲、晚打时间戳、每帧算去畸变映射、盲用原始深度、假设标称内参、隐式混坐标系。

### 16. yolo-training-params — YOLO 训练参数(自有,活文档型)

- **讲什么**:ultralytics YOLO 在 RM 装甲板场景的参数速查,带**活文档声明**:权威是 `30_Knowledge/computer-vision/YOLO训练参数手册.md`,回答前先读活文档,新结论回填活文档而不是只改 skill;每条参数标来源(✅实测/🗣️群结论/📦代码确认/⚠️未验证),验证闭环 = 猜测→工作台预览→训练实测→回填。
- **要点**:RM 关键参数(hsv_h ≤0.01 保红蓝分类、scale 0.5–0.9 小目标核心、flipud 0、mosaic 保持 1.0、copy_paste 对 bbox-only 数据集无效、batch=-1 防 8G OOM、amp 开、cache 关);场景痛点→手段映射表(小目标→SAHI 切片推理;红蓝混淆→压 hsv_h;运动模糊→官方无内置需 Albumentations);RTX 5060 8GB Blackwell 环境硬约束(torch 必须 cu128+,否则 `no kernel image`;分层诊断驱动/构建/运行三层)。

---

## 三、通用工具类(general-tools/)

### 17. ros2-web-integration — ROS2 Web 集成(仓库)

- **讲什么**:把 ROS2 话题/服务安全暴露给 Web:rosbridge_suite vs 自建 FastAPI/Flask 桥的选型表、WebSocket 相机流、遥控看门狗、限流背压、TLS/JWT/CORS。
- **核心规则**:rclpy MultiThreadedExecutor(2–4 线程)放守护线程,Web 服务在主线程,**绝不共享事件循环**;ROS 回调与 HTTP 处理器间的共享状态用锁;异步处理器里禁 `spin_once`/同步 `call()`,用 `call_async()` + `run_in_executor()` 带超时;订阅 CompressedImage(BEST_EFFORT depth 1),绝不向浏览器转发原始 Image;WebSocket 发二进制帧省 ~33% 带宽;每客户端令牌桶限流(钳到 1–30Hz)+ 背压降 JPEG 质量;遥控看门狗:500ms 无指令或断连即发零速度;配置驱动话题白名单,绝不动态订阅客户端要的话题;rosbridge 生产必须 `authenticate:=true`+globs+反代;nginx 终结 TLS、桥只听 localhost、CORS 显式白名单;断连客户端及时清理,优雅停机按 executor→node→rclpy→join 线程顺序。
- **反模式**:HTTP 处理器里 spin、流式发原始图像(921KB/帧)、传感器流不限流(20Hz 雷达 ≈8MB/s)、无鉴权 rosbridge(任何浏览器可发 /cmd_vel)。

### 18. document-processing-workflows — 文档处理路由(自有)

- **讲什么**:文档任务的**路由层**(本体是 knowledge-curation/pdf-converter):按输出需求选工具链——内容提取/OCR/转 Markdown/Word 走 MinerU(pdf-converter);PDF 结构操作(拆分/合并/加密/填表)用 pypdf/pdfplumber;改 Office 原生文件用 DOCX/PPTX/XLSX 专用工具;一条路失败换另一条并对比输出,简单问题不跑昂贵转换。
- **要点**:MinerU 两模式(flash-extract 10MB/20页免鉴权,extract 200MB/600页需 `mineru-open-api auth`);语言参数常见值;常见请求(读 PDF/转 Word/提取表格)的处理方式;故障表(command not found/鉴权/超时/表格差/乱码);响应要报告用了哪条工作流、输出路径、质量局限。

### 19. fix-linux-proxy-dns — 代理/DNS 修复(自有)

- **讲什么**:「不开 VPN 网页打不开、微信 QQ 却能联网」的诊断修复:按代理/DNS 分裂脑处理(浏览器走系统代理,聊天软件走直连)。先只读诊断(env 代理变量、gsettings、本地监听端口 7890 等、代理进程、路由/DNS、直连 vs 走代理 curl 对比),经用户批准才改系统。
- **要点**:DNS 先测后改(dig 逐个测 223.5.5.5/119.29.29.29 等,测通的才上);修复手段——gsettings 关 GNOME 系统代理、在 Mihomo Party 里关 sysProxy(防它反复开)、`nmcli con mod` 配测通 DNS(或还原为自动 DNS,重连会短暂断网要提醒);最后验证 gsettings/nmcli/直连 curl 并报告改了什么。敏感信息(订阅/节点/UUID)不得出现在回复里。

### 20. configure-codex-profile-keys — Codex profile 密钥(自有)

- **讲什么**:给 Codex CLI 搭「每 profile 独立 API key 文件」的用户级方案:`$CODEX_HOME/keys/<profile>.key` 只注入子进程。安全红线:key 不进聊天/参数/TOML/shell 历史/git;key 目录 700、文件 600;终端里出现过的 key 视为泄露建议轮换;不 patch npm wrapper 或二进制,装用户级 shim 防升级覆盖。
- **要点**:`scripts/setup_profile.sh NAME` 一条命令装 shim + 生成 TOML 模板与 key 占位文件;`codex --profile NAME` 启动;`env_key` 只能放变量名(CODEX_<大写>_API_KEY)不能放 sk-...;修已有配置时把字面 key 移入 key 文件;`--force` 前先检查并留时间戳备份;verify_profile.sh 校验权限/注入/加载。

### 21. migrate-codex-skills — skill 迁移(自有)

- **讲什么**:skill 跨机复制/备份/安装/验证。核心答案:纯规则 skill 拷文件夹就够,但目标机必须让目录可被发现并满足依赖;合法目录形状 = SKILL.md + agents/openai.yaml(有就拷)+ scripts/references/assets,**拷整个文件夹不只拷 SKILL.md**。
- **要点**:装法五档(手动拷贝/软链/git clone/`npx skills add` 需 manifest/插件市场),短文本约定优先写 CLAUDE.md 而不是做 skill;Codex(`~/.codex/skills/`)与 Claude(`~/.claude/skills/`)路径别混;迁移前 checklist(find 全部 skill → 查捆绑文件 → rg 查绝对路径假设 → rg 查外部依赖);同机多工具复用用软链(改一处全生效),跨机迁移用拷贝(源头删了不断链),迁软链要拷真实源目录;tool 型 skill 需补装 scripts 依赖;拷完 quick_validate 或手检 frontmatter,重启会话确认 skill 出现;只拷 skills/ 不拷整个 ~/.codex。

---

## 四、知识库类(knowledge-curation/)

### 22. pdf-converter — MinerU 文档转换本体

- **讲什么**:MinerU Open API CLI 转换文档为 Markdown:两种模式——flash-extract(快、免鉴权、10MB/20 页、仅 Markdown、图表公式可能成占位符)与 extract(高保真、需 auth、200MB/600 页、md/json/html/latex/docx、公式/表格识别默认开、OCR 开关、批处理)。
- **要点**:抽取只是第一步,理解/总结/提取表格由 agent 读输出完成;stdout(即读即用)vs `-o`(持久输出);**分页提取必须输出为显式文件路径**(带 `_p{range}` 后缀),否则同文件多段互相覆盖——这是本 skill 的 CRITICAL 规则;语言默认 ch,80+ 语言;故障表(装 CLI/auth/超时/语言)。

### 23. knowledge-base-curation-rules — 知识库整理规则(自有)

- **讲什么**:RM_Knowledge 的整理纪律。最高优先级:改库前先复述变更等确认,只问不写。权威结构:**01_正式知识库 / 02_人工资料 / 03_AI聊天记录** 三模块信任模型(02 与 03 都是源材料但绝不合并;AI 聊天未经验证改写引用不算正式知识);不重建 04_待整理/05_资料归档。
- **要点**:正式笔记按主题/模块组织(不按来源平台)、脱离原始聊天可读、必须带回源信息(附来源传送口模板)、区分已验证事实/假设/待定问题、不确定的新模块进 `99_候选新分支`;工作流 = read→propose→preview/diff→confirm→write→verify,`rmkb scan/plan/apply` 命令工作流,先 dry-run 再真写;写入边界:不覆盖 02/03 源文件、不自动改写原始聊天、不为整洁乱移文件;改后跑 scan/编译检查并报告剩余风险。

---

## 五、跨 skill 重叠对照表(改任一处先查本表)

同一规则出现在多个 skill 里,是**有意重复**(每个 skill 需自洽),但改动时必须同步检查同行的其他 skill:

| 共享主题 | 涉及的 skill | 说明 |
|----------|--------------|------|
| QoS 预设(SensorData/RELIABLE/TRANSIENT_LOCAL) | ros2 · ros2-web-integration | web 侧 CompressedImage=BEST_EFFORT depth1 须与 ros2 预设一致 |
| DDS 网络(RMW、domain ID、关组播、peer、防火墙 7400+250×id) | ros2 · robot-bringup · docker-ros2-development · robotics-security | 四处口径必须一致 |
| 生命周期节点 | ros2 · robot-bringup | bringup 负责 launch 有序编排 |
| 零拷贝(/dev/shm、UniquePtr、组件) | ros2 · docker-ros2-development | docker 侧 shm_size 是前提 |
| 看门狗/心跳 | robotics-design-patterns · robot-bringup · robotics-security | 软件层(sd_notify/心跳)与硬件层(MCU/dev/watchdog)分层不重叠 |
| 停机零速度/安全停 | robot-bringup · ros2-web-integration · robotics-security · robotics-design-patterns | SIGTERM 处理、遥控 500ms 看门狗、驱动速度门、safe stop 各守一层 |
| 速率分离(控制>规划>传感;时延<控制周期) | robotics-software-principles · robotics-design-patterns · robot-perception | 原则给速率表,模式给频率规则,感知给时延预算 |
| sim-to-real(同接口、配置切换、use_sim_time、固定种子) | robotics-software-principles · robotics-design-patterns · robotics-testing · robot-bringup | |
| MCAP 数据录制 | ros2 · robotics-design-patterns | |
| udev 稳定设备名 /dev/robot/* | robot-bringup · docker-ros2-development | |
| systemd EnvironmentFile | robot-bringup(ROS 环境)· robotics-security(机密) | |
| rosbridge_suite | ros2-web-integration · docker-ros2-development | docker compose 示例起 rosbridge:9090 |
| 时间戳纪律(源头打戳、控制用单调钟) | robot-perception · robotics-design-patterns · ros1 | |
| **开发纪律(开发文档+git/BUG 三要素/里程碑)** | **ros-team-code-framework · personal-dev-workflow** | **两处同源文字,改一处必须同步另一处** |
| **ROS2 配置文件职责(package.xml/CMakeLists/colcon)** | **ros2-config-files · ros2** | 速查版与详解版口径要一致;冲突时 ros2-config-files 以 references/ros2_profile.md 为准 |
| **「先复述等确认」最高优先级模式** | robotics-ai-coding-rules · knowledge-base-curation-rules | 同款安全模式,语义保持一致 |
| **MinerU 模式/限制描述** | pdf-converter · document-processing-workflows | 路由层的限制数字以本体为准 |
| **skill 安装/迁移路径约定** | migrate-codex-skills · 《装skill方法总结.md》 · 《README.md 维护约定》 | 统一口径:50_Skills 为权威存放地,软链到 ~/.claude/skills |
| **活文档优先** | yolo-training-params(以 YOLO训练参数手册为准)· personal-dev-workflow(以工作台 docs 为准)· ros2-config-files(以 references/ros2_profile.md 为准) | skill 只沉淀稳定结论,新结论回填活文档 |

## 六、全库共同约定(新增 skill 必须遵守)

1. **目录形状**:`SKILL.md` 必有,frontmatter 带 `name` + 触发词丰富的 `description`(中英触发词都写);可选 `references/`(源笔记)、`scripts/`、`agents/`。
2. **现阶段只用纯知识/规则类 skill**(纯 Markdown,不带 sh 脚本),不在项目内装常驻 skill,统一由 50_Skills 管理后软链(personal-dev-workflow §6)。
3. **安全失效关闭**:通信/传感器丢失→停;急停是硬线;软件安全只是分层之一,永不作为唯一机制(机器人类 skill 共同底线)。
4. **活文档关系**:有上游活文档的 skill 在文首声明权威来源,skill 只放已验证稳定结论。
5. **新增/修改 skill 的同步义务**:① 先入对应分类文件夹;② 更新《README.md》清单;③ 更新《Skill分类总结.md》+ `skill_classification.json`(工作台「Skill 知识库」页读它);④ 更新本文档(一览表 + 对应小结 + 重叠表);⑤ 机器人 10 个 skill 若改了内容,决定是否给上游 `~/robotics-agent-skills` 提 PR(上游与本库副本要保持可互相同步)。

## 七、缺口(有意留白,非遗漏)

README Roadmap 里的 navigation/manipulation/ros2-control/simulation 等方向**尚未建 skill**,当前用既有组合覆盖:仿真 = docker-ros2-development + ros2 + robotics-testing;导航+视觉融合 = ros2 + robot-perception + ros2-config-files(见《Skill分类总结.md》§3/§4)。
