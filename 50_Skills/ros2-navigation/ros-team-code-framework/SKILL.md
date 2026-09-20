---
name: ros-team-code-framework
description: RoboMaster vision-team code framework and development discipline - recommended repo layout (docs, script/utils, src with config/launch/decision/driver/localization/msg/nav_bringup/perception/simulation), README conventions, dev-doc-per-iteration with git commits, bug records with screenshots, milestone marking, path portability (no hardcoded absolute paths), gitignore rules, PDF-to-MD before upload. Use when starting a robot vision/navigation project, structuring a team repository, writing development docs, setting up git conventions, or onboarding new vision-group code. Trigger whenever the user mentions 代码框架, 视觉组, 雷达导航, 相机视觉, 决策, decision, 驱动, driver, 感知, perception, localization, nav_bringup, 仿真, simulation, 开发文档, 里程碑, gitignore, 去绝对路径化, 相对路径, RM, RoboMaster, 队伍仓库.
---

# RM 视觉组代码框架与开发纪律

## 最高优先级：写代码前先对齐框架

视觉组分**雷达导航**和**相机视觉**两条线，写代码之前一定要相互对齐代码框架，再动手。

## 推荐仓库框架

```text
project/
├── docs/                  # 各模块程序的说明文档
├── script/ (或 utils/)    # 按项目写的工具
│                          #   导航例：一键获取/更新/维护航点的导航层代码
│                          #   视觉例：定点画框判断固定位是否有物、维护像素点的工具
├── src/                   # 每个包下面都有 config + launch
│   ├── decision/          # 行为树、驱动车特定动作的 src、维护 src 的 include 头文件
│   ├── driver/            # 元件驱动 = 数据的根源：livox 雷达(可测高)、平面雷达、
│   │                      #   D435i 深度相机、USB 相机、海康工业相机(高帧率)
│   ├── localization/
│   ├── msg/               # 自定义消息类型（临时 json 传输接口功耗大，可实验对比）
│   ├── nav_bringup/
│   ├── perception/        # 相机处理程序、sick 数据处理、imu；多相机 pipe 时先定好
│   │                      #   驱动层枚举/控制规范；多一个相机多一个风险，两个顶天
│   └── simulation/        # gazebo 仿真（实机不需要但必须学）；conda + txt 批量装包
├── README.md              # 门面：项目用途 + 各文件夹用处（简单描述清楚即可，
│                          #   技术细节放 docs，别写废话）
└── sh 脚本/               # 测试与实机的统一入口：一次解决 source 环境、激活 conda、
                           #   cd 目录、调度 utils 和 src 的 launch 传参
```

## 开发纪律（每次开发都执行）

1. 每进行一次开发 → **写一次开发文档**记录本次功能 → **提交本地 git**。
2. 测试发现 BUG → 在本次开发文档基础上补充错误原因 → 把报错截图链入 Bug 记录 → 解决后标记已解决。
3. 需求文档里写阶段性目标（里程碑）→ AI 每开发完一个目标就在里程碑后面标记完成。
4. 文档一律用 Markdown 轻量化。

## 工程约定（强制）

- **去绝对路径化**：代码不用绝对路径，用 `path`/`os` 库做相对路径设置——复用性高、部署方便，clone 下来直接编译可用；必要时才上传地图和模型。
- **gitignore 挡住**：地图、缓存数据、plan 文档、根目录规范文档、pdf、编译产物不上传 git。
- **pdf 转 md** 轻量化之后才能上传（说明文档程序不用，自己拷贝一份就好）。
- 仿真代码同样遵守相对路径约定；后续可学 Docker。

## references

- `references/在导航和相机视觉都必须要学的.md` —— 源笔记（另含 ssh/rustdesk/NAS/frp 内网穿透、git 使用等环境工具内容）
