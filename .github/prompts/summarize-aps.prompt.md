---
description: "Summarize AP data from data/ap_inventory.json — counts by status, offline APs, signal quality, and deployment blockers."
argument-hint: "Optional: path to ap_inventory.json or filter criteria (e.g., 'only critical signal quality')"
---
Read the AP inventory from `data/ap_inventory.json` and produce a summary report:

1. **Counts** — Total APs, broken down by status (`planned`, `deployed`, `offline`, `decommissioned`) and band (`2.4 GHz`, `5 GHz`, `6 GHz`).
2. **Offline APs** — List any APs with `"status": "offline"`. Show ap_id, location, and firmware_version.
3. **Signal Quality** — List APs with `"signal_quality": "critical"` or `"marginal"`, grouped by quality level.
4. **Blockers** — Flag any planned APs that haven't been deployed yet.

Format the output as a clear Markdown table or bullet list.
