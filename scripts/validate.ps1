# validate.ps1 — Validates data/tasks.json structure (Windows variant).
# Exit 0 = valid, Exit 1 = invalid.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataFile  = Join-Path $ScriptDir "..\data\tasks.json"

if (-not (Test-Path $DataFile)) {
    Write-Error "tasks.json not found at $DataFile"
    exit 1
}

try {
    $tasks = Get-Content $DataFile -Raw | ConvertFrom-Json
} catch {
    Write-Error "tasks.json is not valid JSON: $_"
    exit 1
}

$Required   = @("id", "title", "status", "priority", "created_at")
$Statuses   = @("todo", "in-progress", "done")
$Priorities = @("low", "medium", "high")

$ids    = @{}
$errors = @()

for ($i = 0; $i -lt $tasks.Count; $i++) {
    $task = $tasks[$i]
    foreach ($field in $Required) {
        if (-not $task.PSObject.Properties.Name.Contains($field)) {
            $errors += "Task $i : missing field '$field'"
        }
    }
    if ($task.status -notin $Statuses) {
        $errors += "Task $i : invalid status '$($task.status)'"
    }
    if ($task.priority -notin $Priorities) {
        $errors += "Task $i : invalid priority '$($task.priority)'"
    }
    if ($ids.ContainsKey($task.id)) {
        $errors += "Task $i : duplicate id '$($task.id)'"
    }
    $ids[$task.id] = $true
}

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Error $e }
    exit 1
}

Write-Output "OK: $($tasks.Count) tasks validated successfully."
