---
name: personal-dev-workflow
description: Personal development workflow rules distilled from the workbench requirement docs - required five sections for a new requirement doc (使用场景, 解决的问题, 接口定义, 阶段性目标, 最终目标), the requirement-refinement loop (draft -> external AI discussion -> refined spec -> AI restatement -> dev doc with borrowable projects / tech chain / framework), document separation (total docs vs single/archive requirements vs rules), README three-stage writing, per-iteration dev doc + git commit discipline, bug record format (cause + fix + screenshot), and current-stage skill conventions. Use when starting or planning a project, writing requirement or dev docs, updating milestones, recording bugs, or deciding how skills should be used in a project. Trigger whenever the user mentions 需求文档, 开发文档, 工作台, 工作流, 使用场景, 接口定义, 里程碑, 阶段性目标, 最终目标, 复述需求, README, bug 记录, 修 bug, 开发纪律, 规则文档, 总文档, 新项目.
---

# 个人开发工作流规范（提炼自工作台四份开发文档）

## 1. 新项目需求文档五要素（必填，缺一不可）

使用场景 ｜ 解决的问题 ｜ 接口定义 ｜ 阶段性目标（里程碑，写成可勾选清单） ｜ 最终目标

## 2. 需求完善流程（不要直接开写代码）

草稿开发文档 → 发外部 AI（Grok/智谱）讨论有没有可借鉴的开源项目（不懂的概念**新开对话**问，别弄脏需求上下文） → 完善需求 → 让 AI 重新输出一份规范需求文档 → 把新文档发给 AI **复述确认** → 确认后才生成开发文档。

开发文档必须包含：可借鉴项目、技术链、项目框架（具体到文件夹放什么文件，方案名称直接附在文件夹名旁）、**详细技术实现链路单独成文**。

## 3. 文档职责分离

- 总文档三件套（`docs/requirements` 总需求、`docs/framework` 框架、`docs/tech-chain` 技术链路）**不常修改**：改需求只改总需求文档，改技术链路只改总技术链路文档。
- 单次开发需求 → `requirements/single/{名称}_需求.md`；第一版讨论稿与中间版本 → `requirements/archive/`（历史只读，不再修改）。
- `rules/` 只放协定规则条目（短、稳定），**不放 skill 实体**。

## 4. 每次开发纪律

1. 开发完 → 更新开发文档记录本次功能 → 提交本地 git。
2. 测试出 BUG → 在开发文档基础上补充错误原因，把报错截图链入 `bugs/`（每份 Bug 文档必须含：**报错原因 + 修复手法 + 截图**），解决后标记已解决。
3. 需求文档里的里程碑，每完成一个立即标记。

## 5. README 三阶段

- 项目刚启动：最简 README（标题 + 一句话描述 + 安装/启动命令 + 「详细需求见 xxx，开发文档见 xxx」传送门）。
- 功能相对稳定：补充使用说明、配置项、常见问题。
- 准备交付/开源：再打磨（截图、更清晰示例、贡献指南）。
- README 与需求/开发文档职责分离，不互相替代。

## 6. 现阶段 Skill 使用约定

- 只使用**纯知识/规则类** skill（纯 Markdown）；现阶段不用带 sh 脚本的 skill 作为开发规则。
- **不在项目内安装常驻 skill**（不往 `<项目>/.claude/skills/` 或项目目录装 skill 实体）；skill 统一由 `~/vision_tutorial/50_Skills/` 管理，需要时软链到个人级 `~/.claude/skills/`。
- 项目内要引用某个 skill 的知识 → 用工作台把 skill 文件夹拖入 `rules/`，自动扁平化为 `<功能名>.md`（剥离 references/脚本，附来源注脚指向完整版）。
- 这是现阶段取舍；后续要用脚本型/常驻 skill 时，回到总需求文档修改该条并同步《Skill 分类总结》。

## 来源（活文档，更新以这些为准）

- `~/workbench/docs/requirements/工作台需求总文档.md`（§4.3 流程引导、§4.6 Skill 使用约定）
- `~/workbench/docs/framework/工作台框架文档.md`、`~/workbench/docs/tech-chain/工作台技术链路文档.md`
- `~/workbench/requirements/archive/第一版需求初稿.md`（原始讨论稿，只读）
