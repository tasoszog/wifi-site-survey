---
name: task-report
description: "Generate a Markdown status report from data/tasks.json. Use when producing sprint summaries, stakeholder updates, or weekly status reports."
argument-hint: "Optional: report scope like 'high priority only' or 'overdue items'"
---

# Task Report Skill

## When to Use

- Generate a weekly or sprint status report.
- Produce a stakeholder summary of project progress.
- Create an overdue-items report for standup meetings.

## Procedure

1. Read `data/tasks.json` to load all current tasks.
2. Cross-reference with `docs/task-tracker-spec.md` for field definitions and SLAs.
3. Compute the following metrics:
   - Total tasks by status (`todo`, `in-progress`, `done`)
   - Tasks by priority
   - Overdue tasks (past `due_date`, not `done`)
   - Workload per assignee
4. Format the report using the [report template](./assets/report-template.md).
5. Apply the output format from [report format reference](./references/report-format.md).

## Output

A single Markdown document ready to share with stakeholders.
