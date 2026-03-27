"""Minimal task tracker utilities for the Copilot features demo."""

import json
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"

VALID_STATUSES = {"todo", "in-progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


def load_tasks(path=None):
    """Load tasks from the JSON data file."""
    path = path or DATA_FILE
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_by_status(tasks, status):
    """Return tasks matching the given status."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}")
    return [t for t in tasks if t.get("status") == status]


def count_overdue(tasks, today=None):
    """Count tasks that are past their due date and not done."""
    today = today or date.today()
    count = 0
    for task in tasks:
        if task.get("status") == "done":
            continue
        due = task.get("due_date")
        if due:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
            if due_date < today:
                count += 1
    return count


def summary(tasks):
    """Return a dict summarizing task counts by status and priority."""
    by_status = {}
    by_priority = {}
    for task in tasks:
        s = task.get("status", "unknown")
        p = task.get("priority", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
        by_priority[p] = by_priority.get(p, 0) + 1
    return {"total": len(tasks), "by_status": by_status, "by_priority": by_priority}


if __name__ == "__main__":
    tasks = load_tasks()
    print(json.dumps(summary(tasks), indent=2))
