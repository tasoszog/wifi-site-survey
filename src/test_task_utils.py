"""Unit tests for the count_overdue function in task_utils."""

import pytest
from datetime import date
from task_utils import count_overdue, filter_by_assignee


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TODAY = date(2024, 6, 15)


def make_task(status: str, due_date: str | None) -> dict:
    """Helper to build a minimal task dict."""
    task = {"status": status}
    if due_date is not None:
        task["due_date"] = due_date
    return task


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_empty_list_returns_zero():
    """No tasks → count is 0."""
    assert count_overdue([], today=TODAY) == 0


def test_single_overdue_task():
    """One task past due date and not done → count is 1."""
    tasks = [make_task("todo", "2024-06-01")]
    assert count_overdue(tasks, today=TODAY) == 1


def test_single_done_task_not_counted():
    """A done task past due date is NOT counted as overdue."""
    tasks = [make_task("done", "2024-01-01")]
    assert count_overdue(tasks, today=TODAY) == 0


def test_due_today_not_overdue():
    """A task due exactly today is NOT overdue (strict less-than)."""
    tasks = [make_task("todo", "2024-06-15")]
    assert count_overdue(tasks, today=TODAY) == 0


def test_due_in_future_not_overdue():
    """A task due in the future is NOT overdue."""
    tasks = [make_task("in-progress", "2024-12-31")]
    assert count_overdue(tasks, today=TODAY) == 0


def test_multiple_mixed_tasks():
    """Only non-done, past-due tasks are counted."""
    tasks = [
        make_task("todo", "2024-05-01"),        # overdue ✓
        make_task("in-progress", "2024-06-01"), # overdue ✓
        make_task("done", "2024-01-01"),         # done — skip
        make_task("todo", "2024-06-15"),         # due today — skip
        make_task("todo", "2024-12-01"),         # future — skip
    ]
    assert count_overdue(tasks, today=TODAY) == 2


def test_task_without_due_date_not_counted():
    """A task with no due_date field is NOT counted."""
    tasks = [make_task("todo", None)]
    assert count_overdue(tasks, today=TODAY) == 0


def test_all_done_tasks_returns_zero():
    """All done tasks → count is 0 regardless of due dates."""
    tasks = [
        make_task("done", "2024-01-01"),
        make_task("done", "2023-06-15"),
    ]
    assert count_overdue(tasks, today=TODAY) == 0


def test_uses_real_today_when_not_provided():
    """When today is not injected, function uses date.today() without error."""
    tasks = [make_task("todo", "2000-01-01")]  # always in the past
    result = count_overdue(tasks)
    assert result == 1


def test_in_progress_overdue_counted():
    """in-progress tasks past due date ARE counted."""
    tasks = [make_task("in-progress", "2024-03-01")]
    assert count_overdue(tasks, today=TODAY) == 1


def test_all_overdue_counted():
    """All non-done past-due tasks are counted correctly."""
    tasks = [
        make_task("todo", "2024-01-01"),
        make_task("todo", "2024-02-01"),
        make_task("todo", "2024-03-01"),
    ]
    assert count_overdue(tasks, today=TODAY) == 3


def test_mixed_with_missing_due_dates():
    """Mix of tasks with and without due_date — only valid overdue ones counted."""
    tasks = [
        make_task("todo", "2024-05-01"),  # overdue ✓
        make_task("todo", None),           # no due_date — skip
        make_task("todo", "2024-07-01"),  # future — skip
    ]
    assert count_overdue(tasks, today=TODAY) == 1


# ---------------------------------------------------------------------------
# filter_by_assignee tests
# ---------------------------------------------------------------------------

def make_assignee_task(assignee) -> dict:
    """Helper to build a minimal task dict with an assignee."""
    task = {"status": "todo", "title": "test"}
    if assignee is not None:
        task["assignee"] = assignee
    return task


def test_assignee_empty_list():
    """Empty task list returns empty list."""
    assert filter_by_assignee([], "alice") == []


def test_assignee_single_match():
    """One matching task is returned."""
    tasks = [make_assignee_task("alice")]
    assert filter_by_assignee(tasks, "alice") == tasks


def test_assignee_no_match():
    """Unknown assignee returns empty list without raising."""
    tasks = [make_assignee_task("alice"), make_assignee_task("bob")]
    assert filter_by_assignee(tasks, "charlie") == []


def test_assignee_case_insensitive():
    """Lookup is case-insensitive — 'Alice' matches stored 'alice'."""
    tasks = [make_assignee_task("alice")]
    assert filter_by_assignee(tasks, "Alice") == tasks
    assert filter_by_assignee(tasks, "ALICE") == tasks


def test_assignee_null_skipped():
    """Tasks with assignee: null are not returned."""
    tasks = [make_assignee_task(None)]
    # null assignee stored as key with None value
    tasks[0]["assignee"] = None
    assert filter_by_assignee(tasks, "alice") == []


def test_assignee_missing_field_skipped():
    """Tasks with no assignee key are not returned."""
    task = {"status": "todo", "title": "no assignee key"}
    assert filter_by_assignee([task], "alice") == []


def test_assignee_multiple_matches():
    """All tasks for the requested assignee are returned."""
    alice1 = make_assignee_task("alice")
    alice2 = make_assignee_task("alice")
    bob = make_assignee_task("bob")
    result = filter_by_assignee([alice1, bob, alice2], "alice")
    assert result == [alice1, alice2]


def test_assignee_mixed_tasks():
    """Only the requested assignee's tasks are returned from a mixed list."""
    tasks = [
        make_assignee_task("alice"),
        make_assignee_task("bob"),
        make_assignee_task("charlie"),
        make_assignee_task("alice"),
    ]
    result = filter_by_assignee(tasks, "alice")
    assert len(result) == 2
    assert all(t["assignee"] == "alice" for t in result)