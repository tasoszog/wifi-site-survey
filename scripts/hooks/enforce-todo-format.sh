#!/usr/bin/env bash
# enforce-todo-format.sh — PostToolUse hook that validates ap_inventory.json after edits.
#
# Receives JSON on stdin from the hook system. Checks if the edited file is
# data/ap_inventory.json; if so, runs validation. Otherwise exits silently.
#
# Exit codes:
#   0  — continue (file not relevant, or validation passed)
#   2  — blocking error (validation failed)

set -euo pipefail

# Read hook payload from stdin
PAYLOAD=$(cat)

# Extract the file path that was edited (toolName = "editFiles" or "createFile")
TOOL_NAME=$(echo "$PAYLOAD" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('toolName',''))" 2>/dev/null || echo "")

# Only act on file-edit tools
case "$TOOL_NAME" in
    editFiles|createFile) ;;
    *) exit 0 ;;
esac

# Check if any of the edited files is ap_inventory.json
IS_AP_FILE=$(echo "$PAYLOAD" | python3 -c "
import json, sys
d = json.load(sys.stdin)
result = d.get('toolResult', {})
files = result.get('filePaths', result.get('files', []))
if isinstance(files, str):
    files = [files]
for f in files:
    if 'ap_inventory.json' in str(f):
        print('yes')
        sys.exit(0)
print('no')
" 2>/dev/null || echo "no")

if [ "$IS_AP_FILE" != "yes" ]; then
    exit 0
fi

# Run validation
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALIDATE="${SCRIPT_DIR}/../validate.sh"

if bash "$VALIDATE"; then
    echo '{"decision": "continue"}' 
else
    echo "ERROR: ap_inventory.json validation failed after edit." >&2
    exit 2
fi
