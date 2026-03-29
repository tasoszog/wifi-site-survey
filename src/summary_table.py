"""Print a summary table of tasks from data/tasks.json."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def print_summary_table(path: Path = DATA_FILE) -> None:
    """Load tasks and print a summary table grouped by status and priority."""
    with open(path, encoding="utf-8") as f:
        tasks = json.load(f)

    by_status: dict[str, int] = {}
    by_priority: dict[str, int] = {}

    for task in tasks:
        status = task.get("status", "unknown")
        priority = task.get("priority", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1

    print(f"Total tasks: {len(tasks)}\n")

    print(f"{'Status':<15} {'Count':>5}")
    print("-" * 22)
    for status, count in sorted(by_status.items()):
        print(f"{status:<15} {count:>5}")

    print()
    print(f"{'Priority':<15} {'Count':>5}")
    print("-" * 22)
    for priority, count in sorted(by_priority.items()):
        print(f"{priority:<15} {count:>5}")


if __name__ == "__main__":
    print_summary_table()
