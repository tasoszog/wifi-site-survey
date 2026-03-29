# Report Format Reference

## Structure

Every site-survey report must follow this structure:

1. **Header** — Report title with date
2. **Summary** — One-paragraph executive summary of deployment status
3. **Metrics Table** — AP counts by status and band
4. **Signal Quality** — Table of APs with marginal or critical signal
5. **Offline APs** — Table of non-responding access points
6. **Planned Deployments** — APs not yet installed
7. **Recommendations** — Actionable next steps for RF engineering

## Formatting Rules

- Use `##` for section headings.
- All counts in Markdown tables with alignment.
- Critical-signal APs highlighted with a warning emoji (⚠️).
- Offline APs highlighted with a red circle emoji (🔴).
- AP IDs in code formatting (`AP-01`).
- Location descriptions in plain text.
