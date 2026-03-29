# WiFi Site-Survey — Data Specification

Purpose: Define the schema and validation rules for the WiFi site-survey
AP inventory used in this Copilot features demo.

## AP Fields

| Field              | Type     | Required | Description                                  |
|--------------------|----------|----------|----------------------------------------------|
| `ap_id`            | string   | Yes      | Unique identifier (e.g., `AP-01`)            |
| `ssid`             | string   | Yes      | Network name broadcast by the AP             |
| `bssid`            | string   | Yes      | MAC address (e.g., `AA:BB:CC:DD:EE:01`)      |
| `channel`          | integer  | Yes      | Operating channel number                      |
| `band`             | enum     | Yes      | One of: `2.4 GHz`, `5 GHz`, `6 GHz`          |
| `tx_power`         | integer  | Yes      | Transmit power in dBm                         |
| `location`         | string   | Yes      | Human-readable deployment location            |
| `status`           | enum     | Yes      | One of: `planned`, `deployed`, `offline`, `decommissioned` |
| `signal_quality`   | enum     | No       | One of: `good`, `marginal`, `critical`        |
| `firmware_version` | string   | Yes      | Firmware version string (e.g., `8.10.0.1`)    |

## Status Lifecycle

```
planned  ──►  deployed  ──►  offline  ──►  decommissioned
```

- **planned** — approved but not yet installed
- **deployed** — active and serving clients
- **offline** — not responding (needs investigation)
- **decommissioned** — permanently removed from service

## Signal Quality

| Quality    | tx_power Range | Action Required          |
|------------|----------------|--------------------------|
| good       | ≥ 15 dBm       | None                     |
| marginal   | 10–14 dBm      | Schedule power adjustment |
| critical   | < 10 dBm       | Immediate investigation  |

## Data File

All access points are stored in `data/ap_inventory.json` as a JSON array.
Each element is an AP object matching the fields above.

## Validation Rules

1. Every AP must have `ap_id`, `ssid`, `bssid`, `channel`, `band`, `tx_power`,
   `location`, `status`, and `firmware_version`.
2. `status` must be one of the four valid values.
3. `band` must be one of the three valid values.
4. `signal_quality`, if present, must be one of the three valid values.
5. `ap_id` and `bssid` values must be unique across all entries.
6. `channel` must be a positive integer.
7. `tx_power` must be a positive integer (dBm).
