# Task Tracker — Specification

A minimal task tracker used as the domain context for this Copilot features demo.

## Task Fields

| Field        | Type     | Required | Description                          |
|--------------|----------|----------|--------------------------------------|
| `id`         | string   | Yes      | Unique identifier (e.g., `TASK-001`) |
| `title`      | string   | Yes      | Short summary of the task            |
| `status`     | enum     | Yes      | One of: `todo`, `in-progress`, `done`|
| `priority`   | enum     | Yes      | One of: `low`, `medium`, `high`      |
| `assignee`   | string   | No       | Person responsible                   |
| `due_date`   | ISO 8601 | No       | Deadline (`YYYY-MM-DD`)              |
| `tags`       | string[] | No       | Freeform labels                      |
| `created_at` | ISO 8601 | Yes      | When the task was created            |

## Statuses

```
todo  ──►  in-progress  ──►  done
```

- **todo** — not started
- **in-progress** — actively being worked on (max 3 per assignee)
- **done** — completed, cannot transition back

## Priorities

| Priority | SLA (business days) |
|----------|---------------------|
| high     | 2                   |
| medium   | 5                   |
| low      | 10                  |

## Data File

All tasks are stored in `data/tasks.json` as a JSON array. Each element is a task
object matching the fields above.

## Validation Rules

1. Every task must have `id`, `title`, `status`, `priority`, and `created_at`.
2. `status` must be one of the three valid values.
3. `priority` must be one of the three valid values.
4. `due_date`, if present, must be a valid `YYYY-MM-DD` string.
5. `id` values must be unique across all tasks.
