---
description: "Adapt this Copilot features demo workspace to fit any group's discipline or domain. Interactively interviews the user, then transforms all files."
agent: "agent"
---

# Adapt Workspace to a New Discipline

You are a workspace adaptation assistant. Your job is to transform this
WiFi Site-Survey Toolkit demo into a fully working Copilot features demo
for the user's own discipline. Follow the four phases below **in order**.

---

## Phase A — Domain Interview

Before making any changes, interview the user to gather their domain
details. Ask all of the following questions **in a single message** and
wait for the user to reply before proceeding:

1. **Domain name & description** — What is your discipline?
   Give a short name and one-sentence description.
   *(Example: "Restaurant Health Inspections — tracking inspection
   results across restaurant locations.")*

2. **Primary data entity** — What is the main "thing" your inventory
   tracks? This replaces "Access Point" throughout the workspace.
   *(Example: "Restaurant", "Satellite", "Lab Instrument")*

3. **Entity fields** — List 6–10 fields for your entity, each with:
   - Field name (snake_case)
   - Type (`string`, `integer`, `enum`, `boolean`, `date`)
   - Required or optional
   - For enums: list the allowed values
   *(Example: `restaurant_id` string required, `cuisine` enum
   [Italian, Mexican, Japanese, American, Other], …)*

4. **Status lifecycle** — Define 3–5 ordered statuses for your entity.
   This replaces `planned → deployed → offline → decommissioned`.
   *(Example: `scheduled → in_progress → passed → failed → closed`)*

5. **Quality / severity metric** — Define a quality or severity scale
   with 3 levels (good / warning / critical equivalent). For each level,
   specify the name and the rule that determines it.
   *(Example: "Hygiene Score — excellent (≥ 90), acceptable (70–89),
   violation (< 70)")*

6. **Two specialist roles** — Name two agent personas for your domain.
   One is a read-only analyst; the other is a documentation writer.
   These replace "RF Analyst" and "Report Writer".
   *(Example: "Inspection Analyst" and "Compliance Report Writer")*

7. **Report use case** — What kind of summary report should the skill
   generate? This replaces "WiFi site-survey status report".
   *(Example: "Monthly restaurant inspection compliance report")*

8. **Programming language** — Which language for utility code?
   Default is Python. If you choose another language, state it here.

9. **Extra conventions** — Any additional coding conventions, naming
   rules, or constraints you want enforced? (Optional — press Enter
   to skip.)

---

## Phase B — Mapping Confirmation

After receiving the user's answers, produce a **concept mapping table**
and present it for confirmation. Do NOT edit any files yet.

Format:

```
| WiFi Concept               | Your Domain Equivalent          |
|----------------------------|---------------------------------|
| Access Point (AP)          | {entity_name}                   |
| ap_inventory.json          | {entity_snake}_inventory.json   |
| wifi_utils.py              | {domain_snake}_utils.py         |
| RF Analyst                 | {analyst_role}                  |
| Report Writer              | {writer_role}                   |
| wifi-survey-report (skill) | {domain_slug}-report            |
| summarize-aps (prompt)     | summarize-{entities_slug}       |
| site-survey status report  | {report_description}            |
| planned/deployed/offline/… | {status_1}/{status_2}/{…}       |
| good/marginal/critical     | {quality_1}/{quality_2}/{…}     |
| tx_power (dBm)             | {quality_metric_field} ({unit}) |
```

Ask the user: **"Does this mapping look correct? Reply 'yes' to proceed
or describe any corrections."**

Wait for confirmation before continuing.

---

## Phase C — File-by-File Transformation

Apply changes in the six groups below, **in order**. Each group depends
on the groups before it. After finishing each group, print a brief
status line (e.g., "✓ Group 1 complete — spec and data files updated.").

### Group 1 — Spec & Data (foundations)

| File | Action |
|------|--------|
| `docs/wifi-survey-spec.md` | Rewrite completely: new entity name, field table matching the user's schema, status lifecycle diagram, quality metric table, validation rules. Keep the same Markdown structure and heading hierarchy. |
| `data/ap_inventory.json` | Replace with a flat JSON array of **8 realistic sample records** that conform to the new schema. Include a mix of all statuses and quality levels. Use plausible field values for the user's domain. |

### Group 2 — Copilot Configuration (depends on Group 1)

| File | Action |
|------|--------|
| `.github/copilot-instructions.md` | Update project title, description, structure table, conventions, and Quick Start section to reference the new domain, file names, and validation commands. |
| `.github/instructions/data-files.instructions.md` | Rewrite required fields list, enum constraints, uniqueness rules, and `applyTo` glob (if the data file was renamed). |
| `.github/instructions/python-style.instructions.md` | Keep as-is if the user chose Python. If they chose another language, rewrite for that language's conventions and update the `applyTo` glob. |
| `.github/instructions/documentation.instructions.md` | Keep as-is — it is domain-agnostic. |

### Group 3 — Code & Scripts (depends on Groups 1–2)

| File | Action |
|------|--------|
| `src/wifi_utils.py` | Rewrite all functions for the new entity: `load_{entities}`, `find_{quality_issue}`, `filter_{entities}_by_{field}`, `count_by_{status_field}`, `count_by_{category_field}`, `summary`. Update the `__main__` block to print a formatted table of the new entity. Maintain the same code style (type hints, docstrings, pathlib, f-strings). |
| `scripts/validate.sh` | Update the inline Python validation logic: new required fields, new enum values, new uniqueness constraints, new data file path. |
| `scripts/validate.ps1` | Same updates as `validate.sh`, in PowerShell syntax. |
| `scripts/hooks/enforce-todo-format.sh` | Update the file-match check to reference the new data file name. Update the validation call. |
| `scripts/hooks/enforce-todo-format.ps1` | Same updates in PowerShell syntax. |

### Group 4 — Prompts, Agents & Skills (depends on Groups 1–3)

| File | Action |
|------|--------|
| `.github/prompts/summarize-aps.prompt.md` | Rewrite: new description, new data file path, new summary fields (counts by status, quality issues, blockers) matching the user's schema. |
| `.github/prompts/generate-test-cases.prompt.md` | Keep as-is — it is domain-agnostic. |
| `.github/agents/rf-analyst.agent.md` | Rewrite: new `name`, `description`, persona, data file references, and analysis focus areas for the user's analyst role. Keep `tools: [read, search]` (read-only). |
| `.github/agents/report-writer.agent.md` | Rewrite: new `name`, `description`, persona, and output focus for the user's writer role. Keep `tools: [read, search, edit]` and the `.md`-only edit constraint. |
| `.github/skills/wifi-survey-report/SKILL.md` | Rewrite: new `name`, `description`, procedure steps, and metrics list for the user's report use case. Update file path references. |
| `.github/skills/wifi-survey-report/assets/report-template.md` | Rewrite template: new heading, new sections, new template variables matching the user's entity fields, statuses, and quality levels. |
| `.github/skills/wifi-survey-report/references/report-format.md` | Rewrite format rules: new section names, table columns, emoji conventions for the user's statuses and quality levels. |

### Group 5 — HTML & Tutorial (depends on all above)

| File | Action |
|------|--------|
| `index.html` | Replace all WiFi / AP / site-survey references with the new domain terminology. Update: hero section title and description, chapter descriptions, decision flow labels, file map entries, exercise text, appendix references. Preserve all HTML structure, CSS, and JavaScript functionality. |
| `prolog.html` | Replace WiFi domain references in all 7 video scene narration blocks. Update the domain example, toolkit name, and any AP-specific wording. Preserve HTML structure. |
| `README.md` | Replace the project title, domain description, and all exercise instructions that reference WiFi, APs, or site-surveys. Update file paths mentioned in exercise steps. Preserve Markdown structure and chapter numbering. |

### Group 6 — File & Folder Renames (final pass)

Rename domain-specific files and folders. For each rename:
- Create the new file (or folder + files) with the adapted content.
- Delete the old file (or folder).
- After all renames, do a **cross-reference sweep**: search every file in
  the workspace for any remaining reference to the old file/folder names
  and update them to point to the new names.

| Old Path | New Path (use user's domain terms) |
|----------|------------------------------------|
| `src/wifi_utils.py` | `src/{domain_snake}_utils.py` |
| `data/ap_inventory.json` | `data/{entity_snake}_inventory.json` |
| `.github/prompts/summarize-aps.prompt.md` | `.github/prompts/summarize-{entities_slug}.prompt.md` |
| `.github/agents/rf-analyst.agent.md` | `.github/agents/{analyst_slug}.agent.md` |
| `.github/agents/report-writer.agent.md` | `.github/agents/{writer_slug}.agent.md` |
| `.github/skills/wifi-survey-report/` | `.github/skills/{domain_slug}-report/` (create new folder, move adapted `SKILL.md`, `assets/report-template.md`, `references/report-format.md` into it, then delete the old folder) |

After all renames, update every reference to old paths in:
- `.github/copilot-instructions.md`
- `.github/instructions/data-files.instructions.md`
- `.github/skills/{new}/SKILL.md`
- `scripts/validate.sh`, `scripts/validate.ps1`
- `scripts/hooks/enforce-todo-format.sh`, `scripts/hooks/enforce-todo-format.ps1`
- `index.html` (file map section)
- `README.md` (exercise steps, Quick Start)

---

## Phase D — Verification

After all transformations and renames are complete:

1. **Validate data** — Run the appropriate validation script
   (`scripts/validate.ps1` on Windows, `scripts/validate.sh` on
   macOS/Linux) against the new data file. Fix any errors.

2. **Check YAML frontmatter** — Read every `.md` file under `.github/`
   and verify the YAML frontmatter between `---` fences is valid
   (no syntax errors, required fields present).

3. **Stale reference scan** — Search the entire workspace for leftover
   WiFi-era terms. Grep (case-insensitive) for:
   `wifi`, `site.survey`, `access.point`, `AP-0`, `ap_inventory`,
   `wifi_utils`, `rf.analyst`, `summarize.aps`, `wifi-survey-report`.
   Any hits outside this prompt file itself must be fixed.

4. **Print summary** — Display a final summary table:

   ```
   | Action          | Count | Details                      |
   |-----------------|-------|------------------------------|
   | Files rewritten |   N   | list of paths                |
   | Files renamed   |   N   | old → new                    |
   | Files unchanged |   N   | list (generic/domain-agnostic)|
   | Stale refs found|   0   | (should be zero)             |
   | Validation      | PASS  |                              |
   ```

   If any stale references remain, list them and fix them before
   declaring the adaptation complete.
