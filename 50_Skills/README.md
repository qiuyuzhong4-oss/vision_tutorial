# 50_Skills · AI Agent Skill 统一管理区

> 所有 AI agent skill（Claude / Codex 等）的**唯一权威存放地**：按「什么项目用什么类型的 skill」分类。
> 使用/安装方法见同目录《装skill方法总结.md》，分类详情见《Skill分类总结.md》（工作台「Skill 知识库」页面读取的是它的同步副本）。

## 目录结构

```text
50_Skills/
├── README.md                  # 本文件
├── Skill分类总结.md            # 分类总纲 v0.2
├── 装skill方法总结.md          # 安装方式速查（个人级/项目级/市场/伪 skill）
├── ros2-navigation/           # ROS2 导航 / 整车 / 机器人软件
├── camera-perception/         # 相机视觉 / 感知
├── general-tools/             # 通用工具 / Web / 环境运维
└── knowledge-curation/        # 知识库 / 文档整理
```

## Skill 清单

### ros2-navigation/（ROS2 导航 / 整车 / 机器人软件）

| Skill | 状态 | 来源 |
|-------|------|------|
| ros2 | 已有 | ~/robotics-agent-skills 仓库 |
| ros1 | 已有 | 同上（旧版维护/迁移用） |
| robot-bringup | 已有 | 同上 |
| robotics-design-patterns | 已有 | 同上（架构模式：行为树/状态机/安全系统） |
| robotics-software-principles | 已有 | 同上（机器人软件设计原则） |
| robotics-security | 已有 | 同上（SROS2/DDS 安全加固） |
| robotics-testing | 已有 | 同上 |
| docker-ros2-development | 已有 | 同上 |
| robotics-ai-coding-rules | 已有 | 桌面 skill/（AI 先复述再动手） |
| publish-git-repositories | 已有 | 桌面 skill/（gitignore/发布约定） |
| **ros2-config-files** | **本次生成** | 提炼自 30_Knowledge/Universal_robotics/ros2_profile.md |
| **ros2-thread-naming** | **本次生成** | 提炼自 CPU资源查询工具.md + 程序资源区分查询工具及方法/ |
| **ros-team-code-framework** | **本次生成** | 提炼自 在导航和相机视觉都必须要学的.md |

### camera-perception/（相机视觉 / 感知）

| Skill | 状态 | 来源 |
|-------|------|------|
| robot-perception | 已有 | ~/robotics-agent-skills 仓库 |
| **yolo-training-params** | **本次生成** | 提炼自 computer-vision/YOLO训练参数手册.md（活文档，skill 内已声明以活文档为准） |

### general-tools/（通用工具 / Web / 环境运维）

| Skill | 状态 | 来源 |
|-------|------|------|
| document-processing-workflows | 已有 | 桌面 skill/ |
| fix-linux-proxy-dns | 已有 | 桌面 skill/ |
| configure-codex-profile-keys | 已有 | 桌面 skill/ |
| migrate-codex-skills | 已有 | 桌面 skill/ |
| ros2-web-integration | 已有 | ~/robotics-agent-skills 仓库（rosbridge/WebSocket 仪表盘） |
| **personal-dev-workflow** | **本次生成** | 提炼自工作台四份开发文档（需求五要素/六步流程/文档分离/README 三阶段/开发纪律/现阶段 skill 约定） |

### knowledge-curation/（知识库 / 文档整理）

| Skill | 状态 | 来源 |
|-------|------|------|
| knowledge-base-curation-rules | 已有 | 桌面 skill/ |
| pdf-converter | 已有 | ~/.agents/skills（npx skills add 安装） |

## 安装方式（装法详见《装skill方法总结.md》）

```bash
# 个人级（对所有项目生效）：软链，改一处全生效
ln -s ~/vision_tutorial/50_Skills/ros2-navigation/ros2-config-files ~/.claude/skills/ros2-config-files

# 项目级（只对当前项目生效，可随 git 分享）
ln -s ~/vision_tutorial/50_Skills/ros2-navigation/ros2-config-files <项目>/.claude/skills/ros2-config-files
```

## 维护约定

1. 新 skill 先放进对应分类文件夹（新建分类需同步《Skill分类总结.md》），再软链安装。
2. 从笔记提炼新 skill 时：SKILL.md 放稳定结论，源笔记放 `references/`；**活文档类只引用不复制**（如 YOLO 参数手册），避免双份失同步。
3. 仿真类、导航+视觉融合类项目没有专属 skill：分别复用 ros2-navigation 与 camera-perception 里的组合，见分类总结。
4. 源笔记 originals 仍在 `30_Knowledge/` 不动，这里管理的是 skill 形态。
