#!/usr/bin/env bash
# validate.sh — Validates data/ap_inventory.json structure.
# Exit 0 = valid, Exit 1 = invalid.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_FILE="${SCRIPT_DIR}/../data/ap_inventory.json"

if [ ! -f "$DATA_FILE" ]; then
    echo "ERROR: ap_inventory.json not found at $DATA_FILE" >&2
    exit 1
fi

# Check valid JSON
if ! python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$DATA_FILE" 2>/dev/null; then
    echo "ERROR: ap_inventory.json is not valid JSON" >&2
    exit 1
fi

# Validate each AP has required fields and valid enum values
python3 -c "
import json, sys

REQUIRED = {'ap_id', 'ssid', 'bssid', 'channel', 'band', 'tx_power', 'location', 'status', 'firmware_version'}
STATUSES = {'planned', 'deployed', 'offline', 'decommissioned'}
BANDS = {'2.4 GHz', '5 GHz', '6 GHz'}
QUALITIES = {'good', 'marginal', 'critical'}

with open(sys.argv[1]) as f:
    aps = json.load(f)

if not isinstance(aps, list):
    print('ERROR: root must be an array', file=sys.stderr)
    sys.exit(1)

ap_ids = set()
bssids = set()
errors = []
for i, ap in enumerate(aps):
    missing = REQUIRED - set(ap.keys())
    if missing:
        errors.append(f'AP {i}: missing fields: {missing}')
    if ap.get('status') not in STATUSES:
        errors.append(f'AP {i}: invalid status \"{ap.get(\"status\")}\"')
    if ap.get('band') not in BANDS:
        errors.append(f'AP {i}: invalid band \"{ap.get(\"band\")}\"')
    sq = ap.get('signal_quality')
    if sq is not None and sq not in QUALITIES:
        errors.append(f'AP {i}: invalid signal_quality \"{sq}\"')
    aid = ap.get('ap_id')
    if aid in ap_ids:
        errors.append(f'AP {i}: duplicate ap_id \"{aid}\"')
    ap_ids.add(aid)
    bssid = ap.get('bssid')
    if bssid in bssids:
        errors.append(f'AP {i}: duplicate bssid \"{bssid}\"')
    bssids.add(bssid)

if errors:
    for e in errors:
        print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)

print(f'OK: {len(aps)} access points validated successfully.')
" "$DATA_FILE"
