---
description: "Rewrite all exercises in README.md so they follow a continuous WiFi system engineer scenario — each exercise flows into the next, and all examples use WiFi domain context."
argument-hint: "Optional: chapter range to rewrite, e.g. 'Chapter 0–3 only' or 'Part B only'"
agent: "agent"
---

# Adapt Tutorial Exercises for a WiFi System Engineer

Rewrite every exercise in [README.md](../../README.md) so that:

## 1. Continuous narrative

All exercises across **every chapter** tell one connected story. Each exercise
builds on the outcome of the previous one — files created, edits made, or
concepts introduced carry forward. The learner should feel they are working
through a single, realistic WiFi engineering project from start to finish,
not jumping between unrelated tasks.

**Narrative arc** (use this as the backbone):

1. **Chapter 0 (Git)** — The engineer initialises a new repository for a WiFi
   site-survey project. Commits, branches, and stash exercises track changes
   to access-point inventory files and survey configs.
2. **Chapter 1 (Slash commands)** — The engineer uses Copilot to explain,
   test, plan, and scaffold code for a WiFi network analysis toolkit
   (e.g., signal-strength parser, channel-overlap detector, client-load
   balancer).
3. **Chapter 2 (`@` participants)** — The engineer asks `@vscode` about
   extensions useful for network engineers, `@terminal` for Wi-Fi diagnostic
   CLI commands (netsh wlan, iwconfig, etc.), and `@github` for open PRs on
   the survey repo.
4. **Chapter 3 (`#` context)** — The engineer attaches survey data files,
   references the codebase for validation rules, and uses `#changes` to
   commit AP placement updates.
5. **Chapters 4–6 (Instructions & Prompts)** — The engineer creates workspace
   instructions for the WiFi project conventions, file-specific instructions
   for JSON survey-data schemas and Python RF-analysis style, and prompt
   files for generating RF coverage reports.
6. **Chapter 7 (Hooks)** — A hook validates that edited AP-inventory JSON
   always has required fields (BSSID, SSID, channel, tx_power).
7. **Chapter 8 (Agents)** — A read-only "RF Analyst" agent analyses survey
   data; a "Report Writer" subagent generates site-survey documentation.
8. **Chapter 9 (Skills)** — A skill produces a formatted WiFi site-survey
   status report from the AP inventory data.
9. **Chapter 10 (MCP)** — The engineer fetches vendor firmware release notes
   via the MCP `fetch` server.

## 2. WiFi system engineer domain

Replace **all** generic task-tracker examples with WiFi engineering equivalents.
Use realistic terminology and scenarios a WiFi system engineer would encounter
daily. Reference table for replacements:

| Current (task tracker)             | Replace with (WiFi engineering)                              |
|------------------------------------|--------------------------------------------------------------|
| `tasks.json`                       | `data/ap_inventory.json` (access-point inventory)            |
| Task fields (id, title, status…)   | AP fields (ap_id, ssid, bssid, channel, band, tx_power, location, status, firmware_version) |
| `task_utils.py`                    | `src/wifi_utils.py` (WiFi analysis utilities)                |
| `count_overdue`                    | `find_weak_signals` or `detect_channel_conflicts`            |
| `filter_by_status`                 | `filter_aps_by_band` (2.4 GHz / 5 GHz / 6 GHz)             |
| `get_tasks_by_tag`                 | `get_aps_by_location` (floor, building, zone)                |
| `task-tracker-spec.md`             | `docs/wifi-survey-spec.md` (survey data specification)       |
| `validate.sh` / `validate.ps1`    | Scripts that validate AP inventory schema                    |
| Assignee names (alice, bob…)       | WiFi engineer names or site names (Site-A, Building-North)   |
| Priority (low/medium/high)         | Severity or signal quality (good/marginal/critical)          |
| Status (todo/in-progress/done)     | AP status (planned/deployed/offline/decommissioned)          |
| Tags (infra, docs, bug…)          | Tags (indoor, outdoor, mesh, DFS, high-density)              |
| "Set up CI pipeline"              | "Deploy AP-42 on Floor 3 East Wing"                          |
| "Write unit tests"                | "Run RF coverage validation for Building North"              |
| Task-report skill                 | WiFi site-survey report skill                                |
| Conventional commit examples      | e.g., `feat(survey): add channel-overlap detection`          |

## 3. Rules

- **Do NOT change which Copilot feature is being taught.** Every exercise must
  still demonstrate the same `/` command, `@` participant, `#` reference, or
  customization primitive as the original.
- **Keep the same exercise numbering and structure** (Step 1, Step 2, etc.).
- **Keep "What you see" blocks** — update their content to match the WiFi
  domain.
- **Keep safety notes, tips, and cleanup steps** — adapt file paths to the new
  domain files.
- **Maintain the same heading hierarchy** and Markdown formatting conventions
  already used in the README.
- **Cross-reference between exercises**: when an exercise uses a file or
  function created in an earlier exercise, mention it explicitly
  (e.g., "Using the `wifi_utils.py` file you created in Chapter 1
  Exercise 6…").
- Keep the table-of-contents structure intact; update section names only if
  the domain term changed.
- When the original exercise says "add a comment" or "make a small edit",
  make it a WiFi-relevant edit (e.g., "add a `# Channel planning constants`
  comment" or "update the tx_power default").
