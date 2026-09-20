# Skill 分类总结（v0.3）：什么项目用什么类型的 Skill

> v0.3 ｜ 2026-09-17 ｜ 权威数据：同目录 `skill_classification.json`（工作台「Skill 知识库」页面读取的是它的同步副本）
>
> 相比 v0.2：新增 `personal-dev-workflow`（从工作台四份开发文档提炼的个人开发流程规范）。
> 相比 v0.1：原「建议新建」的 4 个 skill 已提炼完成入库；补充登记 5 个此前未列入的 robotics skill；统一管理区确定在 `~/vision_tutorial/50_Skills/`。

## 0. 使用方法

- 所有 skill 的**唯一权威存放地**是 `~/vision_tutorial/50_Skills/`，按分类文件夹组织；安装用软链（个人级 `~/.claude/skills/` 或项目级 `<项目>/.claude/skills/`），装法见同目录《装skill方法总结.md》。
- 不确定某个项目算哪类时，按「主要工作量在哪」归类：跑在 ROS2 上 → 导航/整车/感知类；纯 Python/Node 工具 → 通用工具类。
- 仿真类、导航+视觉融合类没有专属 skill，用 ros2-navigation 与 camera-perception 组合覆盖。

## 1. ROS2 导航 / 整车项目

**典型项目**：RC2026 整车、雷达站导航、Nav2 建图定位、行为树决策。
**位置**：`50_Skills/ros2-navigation/`

| Skill | 状态 | 用途 |
|-------|------|------|
| ros2 / ros1 | 已有 | ROS2 通用规范 / ROS1 旧系统维护迁移 |
| robot-bringup | 已有 | 整车启动组织 |
| robotics-design-patterns | 已有（本次登记） | 架构模式：行为树/状态机/安全系统 |
| robotics-software-principles | 已有（本次登记） | 机器人模块设计原则 |
| robotics-security | 已有（本次登记） | SROS2/DDS 安全加固 |
| robotics-testing / docker-ros2-development | 已有 | 测试 / 容器化环境 |
| robotics-ai-coding-rules | 已有 | AI 先复述再动手（桌面 skill 迁入） |
| publish-git-repositories | 已有 | gitignore 约定（桌面 skill 迁入） |
| **ros2-config-files** | **已生成** | 18 类配置文件职责 +「配置问题伪装成算法问题」排查（源：ros2_profile.md） |
| **ros2-thread-naming** | **已生成** | 进程/线程命名可观测性 + htop 设置 + 给 AI 的话术（源：CPU资源查询工具等） |
| **ros-team-code-framework** | **已生成** | 视觉组代码框架 + 开发纪律 + 去绝对路径化/gitignore/pdf→md（源：在导航和相机视觉都必须要学的.md） |

## 2. 相机视觉 / 感知项目

**典型项目**：D435i、海康工业相机、AprilTag、YOLO、标定/手眼标定、九宫格空位判断。
**位置**：`50_Skills/camera-perception/`

| Skill | 状态 | 用途 |
|-------|------|------|
| robot-perception | 已有 | 感知算法 |
| **yolo-training-params** | **已生成** | YOLO 训练参数 RM 速查（源：YOLO训练参数手册.md 活文档，skill 以活文档为准） |
| ros2-thread-naming（复用） | 已生成 | 多相机多 pipe 并发排查 |

**你的笔记约定**：多一个相机就多一个风险，两个顶天；驱动层枚举/控制相机的规范要提前定；定点画框维护像素点这类工具放 script(utils) 层（已沉淀进 ros-team-code-framework）。

## 3. 仿真项目（Gazebo / Ignition）

复用 `docker-ros2-development` + `ros2` + `robotics-testing`。
**约定**：仿真代码不用绝对路径，用 path/os 做相对路径，clone 即编译；conda + txt 批量装包；算法节点与实车一致，差异放仿真配置与 launch。

## 4. 导航 + 视觉融合定位

组合 `ros2` + `robot-perception` + **ros2-config-files**：融合定位出问题先查 URDF/Xacro 的 frame 与安装位置、再查标定 YAML——很多「算法问题」其实是配置问题。
参考写法：需求总文档 §2 相机定位九宫格案例（订阅 base_link → 记点取相对位置 → 标记角点 → 按格距偏移判空）。

## 5. 通用工具 / Web 工作台 / 脚本项目

**位置**：`50_Skills/general-tools/`（+ 跨分类复用 robotics-ai-coding-rules、publish-git-repositories）

| Skill | 状态 | 用途 |
|-------|------|------|
| document-processing-workflows | 已有 | 文档批处理 |
| fix-linux-proxy-dns | 已有 | 环境/代理/DNS 运维 |
| configure-codex-profile-keys / migrate-codex-skills | 已有 | Codex 工具链运维 |
| ros2-web-integration | 已有（本次登记） | rosbridge/WebSocket 机器人 Web 仪表盘 |
| **personal-dev-workflow** | **已生成（v0.3）** | 个人开发流程规范：需求五要素、六步流程、文档职责分离、README 三阶段、开发纪律、现阶段 skill 约定（源：工作台四份开发文档） |

## 6. 知识库 / 文档整理

**位置**：`50_Skills/knowledge-curation/`

| Skill | 状态 | 用途 |
|-------|------|------|
| knowledge-base-curation-rules | 已有 | 知识库整理规则 |
| pdf-converter | 已安装 | PDF→MD 轻量化后才上传 git |

## 7. 跨项目通用规则（已沉淀进 skill）

1. 写代码前先对齐代码框架 → **ros-team-code-framework**
2. 项目必须**去绝对路径化**（不写死 `/home/xxx`，脚本位置推导 / path、os 相对路径）→ **ros-team-code-framework**
3. 给 AI 下工程任务带可观测性与验证要求 → **ros2-thread-naming**
4. 每次开发写开发文档并提交 git；BUG 记录含原因+手法+截图；里程碑逐个标记 → **ros-team-code-framework**
5. pdf 转 md 后才上传 git；地图/缓存/编译产物 gitignore → **ros-team-code-framework** + **publish-git-repositories**
6. 现阶段只用纯知识/规则类 skill（不带 sh 脚本），不在项目内装常驻 skill；项目内引用 skill 知识用工作台拖入扁平化为 `<功能名>.md` → **personal-dev-workflow**

## 8. 安装方式速查（详见《装skill方法总结.md》）

| 方式 | 命令/位置 | 适用 |
|------|-----------|------|
| 统一管理区 | `~/vision_tutorial/50_Skills/` | 所有 skill 的权威存放地，先入库再软链 |
| 个人级 | `~/.claude/skills/<skill>/SKILL.md`（建议软链到 50_Skills） | 所有项目生效 |
| 项目级 | `<项目>/.claude/skills/<skill>/SKILL.md` | 当前项目生效，可随 git 分享 |
| manifest | `npx skills add <user>/<repo>` | 仓库带 manifest |
| 插件市场 | `/plugin marketplace add <github-url>` | 官方/第三方合集 |
| 伪 skill | 写进 CLAUDE.md / AGENTS.md | 纯文字约定 |

## 9. 待办

无待生成项。后续新 skill 按《README.md》维护约定：先入分类文件夹（同步分类总结），再软链安装。
