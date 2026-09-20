---
name: knowledge-base-curation-rules
description: Personal knowledge-base curation rules for RM_Knowledge and RM_AI_Workbench. Use when Codex is asked to organize, restructure, classify, migrate, clean, summarize, or write notes in /home/liantian/RM_Knowledge; adapt /home/liantian/RM_AI_Workbench knowledge workflows; generate formal notes from AI chats, personal notes, other people's notes, PDFs, web clips, or raw Markdown; or change knowledge-base rules, source-trust structure, scan/plan/apply behavior, source citations, or directory layout.
---

# Knowledge Base Curation Rules

## Highest Priority

Before changing knowledge-base content, structure, rules, or workbench code, restate the requested change and wait for explicit confirmation unless the user has already clearly confirmed the exact work.

For every knowledge-base modification:

1. Restate the user's goal.
2. State the expected structure or behavior after the change.
3. State what must remain unchanged.
4. Describe the implementation plan.
5. Show the affected files, folders, or commands.
6. Wait for the user's confirmation before writing.

If the user only asks a question, answer the question. Do not edit files.

## Canonical Structure

Treat `/home/liantian/RM_Knowledge` as the long-term knowledge asset. Its user-facing knowledge modules are only:

```text
RM_Knowledge/
├── 01_正式知识库
├── 02_人工资料
└── 03_AI聊天记录
```

Allowed support folders such as `rules`, `Assets`, `Templates`, `.obsidian`, and `Daily` may exist, but do not describe them as knowledge modules.

Do not recreate `04_待整理` or `05_资料归档` as top-level knowledge modules. If a legacy reference must be preserved for compatibility, redirect it into one of the three modules and document why.

## Trust Model

Use the three modules by trust and processing state:

- `01_正式知识库`: curated formal notes, default retrieval source, organized by knowledge module.
- `02_人工资料`: uncurated or partially curated human-sourced material, including the user's notes and other people's notes.
- `03_AI聊天记录`: unverified AI chat records, organized by AI provider and timestamp.

Do not merge `02_人工资料` and `03_AI聊天记录`. Both are source material, but they must stay separate.

Do not treat AI chat output as formal knowledge until it is verified, rewritten, and cited.

## Formal Note Rules

Formal notes in `01_正式知识库` must:

- Be organized by topic/module, not by source platform.
- Be readable without opening the raw chat or raw source file.
- Include source information that points back to the original material.
- Separate verified facts from assumptions, decisions, and open questions.
- Avoid copying full AI chat transcripts into formal notes.
- Use `99_候选新分支` for uncertain new module suggestions unless the user confirms a new branch.

Use this source block when useful:

```markdown
## 来源传送口

- 来源类型：
- 原始文件：
- Provider：
- Session ID：
- 原始 JSON：
- 作者/链接：
- 整理时间：
- 处理状态：
```

## Workflow

Use the same safety pattern as code changes:

```text
read context -> propose plan -> preview or diff -> confirm -> write -> verify
```

For `RM_AI_Workbench`, prefer the command workflow:

```bash
cd /home/liantian/RM_AI_Workbench
./scripts/rmkb scan
./scripts/rmkb plan --backend llm-cli --model qwen3:4b --source "/path/to/source-or-folder"
./scripts/rmkb apply --plan "/path/to/plan.json"
./scripts/rmkb apply --plan "/path/to/plan.json" --apply
```

Use dry-run previews before permanent writes. Do not batch-apply many generated plans without user review.

## Read Before Editing

Before editing, inspect enough context to avoid breaking the existing knowledge system:

- Current top-level folders under `/home/liantian/RM_Knowledge`.
- Relevant rules under `/home/liantian/RM_Knowledge/rules`.
- Relevant workbench config under `/home/liantian/RM_AI_Workbench/config`.
- Relevant workbench code paths before modifying command behavior.
- Existing files at target paths before creating or overwriting notes.

Prefer `rg`, `find`, and focused file reads. Do not claim a global review if only a small part was inspected.

## Write Boundaries

Protect the original source material:

- Do not overwrite files in `02_人工资料` or `03_AI聊天记录` during formal-note generation.
- Do not delete source files unless the user explicitly asks.
- Do not auto-normalize or rewrite raw chat records.
- Do not create extra top-level knowledge modules without confirmation.
- Do not add unrelated features, UI, dependencies, or abstractions.
- Do not move files just to make the tree look cleaner if links, manifests, or scripts would break.

When a source is low-value or ambiguous, use `needs_review`, `ignore`, or a plan note instead of forcing it into the formal knowledge base.

## Verification

After edits, run the smallest meaningful checks available:

- Verify top-level knowledge folders still match the intended three-module structure.
- Run `./scripts/rmkb scan` after workbench or formal knowledge changes.
- Run Python compile checks after code changes.
- Re-read changed rules/configs to confirm stale `04_待整理` or `05_资料归档` references were not left as active defaults.
- Confirm generated formal notes include source information and do not overwrite existing notes unexpectedly.

If a check cannot be run, say why and state the remaining risk.

## Final Response

Keep the final response concise and include:

- Files or folders changed.
- What changed.
- What stayed unchanged.
- Checks run.
- Any remaining risk or manual review needed.
