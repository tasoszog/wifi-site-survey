---
description: "Use when creating or editing JSON data files in data/. Covers AP inventory schema validation, required fields, and enum constraints."
applyTo: "data/**/*.json"
---
# Data File Guidelines

- Every AP object must include: `ap_id`, `ssid`, `bssid`, `channel`, `band`, `tx_power`, `location`, `status`, `firmware_version`.
- `status` must be one of: `planned`, `deployed`, `offline`, `decommissioned`.
- `band` must be one of: `2.4 GHz`, `5 GHz`, `6 GHz`.
- `signal_quality`, if present, must be one of: `good`, `marginal`, `critical`.
- `ap_id` and `bssid` values must be unique across all entries.
- Keep the file as a flat JSON array (no nesting, no wrapper object).
- Run `scripts/validate.sh` (or `scripts/validate.ps1` on Windows) after changes.
