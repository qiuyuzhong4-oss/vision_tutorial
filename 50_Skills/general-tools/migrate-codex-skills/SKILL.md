---
name: migrate-codex-skills
description: Guide for copying, backing up, installing, and verifying local Codex skills across computers. Use when the user asks whether a skill folder can be copied directly, how to move skills to a new machine, where to place SKILL.md folders, how to handle ~/.codex/skills, $CODEX_HOME/skills, custom skill directories, symlinks, agents/openai.yaml, scripts/references/assets, dependencies, or Chinese requests such as 换电脑使用skill, 迁移skill, 复制skill, 安装skill, 装skill方法.
---

# Migrate Codex Skills

## Core Answer

Copying the skill folder is usually enough only for pure-rule skills, but the target computer must also make that folder discoverable by Codex and satisfy any dependencies.

A valid skill folder must keep this shape:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml       # optional but should be copied if present
├── scripts/              # optional
├── references/           # optional
└── assets/               # optional
```

Always copy the whole `skill-name/` folder, not only `SKILL.md`, unless the skill truly has no extra files.

## Install Methods

Use the simplest installation method that matches the source and target agent:

1. Manual folder install for local skills:

```bash
mkdir -p ~/.codex/skills
cp -a /path/to/skill-name ~/.codex/skills/
```

2. Symlink install when one source folder should be edited in place and reused locally:

```bash
ln -s /path/to/skill-name ~/.codex/skills/skill-name
```

3. Git clone plus copy or symlink when a skill comes from a repo without a supported marketplace or manifest:

```bash
git clone https://github.com/<owner>/<repo>.git
cp -a <repo>/skill-name ~/.codex/skills/
```

4. Tool-specific installers, such as `npx skills add <owner>/<repo>`, only when the target tool explicitly supports that installer and the repo provides the expected manifest.

5. Marketplace or plugin installation only when the user is working in a tool that supports plugin marketplaces. Record the resulting on-disk skill path before migration so the real `SKILL.md` folder can be copied later if needed.

Use `CLAUDE.md`, project instructions, or another always-loaded instruction file instead of a skill when the content is only a short, pure-text preference and does not need scripts, references, assets, metadata, or selective triggering.

## Codex Paths

For Codex, prefer one of these target locations:

```text
${CODEX_HOME}/skills/<skill-name>/SKILL.md
~/.codex/skills/<skill-name>/SKILL.md
```

If the user stores skills in a custom directory such as `~/桌面/skill`, copying there is fine only if the new computer's Codex setup also loads that directory. If unsure, install to `~/.codex/skills` for portability.

Do not confuse Codex paths with Claude paths:

```text
Codex:  ~/.codex/skills/
Claude: ~/.claude/skills/
```

If the user explicitly targets Claude, use Claude paths. If the user targets Codex, use Codex paths.

For Claude-style installs, common locations are:

```text
~/.claude/skills/<skill-name>/SKILL.md
<project>/.claude/skills/<skill-name>/SKILL.md
```

Marketplace-managed Claude skills may live under:

```text
~/.claude/plugins/marketplaces/<marketplace>/<plugin>/skills/<skill-name>/SKILL.md
```

Do not migrate only the marketplace metadata if the goal is to preserve the skill itself; locate and copy the actual skill folder.

## Migration Checklist

Before migrating:

1. Find all local skills:

```bash
find ~/.codex/skills ~/桌面/skill -maxdepth 3 -name SKILL.md -print 2>/dev/null
```

2. Inspect whether each skill has bundled files:

```bash
find /path/to/skill-name -maxdepth 2 -type f -print
```

3. Check for absolute paths or machine-specific assumptions:

```bash
rg -n '(/home/|/Users/|/opt/|/usr/local|桌面|Desktop|CODEX_HOME|\\.codex|\\.claude)' /path/to/skill-name
```

4. Check for external dependencies mentioned by the skill:

```bash
rg -n '(npm|pip|apt|brew|cargo|go install|uv|conda|docker|ollama|mineru|playwright)' /path/to/skill-name
```

## Copy Methods

Use archive-preserving copy for local transfer:

```bash
cp -a /old/path/skill-name ~/.codex/skills/
```

Use `rsync` for cross-machine transfer:

```bash
rsync -a /old/path/skill-name user@host:~/.codex/skills/
```

Use Git for long-term sync when the skill is personal and should evolve over time:

```bash
git init
git add skill-name
git commit -m "Add local Codex skill"
```

Avoid copying the entire `~/.codex` directory unless the user explicitly wants sessions, config, caches, and local state too. Copying only `skills/` is safer.

## Symlink Versus Copy

Use a copy when migrating to another computer or making a stable snapshot:

```bash
cp -a ~/桌面/skill/my-skill ~/.codex/skills/
```

Use a symlink when one source directory should be edited and reused by multiple tools or profiles on the same machine:

```bash
ln -s ~/桌面/skill/my-skill ~/.codex/skills/my-skill
```

When moving symlinked skills to another computer, copy the real source directory, not just the symlink. Validate with:

```bash
ls -la ~/.codex/skills
readlink -f ~/.codex/skills/my-skill
```

Symlinks are good for same-machine development because one edit updates every linked install. Copies are safer for machine migration because they do not break when the original source path is absent.

## Dependencies

Pure rule skills usually need no installation beyond copying the folder.

Tool skills may need extra setup:

- `scripts/` may need executable permissions, Python packages, Node packages, CLI tools, Docker, or system packages.
- `assets/` must be copied if outputs depend on templates, images, fonts, or boilerplate.
- `references/` must be copied if the skill body points to them.
- Secrets should not be stored inside the skill; use environment variables or local config.

After copying, run any dependency install steps documented by the skill. If none are documented but scripts exist, inspect the scripts before running them.

Common dependency patterns:

- Node CLI tools: `npm i -g <tool>`.
- Python libraries: `pip install <package>` or the project's preferred environment manager.
- System packages: `apt`, `brew`, or distro-specific package managers.
- Document conversion tools may require both the skill folder and an external CLI.

## Validation

Validate structure when the skill-creator validator is available:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/<skill-name>
```

If that path does not exist, perform a manual check:

```bash
test -f ~/.codex/skills/<skill-name>/SKILL.md
sed -n '1,20p' ~/.codex/skills/<skill-name>/SKILL.md
```

Then restart the Codex session and check whether the skill appears in the available skills list or invoke it explicitly:

```text
Use $skill-name to ...
```

If the skill does not appear:

- Confirm the folder name matches the `name:` in `SKILL.md`.
- Confirm `SKILL.md` has YAML frontmatter with `name` and `description`.
- Confirm the skill lives under a scanned directory.
- Confirm the session was restarted after copying.

For Claude-style installs, restart the session and check the available skills list in the new conversation. For filesystem verification, use:

```bash
ls -la ~/.claude/skills/
find ~/.claude -name SKILL.md -print
```

To uninstall a manually installed skill, remove the skill folder or symlink and restart the session. To uninstall marketplace-managed skills, prefer the tool's plugin removal command; only delete marketplace folders manually when the user understands the impact.

## Response Pattern

When helping the user migrate skills, answer with:

- Whether direct copy is enough for this skill.
- Exact source and destination paths.
- Whether custom skill directories need new-machine configuration.
- Dependencies or bundled resources that must be copied.
- Validation result or validation commands.
