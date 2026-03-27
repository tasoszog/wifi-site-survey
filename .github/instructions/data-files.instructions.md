---
description: "Use when creating or editing JSON data files in data/. Covers task schema validation, required fields, and enum constraints."
applyTo: "data/**/*.json"
---
# Data File Guidelines

- Every task object must include: `id`, `title`, `status`, `priority`, `created_at`.
- `status` must be one of: `todo`, `in-progress`, `done`.
- `priority` must be one of: `low`, `medium`, `high`.
- `due_date` format: `YYYY-MM-DD` (ISO 8601).
- `id` values must be unique — use the pattern `TASK-NNN`.
- Keep the file as a flat JSON array (no nesting, no wrapper object).
- Run `scripts/validate.sh` (or `scripts/validate.ps1` on Windows) after changes.
