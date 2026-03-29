# WiFi Site-Survey Toolkit — Copilot Features Demo

This is a minimal WiFi site-survey toolkit used to demonstrate every GitHub
Copilot customization primitive. See `docs/wifi-survey-spec.md` for the domain spec.

## Structure

| Folder     | Purpose                                              |
|------------|------------------------------------------------------|
| `data/`    | AP inventory data (`ap_inventory.json`)              |
| `docs/`    | Specifications and design documents                  |
| `src/`     | Python utilities for loading and analysing AP data   |
| `scripts/` | Validation and automation scripts                    |

## Conventions

- **Data format**: JSON arrays in `data/`. Validated by `scripts/validate.sh`.
- **Python style**: snake_case, type hints encouraged, docstrings on public functions.
- **Documentation**: Markdown only. Link to spec docs rather than duplicating content.
- **No secrets**: Never commit credentials. Use environment variables where needed.

## Quick Start

```bash
# Validate the AP inventory data
bash scripts/validate.sh        # macOS / Linux
powershell scripts/validate.ps1 # Windows

# Run WiFi utilities
python src/wifi_utils.py
```
