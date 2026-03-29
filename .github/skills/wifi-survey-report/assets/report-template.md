# WiFi Site-Survey Report — {{DATE}}

## Summary

{{EXECUTIVE_SUMMARY}}

## AP Inventory Metrics

| Status           | Count |
|------------------|------:|
| Deployed         | {{DEPLOYED_COUNT}} |
| Planned          | {{PLANNED_COUNT}} |
| Offline          | {{OFFLINE_COUNT}} |
| Decommissioned   | {{DECOMMISSIONED_COUNT}} |
| **Total**        | **{{TOTAL}}** |

| Band    | Count |
|---------|------:|
| 2.4 GHz | {{BAND_24_COUNT}} |
| 5 GHz   | {{BAND_5_COUNT}} |
| 6 GHz   | {{BAND_6_COUNT}} |

## ⚠️ Signal Quality Issues

| AP ID | Location | Band | tx_power | Signal Quality |
|-------|----------|------|----------|----------------|
{{SIGNAL_QUALITY_ROWS}}

## 🔴 Offline APs

| AP ID | Location | Firmware | Last Known Band |
|-------|----------|----------|-----------------|
{{OFFLINE_ROWS}}

## Planned Deployments

{{PLANNED_DEPLOYMENTS}}

## Recommendations

{{RECOMMENDATIONS}}
