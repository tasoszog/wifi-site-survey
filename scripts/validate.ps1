# validate.ps1 — Validates data/ap_inventory.json structure (Windows variant).
# Exit 0 = valid, Exit 1 = invalid.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataFile  = Join-Path $ScriptDir "..\data\ap_inventory.json"

if (-not (Test-Path $DataFile)) {
    Write-Error "ap_inventory.json not found at $DataFile"
    exit 1
}

try {
    $aps = Get-Content $DataFile -Raw | ConvertFrom-Json
} catch {
    Write-Error "ap_inventory.json is not valid JSON: $_"
    exit 1
}

$Required   = @("ap_id", "ssid", "bssid", "channel", "band", "tx_power", "location", "status", "firmware_version")
$Statuses   = @("planned", "deployed", "offline", "decommissioned")
$Bands      = @("2.4 GHz", "5 GHz", "6 GHz")
$Qualities  = @("good", "marginal", "critical")

$ids    = @{}
$bssids = @{}
$errors = @()

for ($i = 0; $i -lt $aps.Count; $i++) {
    $ap = $aps[$i]
    foreach ($field in $Required) {
        if (-not $ap.PSObject.Properties.Name.Contains($field)) {
            $errors += "AP $i : missing field '$field'"
        }
    }
    if ($ap.status -notin $Statuses) {
        $errors += "AP $i : invalid status '$($ap.status)'"
    }
    if ($ap.band -notin $Bands) {
        $errors += "AP $i : invalid band '$($ap.band)'"
    }
    if ($ap.PSObject.Properties.Name.Contains("signal_quality") -and $ap.signal_quality -notin $Qualities) {
        $errors += "AP $i : invalid signal_quality '$($ap.signal_quality)'"
    }
    if ($ids.ContainsKey($ap.ap_id)) {
        $errors += "AP $i : duplicate ap_id '$($ap.ap_id)'"
    }
    $ids[$ap.ap_id] = $true
    if ($bssids.ContainsKey($ap.bssid)) {
        $errors += "AP $i : duplicate bssid '$($ap.bssid)'"
    }
    $bssids[$ap.bssid] = $true
}

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Error $e }
    exit 1
}

Write-Output "OK: $($aps.Count) access points validated successfully."
