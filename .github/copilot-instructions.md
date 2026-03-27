# Task Tracker — Copilot Features Demo

This is a minimal task-tracker project used to demonstrate every GitHub Copilot
customization primitive. See `docs/task-tracker-spec.md` for the domain spec.

## Structure

| Folder     | Purpose                                          |
|------------|--------------------------------------------------|
| `data/`    | Task data (`tasks.json`)                         |
| `docs/`    | Specifications and design documents              |
| `src/`     | Python utilities for loading and querying tasks  |
| `scripts/` | Validation and automation scripts                |

## Conventions

- **Data format**: JSON arrays in `data/`. Validated by `scripts/validate.sh`.
- **Python style**: snake_case, type hints encouraged, docstrings on public functions.
- **Documentation**: Markdown only. Link to spec docs rather than duplicating content.
- **No secrets**: Never commit credentials. Use environment variables where needed.

## Quick Start

```bash
# Validate the task data
bash scripts/validate.sh        # macOS / Linux
powershell scripts/validate.ps1 # Windows

# Run task utilities
python src/task_utils.py
```
