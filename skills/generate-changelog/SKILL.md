---
name: generate-changelog
description: Automatically inspects git commit history since the latest tag and generates a structured, categorized CHANGELOG.md adhering to Keep a Changelog standards.
tools:
  - bash
---

# Generate Changelog Skill

This skill automates the extraction and categorization of git commit logs to produce a release-ready `CHANGELOG.md`.

## When to Use
Trigger this skill whenever you need to:
- Draft release notes before cutting a new tag.
- Summarize changes across multiple pull requests.
- Update `CHANGELOG.md` following conventional commit conventions (`feat`, `fix`, `refactor`, `perf`, `chore`).

## Usage

### Option 1: Native CLI
Run either the Python generator (cross-platform) or the Bash script:
```bash
# Using Python
python skills/generate-changelog/changelog.py --version v1.0.0

# Using Bash
bash skills/generate-changelog/changelog.sh CHANGELOG.md v1.0.0
```

### Option 2: Within Claude Code
Invoke the command:
```
/generate-changelog
```
The skill automatically detects git commits, groups them into:
- **`Added`**: New features and capabilities.
- **`Fixed`**: Bug fixes and patches.
- **`Changed`**: Refactoring and optimizations.
- **`Removed`**: Deprecated or deleted functionality.
- **`Maintenance`**: Tooling, CI, and documentation updates.

And prepends the output directly to `CHANGELOG.md`.
