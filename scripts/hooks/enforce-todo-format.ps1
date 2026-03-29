# enforce-todo-format.ps1 — PostToolUse hook that validates ap_inventory.json after edits.
#
# Receives JSON on stdin from the hook system. Checks if the edited file is
# data/ap_inventory.json; if so, runs validation. Otherwise exits silently.
#
# Exit codes:
#   0  — continue (file not relevant, or validation passed)
#   2  — blocking error (validation failed)

$ErrorActionPreference = "Stop"

# Read hook payload from stdin
$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try {
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0
}

# Only act on file-edit tools
$toolName = $payload.toolName
if ($toolName -notin @("editFiles", "createFile")) { exit 0 }

# Check if any edited file is ap_inventory.json
$result = $payload.toolResult
$files = @()
if ($result.filePaths) { $files = $result.filePaths }
elseif ($result.files)  { $files = $result.files }

$isApFile = $false
foreach ($f in $files) {
    if ($f -like "*ap_inventory.json*") { $isApFile = $true; break }
}
if (-not $isApFile) { exit 0 }

# Run validation
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ValidateScript = Join-Path $ScriptDir "..\validate.ps1"

try {
    & powershell -ExecutionPolicy Bypass -File $ValidateScript
    Write-Output '{"decision": "continue"}'
} catch {
    Write-Error "ap_inventory.json validation failed after edit."
    exit 2
}
