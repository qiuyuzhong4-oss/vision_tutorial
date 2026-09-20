# 装 skill 的几种方法(总结)

## 1. 手动放到个人/项目目录(最直接)

适合:自己写 SKILL.md,或拿到现成文件夹。

**个人级**(对所有项目生效)
```
~/.claude/skills/<skill-name>/SKILL.md
```
当前的 `pdf-converter` 就是这样装的(还是个**软链**到 `~/.agents/skills/pdf-converter`)。

**项目级**(只对当前项目生效,可随 git 分享)
```
<项目>/.claude/skills/<skill-name>/SKILL.md
```
适合团队约定。

**软链 vs 拷贝:**
- 软链:一份源多处用,改一处全生效
- 拷贝:每处独立,互不影响

## 2. Git clone + 手动放

仓库作者没做 npx manifest、但又想用现成的场景。

```bash
git clone https://github.com/xxx/some-skill.git
ln -s $(pwd)/some-skill ~/.claude/skills/some-skill
# 或直接拷
cp -r some-skill ~/.claude/skills/
```

## 3. `npx skills add`(标准 manifest)

```bash
npx skills add <github-user>/<repo>
```

- 一些 skill 仓库带 `skills.json` 之类的 manifest,可以走这条
- `pdf-converter` 的 README 就推荐了这条(`npx skills add tanis90/pdf-converter-mineru`)

## 4. 插件市场

**装市场本身**(`/plugin` 命令或 `settings.json`):
```bash
/plugin marketplace add <github-url>
```

**已装的市场**(在 `~/.claude/plugins/marketplaces/`):
- `anthropic-agent-skills` — Anthropic 官方,18 个 skill
- `claude-plugins-official` — 另一个官方合集,30+ skill(分属 discord/imessage/telegram/plugin-dev/...)

**市场里 skill 的存放路径:**
```
~/.claude/plugins/marketplaces/<市场>/<插件>/skills/<skill>/SKILL.md
```

## 5. 写在 CLAUDE.md(伪 skill)

不算 skill,但效果类似:把"长期约定"写进 `CLAUDE.md`(项目级)或 `~/.claude/CLAUDE.md`(个人级),system prompt 每次都读。

适合:**纯文字**约定 — 编码规范、个人偏好。不附带脚本/CLI 的就别费劲做 skill 了。

---

## 验证 / 卸载

| 操作 | 怎么搞 |
|---|---|
| **看装了哪些** | 重启会话,看 system prompt 顶部 "available skills" 列表 |
| **看实际文件** | `ls -la ~/.claude/skills/` + `find ~/.claude -name SKILL.md` |
| **卸载个人/项目级** | 删文件夹/软链,重启会话 |
| **卸载市场级** | `/plugin remove <插件名>`,或删 `~/.claude/plugins/marketplaces/<市场>` |

---

## 装好之后通常还要装依赖

skill 的 SKILL.md 里一般会写"先跑 npm i / pip install"这种。
- **工具类**(pdf-converter、pptx 等)要装 CLI:`npm i -g ...` 或 `pip install ...`
- **纯规则类**(只规定行为的)不用装东西
