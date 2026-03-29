---
name: wifi-survey-report
description: "Generate a Markdown site-survey status report from data/ap_inventory.json. Use when producing deployment summaries, coverage audit reports, or signal quality assessments."
argument-hint: "Optional: report scope like 'critical signal only' or 'offline APs'"
---

# WiFi Survey Report Skill

## When to Use

- Generate a site-survey deployment status report.
- Produce a coverage audit summary for stakeholders.
- Create a signal quality assessment for the RF engineering team.

## Procedure

1. Read `data/ap_inventory.json` to load all access points.
2. Cross-reference with `docs/wifi-survey-spec.md` for field definitions and quality thresholds.
3. Compute the following metrics:
   - Total APs by status (`planned`, `deployed`, `offline`, `decommissioned`)
   - APs by band (`2.4 GHz`, `5 GHz`, `6 GHz`)
   - Signal quality distribution (`good`, `marginal`, `critical`)
   - Weak-signal APs (tx_power < 12 dBm)
4. Format the report using the [report template](./assets/report-template.md).
5. Apply the output format from [report format reference](./references/report-format.md).

## Output

A single Markdown document ready to share with stakeholders.
