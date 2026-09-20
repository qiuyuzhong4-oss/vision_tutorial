---
name: document-processing-workflows
description: Choose and run document processing workflows for PDFs, images, Word, PowerPoint, and Excel-like files, including MinerU pdf-converter, OCR, Markdown extraction, DOCX conversion, table extraction, and fallback between document skills. Use for Chinese or English requests such as 读PDF, 总结文档, PDF转Word, PDF转Markdown, OCR识别, 提取表格, 看这个论文, 文档处理skill怎么用.
---

# Document Processing Workflows

## Routing

Use the toolchain that matches the user's output requirement:

- Use `pdf-converter` with MinerU for broad format conversion, OCR, scanned documents, images, PDF, Word, PowerPoint, spreadsheet-like files, Markdown, JSON, HTML, LaTeX, or DOCX output.
- Use a PDF-structure tool such as pypdf/pdfplumber when the task is specifically editing, splitting, merging, rotating, encrypting, filling, or structurally inspecting PDF files.
- Use DOCX/PPTX/XLSX-specific tooling when the user wants to modify the native Office document itself rather than extract content from it.
- If one workflow fails, times out, loses tables, garbles text, or misses images, try another workflow and compare outputs.

Do not run multiple expensive conversions when a quick extraction already answers a simple question.

## MinerU Setup

The `pdf-converter` workflow requires the external CLI:

```bash
npm i -g mineru-open-api
```

If the command is not found, check that the npm global binary directory is in `PATH`.

Authenticated high-limit mode requires:

```bash
mineru-open-api auth
```

Do not ask the user to paste auth tokens into chat.

## MinerU Modes

Use `flash-extract` by default for quick reading:

- Limit: about 10 MB or 20 pages.
- Output: Markdown.
- Best for quick Q&A, summaries, and direct reading.
- Images, tables, and formulas may become placeholders or reduced Markdown.

Use `extract` for larger or higher-fidelity jobs:

- Limit: about 200 MB or 600 pages.
- Output formats: `md`, `json`, `html`, `latex`, `docx`, or combinations such as `-f md,docx`.
- Best for large files, batch work, preserving tables/images/formulas, and Word conversion.
- Requires `mineru-open-api auth`.

For long jobs, raise timeout deliberately, for example `--timeout 600` if the CLI supports it.

## Language

Choose `--language` when OCR or layout recognition benefits from an explicit language. Common values:

```text
ch, en, japan, korean, chinese_cht, fr, de, es
```

Use `ch` for mixed Chinese and English unless the user specifies otherwise.

## Common Requests

For "look at this PDF", extract Markdown, read the output, and answer from the content.

For "convert to Markdown", write the Markdown output to the requested folder and report the path.

For "convert to Word", use authenticated `extract` with DOCX output. If auth is missing, explain that authentication is required for this mode.

For "extract tables/references", convert to Markdown or JSON first, then parse the relevant sections from the generated output.

For scanned PDFs or images, use OCR-capable conversion first. If OCR is poor, retry with explicit language and higher-fidelity mode.

For files larger than flash limits, use authenticated extract or ask the user to authorize/authenticate the CLI before continuing.

## Troubleshooting

- `mineru-open-api: command not found`: install the CLI or fix `PATH`.
- Auth error in high-limit mode: run `mineru-open-api auth`.
- Timeout on large files: retry with a longer timeout.
- Bad table extraction: try JSON/HTML output or a PDF table tool.
- Garbled multilingual OCR: retry with `--language`.
- Missing images/formulas in Markdown: use authenticated extract and a richer output format.

## Installed Skill Reference

If the user asks where the local `pdf-converter` skill is installed, inspect likely paths:

```bash
find ~/.codex ~/.agents ~/.claude -maxdepth 5 -path '*pdf-converter*' -name SKILL.md -print 2>/dev/null
```

Do not assume the same path across machines. A symlinked install should be resolved before migration.

## Response Pattern

When handling a document task, report:

- Which workflow was used.
- Output file path if a conversion file was created.
- Any quality limitations, such as OCR uncertainty or reduced table fidelity.
- Whether another extraction pass is recommended for tables, formulas, or images.
