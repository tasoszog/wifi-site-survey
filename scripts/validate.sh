#!/usr/bin/env bash
# validate.sh — Validates data/tasks.json structure.
# Exit 0 = valid, Exit 1 = invalid.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_FILE="${SCRIPT_DIR}/../data/tasks.json"

if [ ! -f "$DATA_FILE" ]; then
    echo "ERROR: tasks.json not found at $DATA_FILE" >&2
    exit 1
fi

# Check valid JSON
if ! python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$DATA_FILE" 2>/dev/null; then
    echo "ERROR: tasks.json is not valid JSON" >&2
    exit 1
fi

# Validate each task has required fields and valid enum values
python3 -c "
import json, sys

REQUIRED = {'id', 'title', 'status', 'priority', 'created_at'}
STATUSES = {'todo', 'in-progress', 'done'}
PRIORITIES = {'low', 'medium', 'high'}

with open(sys.argv[1]) as f:
    tasks = json.load(f)

if not isinstance(tasks, list):
    print('ERROR: root must be an array', file=sys.stderr)
    sys.exit(1)

ids = set()
errors = []
for i, task in enumerate(tasks):
    missing = REQUIRED - set(task.keys())
    if missing:
        errors.append(f'Task {i}: missing fields: {missing}')
    if task.get('status') not in STATUSES:
        errors.append(f'Task {i}: invalid status \"{task.get(\"status\")}\"')
    if task.get('priority') not in PRIORITIES:
        errors.append(f'Task {i}: invalid priority \"{task.get(\"priority\")}\"')
    tid = task.get('id')
    if tid in ids:
        errors.append(f'Task {i}: duplicate id \"{tid}\"')
    ids.add(tid)

if errors:
    for e in errors:
        print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)

print(f'OK: {len(tasks)} tasks validated successfully.')
" "$DATA_FILE"
