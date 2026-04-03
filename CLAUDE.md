# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a workspace for **Claude Code skill development and testing**. It contains the `weekly-report` skill as an example.

## Directory Structure

- `/Users/zly/.claude/skills/weekly-report/` - Original skill definition (do not modify)
- `weekly-report-workspace/` - Working copy for development and testing

## Working with the weekly-report Skill

The `weekly-report` skill generates standard graduate student weekly reports (周报) in Markdown format and can convert them to PDF.

**Key Files:**
- `weekly-report-workspace/SKILL.md` - Skill definition (copy of original for reference)
- `weekly-report-workspace/scripts/md_to_pdf.py` - Markdown to PDF conversion script
- `weekly-report-workspace/evals/evals.json` - Test evaluations

**Common Operations:**
- Edit skills in `/Users/zly/.claude/skills/` (Claude's skills directory)
- Test changes using evaluation prompts in `evals.json`
- Run `python scripts/md_to_pdf.py <input.md> <output.pdf>` to convert reports to PDF

## Report Format

```markdown
**汇报人**：{name}  **汇报周期**：{start_date}-{end_date}

### 本周已完成工作
1. {task}
...

### 后续计划与预期
1. {plan}
...
```
