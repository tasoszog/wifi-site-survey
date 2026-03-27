---
description: "Summarize tasks from data/tasks.json — counts by status and priority, list overdue items, and highlight blockers."
argument-hint: "Optional: path to tasks.json or filter criteria (e.g., 'only high priority')"
---
Read the task data from `data/tasks.json` and produce a summary report:

1. **Counts** — Total tasks, broken down by status (`todo`, `in-progress`, `done`) and priority (`high`, `medium`, `low`).
2. **Overdue** — List any tasks where `due_date` is before today and `status` is not `done`. Show id, title, due date, and assignee.
3. **In-progress** — List tasks currently being worked on, grouped by assignee.
4. **Blockers** — Flag any high-priority tasks that are still `todo`.

Format the output as a clear Markdown table or bullet list.
