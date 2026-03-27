# GitHub Copilot Features — Hands-On Tutorial

A self-contained example project that demonstrates **every** GitHub Copilot
customization primitive with working files you can test immediately.

> **Audience**: Team members learning Copilot's customization system.
> **Time**: ~60–90 minutes to complete all chapters.
> **Prerequisites**: VS Code 1.100+, GitHub Copilot extension, an active Copilot subscription.

---

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- **Part A — Built-in Chat Interface**
  - [Chapter 1: `/` Slash Commands](#chapter-1--slash-commands)
  - [Chapter 2: `@` Chat Participants](#chapter-2--chat-participants)
  - [Chapter 3: `#` Context Mentions & Tools](#chapter-3--context-mentions--tools)
- **Part B — Customization Primitives**
  - [Chapter 4: Workspace Instructions](#chapter-4-workspace-instructions)
  - [Chapter 5: File-Specific Instructions](#chapter-5-file-specific-instructions)
  - [Chapter 6: Prompt Files](#chapter-6-prompt-files)
  - [Chapter 7: Hooks](#chapter-7-hooks)
  - [Chapter 8: Custom Agents](#chapter-8-custom-agents)
  - [Chapter 9: Skills](#chapter-9-skills)
  - [Chapter 10: MCP Integration](#chapter-10-mcp-integration)
- **Appendices**
  - [A: Decision Flow](#appendix-a-decision-flow)
  - [B: Common Pitfalls](#appendix-b-common-pitfalls--debugging)
  - [C: File Reference](#appendix-c-file-reference)
  - [D: Slash Command Reference](#appendix-d-complete-slash-command-reference)
  - [E: `@` and `#` Cheat Sheet](#appendix-e--and--cheat-sheet)

---

## Introduction

GitHub Copilot in VS Code is more than autocomplete. It provides a full
customization system that lets you shape how the AI understands your project,
what tools it can use, and how it responds. There are three layers:

| Layer | What | How |
|-------|------|-----|
| **Chat Interface** | Built-in `/` commands, `@` participants, `#` context | Already available — just type in chat |
| **Customization Primitives** | Instructions, prompts, hooks, agents, skills | Create files in `.github/` — version-controlled, team-shared |
| **External Tools** | MCP servers, extension tools | Configure in `.vscode/mcp.json` or install extensions |

This tutorial walks through all three layers with working examples you can test
in this project.

### Project Domain

This project uses a minimal **task tracker** as its domain:
- `data/tasks.json` — 8 sample tasks with statuses, priorities, and due dates
- `src/task_utils.py` — Python utilities for loading and querying tasks
- `docs/task-tracker-spec.md` — the data specification
- `scripts/validate.sh` / `validate.ps1` — data validation scripts

The domain is intentionally simple — the focus is on the Copilot features, not
the application code.

---

## Getting Started

### 1. Open this project in VS Code

```
code copilot-features-demo
```

Or use **File → Open Folder** and select this directory.

### 2. Verify Copilot is active

- Look for the Copilot icon (sparkle) in the status bar.
- Open Chat: **Ctrl+Alt+I** (Windows/Linux) or **Cmd+Alt+I** (macOS).
- Type "Hello" — you should get a response.

### 3. Enable agent mode

In your VS Code settings, ensure:
```json
{
  "chat.agent.enabled": true
}
```

### 4. Initialize the project as a git repository (recommended)

Initializing git allows you to track changes, revert experiments, and share
your customization files with your team via version control.

**On Windows (PowerShell):**

```powershell
cd C:\Projects\copilot-features-demo
git init
git add .
git commit -m "Initial commit: Copilot features demo"
```

**On macOS / Linux (Terminal):**

```bash
cd ~/path/to/copilot-features-demo
git init
git add .
git commit -m "Initial commit: Copilot features demo"
```

**What each command does:**

| Command | Purpose |
|---------|---------|
| `git init` | Creates a new `.git/` folder — turns the directory into a git repository |
| `git add .` | Stages all files in the project for the first commit |
| `git commit -m "..."` | Saves a snapshot of the project with a descriptive message |

> **Tip**: If git is not installed, download it from [https://git-scm.com](https://git-scm.com)
> and re-open your terminal after installation.

Workspace instructions are designed to be version-controlled and shared with
your team.

---

# Part A — Built-in Chat Interface

These features are available out of the box. No files to create — just open
Chat and start typing.

---

## Chapter 1 · `/` Slash Commands

**Concept**: Slash commands are shortcuts to specific functionality. Type `/` in
the chat input to see all available commands. They fall into 8 categories:

### Category 1: Coding Actions

These operate on code you select or reference in your prompt.

| Command | What it does |
|---------|-------------|
| `/explain` | Explains selected code — purpose, logic, edge cases |
| `/fix` | Proposes fixes for errors (reads Problems panel / stack traces) |
| `/tests` | Generates tests for selected code using your project's test framework |
| `/doc` | Generates documentation comments (inline chat) |
| `/setupTests` | Scaffolds a test framework (config, dependencies, example tests) |
| `/fixTestFailure` | Analyzes failing tests and suggests fixes |

### Category 2: Scaffolding

| Command | What it does |
|---------|-------------|
| `/new` | Creates a new file or project from a description |
| `/newNotebook` | Creates a new Jupyter notebook from a description |

### Category 3: Session Management

| Command | What it does |
|---------|-------------|
| `/clear` | Starts a fresh chat session (archives current one) |
| `/fork` | Copies the conversation into a new independent session |
| `/compact` | Summarizes conversation history to free context window space |
| `/rename` | Renames the current chat session (for organization) |

### Category 4: Planning & Search

| Command | What it does |
|---------|-------------|
| `/plan` | Creates a step-by-step implementation plan before writing code |
| `/search` | Semantic search across your workspace |
| `/startDebugging` | Generates a `launch.json` and starts a debug session |

### Category 5: Customization Creators

These create the files you'll learn about in Part B:

| Command | What it creates |
|---------|----------------|
| `/init` | Generates `copilot-instructions.md` from your project structure |
| `/create-prompt` | Creates a `.prompt.md` file |
| `/create-instruction` | Creates a `.instructions.md` file |
| `/create-skill` | Creates a `SKILL.md` and skill folder |
| `/create-agent` | Creates an `.agent.md` file |
| `/create-hook` | Creates a hook `.json` config |
| `/agent-customization` | Opens the agent customization workflow |

### Category 6: Management UIs

These open configuration panels for managing customization files:

| Command | Opens |
|---------|-------|
| `/agents` | Custom agents configuration |
| `/hooks` | Hook configuration |
| `/instructions` | Instruction files |
| `/prompts` | Prompt files |
| `/skills` | Agent skills |
| `/tools` | Tool availability and permissions |
| `/models` | AI model picker |
| `/plugins` | Chat plugins/extensions |

### Category 7: Permission Control

| Command | What it does |
|---------|-------------|
| `/autoApprove` | Auto-approve all tool calls (skip confirmation dialogs) |
| `/disableAutoApprove` | Re-enable confirmation dialogs |
| `/yolo` | Maximum autonomy — auto-approve + auto-respond to questions |
| `/disableYolo` | Return to normal approval mode |

> **Warning**: `/yolo` mode gives Copilot full autonomy with no confirmation
> prompts. Use it only in safe environments where you understand the
> consequences.

### Category 8: Debugging

| Command | What it does |
|---------|-------------|
| `/debug` | Opens the Chat Debug view — inspect system prompts, tools, and context that Copilot received |
| `/troubleshoot` | Analyzes agent debug logs for the current session |

### Key Insight

**Custom prompts and skills also appear as `/` commands.** Once you create a
prompt file (`.prompt.md`) or a skill (`SKILL.md`), you can invoke them by
typing `/` followed by the file name. For example, this project includes
`/generate-test-cases` and `/summarize-tasks` (prompts) and `/task-report`
(skill).

### 🧪 Try It — Exercises

1. Open `src/task_utils.py` in the editor.
2. Select the `count_overdue` function.
3. In Chat, type: `/explain`
   - **Expected**: Copilot explains the function's logic, parameters, and edge cases.
4. With the same selection, type: `/tests`
   - **Expected**: Copilot generates pytest-style test cases for `count_overdue`.
5. Type: `/plan Add a function to find tasks assigned to a specific person`
   - **Expected**: A structured plan with steps, not immediate code.
6. Type: `/debug`
   - **Expected**: The Chat Debug view opens, showing the system prompt and loaded context.
7. After several messages, type: `/compact`
   - **Expected**: The conversation is summarized, freeing context window space.

---

## Chapter 2 · `@` Chat Participants

**Concept**: Chat participants are domain-specific assistants you invoke with
`@`. They are built-in or contributed by extensions. Type `@` in the chat
input to see available participants.

### Built-in Participants

| Participant | Domain | Example |
|-------------|--------|---------|
| `@vscode` | VS Code features, settings, keybindings, extension APIs | `@vscode how do I enable word wrapping?` |
| `@terminal` | Shell commands, terminal operations, command-line help | `@terminal list the 5 largest files in this workspace` |
| `@github` | GitHub repos, PRs, issues, commits (requires [GitHub Pull Requests](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) extension) | `@github what are my open PRs?` |

### How Participants Differ from Custom Agents

| | `@` Chat Participants | Custom Agents (`.agent.md`) |
|-|----------------------|----------------------------|
| **Created by** | VS Code or extensions | You (project files) |
| **Invoked with** | `@name` in chat | Agent picker dropdown |
| **Tools** | Fixed by the extension | You define which tools are available |
| **Customizable** | No | Yes — full control over instructions, tools, model |
| **Shared via** | Extension installation | Version control (`.github/agents/`) |

### Extension-Contributed Participants

Extensions can add their own `@` participants. To discover them:
1. Type `@` in the chat input — all available participants are listed.
2. Or run the command: **Chat: List Participants** from the Command Palette.

Examples: Docker extensions may add `@docker`, database extensions may add
`@database`, etc.

### 🧪 Try It — Exercises

1. In Chat, type: `@vscode how do I change the font size?`
   - **Expected**: Instructions specific to VS Code settings, not general advice.
2. Type: `@terminal what command shows disk usage on Windows?`
   - **Expected**: PowerShell or cmd commands, not bash.
3. Type: `@vscode what's the keyboard shortcut for multi-cursor?`
   - **Expected**: Platform-specific keybinding (Ctrl+Alt+↓ on Windows).

---

## Chapter 3 · `#` Context Mentions & Tools

**Concept**: The `#` symbol lets you explicitly control what context and tools
are available to Copilot. Type `#` in the chat input to see all options.

### Context References

These add specific items from your workspace as context:

| Reference | What it adds |
|-----------|-------------|
| `#file:path/to/file` | A specific file's contents |
| `#folder:path/to/dir` | Files within a directory |
| `#symbol:functionName` | A specific code symbol (function, class, variable) |
| `#codebase` | Searches your entire codebase for relevant context |
| `#selection` | The current editor text selection |
| `#changes` | Uncommitted source control changes |

### Tool References

These invoke specific tools during the conversation:

| Tool | What it does |
|------|-------------|
| `#fetch` | Retrieves content from a URL |
| `#terminalSelection` | Reads the current terminal selection |
| `#terminalLastCommand` | Gets the last terminal command and its output |
| `#problems` | Adds workspace errors/warnings from the Problems panel |

### Tool Sets

When defining tools in agent or prompt frontmatter (the `tools:` field), you
reference tool sets by their alias:

| Alias | Capability | Example tools included |
|-------|-----------|----------------------|
| `read` | Read workspace files | `readFile`, `getNotebookSummary`, `terminalLastCommand` |
| `edit` | Modify files | `createFile`, `editFiles`, `editNotebook` |
| `execute` | Run code | `runInTerminal`, `runNotebookCell`, `testFailure` |
| `search` | Find things | `codebase`, `fileSearch`, `textSearch`, `listDirectory` |
| `web` | Access the internet | `fetch` |
| `agent` | Delegate to subagents | `runSubagent` |
| `vscode` | VS Code operations | `runCommand`, `extensions`, `installExtension` |
| `browser` | Interact with browser (Experimental) | Navigate, read, click, screenshot |
| `todos` | Task tracking | Manage todo lists in chat |

### Drag & Drop

You can also add context without `#` mentions:
- **Drag files** from the Explorer or Search view onto the Chat.
- **Drag folders** onto Chat to include all files within.
- **Drag problems** from the Problems panel.
- **Attach images** — screenshots, mockups, or diagrams.

### 🧪 Try It — Exercises

1. In Chat, type: `Explain #file:src/task_utils.py`
   - **Expected**: Copilot explains the entire file with full context.
2. Type: `What tasks are overdue based on #file:data/tasks.json`
   - **Expected**: Analysis specifically using the tasks data.
3. Type: `What are the validation rules? #codebase`
   - **Expected**: Copilot searches the entire project and finds rules in the spec and validate scripts.
4. After running `python src/task_utils.py` in the terminal, type:
   `Explain the output #terminalLastCommand`
   - **Expected**: Copilot reads the terminal output and explains the summary.
5. Type: `Summarize #fetch https://code.visualstudio.com/updates`
   - **Expected**: Copilot fetches the page and summarizes the latest VS Code release notes.

---

# Part B — Customization Primitives

From here on, each chapter focuses on a **file you create** in your project.
This project already includes all the example files — each chapter explains
what they do, why they're structured that way, and how to test them.

---

## Chapter 4: Workspace Instructions

**File**: `.github/copilot-instructions.md`

**Concept**: This file provides always-on context that Copilot reads with every
request in this workspace. It's like a brief project orientation for the AI —
shared via version control with your whole team.

### What's in the file

```
.github/copilot-instructions.md
```

Open it and you'll see:
- A project summary and folder structure table
- Coding conventions (data format, Python style, Markdown docs, no secrets)
- A quick-start section with validation commands

### Design Principles

1. **Minimal by default** — Only include what's relevant to *every* task. This
   file is loaded into every chat interaction, so bloat costs context-window
   space.
2. **Link, don't embed** — Reference `docs/task-tracker-spec.md` instead of
   copying its contents.
3. **Concise and actionable** — Every line should guide Copilot's behavior.

### When to use

- General coding standards that apply everywhere
- Project structure and conventions shared with the team
- Quick-start info the AI needs for any task

### Alternative: `AGENTS.md`

Instead of `copilot-instructions.md`, you can use an `AGENTS.md` file at the
project root. The key difference:
- `AGENTS.md` supports hierarchical overrides in monorepos (nested files in
  subdirectories take precedence).
- `copilot-instructions.md` is the recommended cross-editor format.
- **Use only one** — not both.

### 🧪 Try It

1. Open Chat and ask: `What are the coding conventions for this project?`
   - **Expected**: Copilot references conventions from `copilot-instructions.md`
     without you explicitly attaching the file.
2. Ask: `How do I validate the task data?`
   - **Expected**: Copilot mentions the validate scripts from the Quick Start section.
3. Use `/debug` to inspect the system prompt — you should see the workspace
   instructions injected.

### 📝 Exercise

Edit `.github/copilot-instructions.md` to add a new convention: "All JSON files
must use 2-space indentation." Then ask Copilot to create a new JSON file —
verify it uses 2-space indentation.

---

## Chapter 5: File-Specific Instructions

**Files**: `.github/instructions/*.instructions.md`

**Concept**: While workspace instructions apply everywhere, *file instructions*
apply only to specific files or tasks. They use two discovery modes:

| Mode | How it triggers | Use case |
|------|----------------|----------|
| **Explicit** (`applyTo`) | Automatically loaded when files matching the glob pattern are in context | File-type rules: "all Python files follow this style" |
| **On-demand** (`description`) | Copilot loads it when the task description matches | Task-type rules: "when writing documentation, follow these guidelines" |

### The three example files

#### 1. `data-files.instructions.md` — Explicit (glob-triggered)

```yaml
---
description: "Use when creating or editing JSON data files in data/..."
applyTo: "data/**/*.json"
---
```

This loads automatically whenever you open, create, or edit any `.json` file
in the `data/` folder. Copilot sees the task schema rules, required fields,
and validation commands.

#### 2. `python-style.instructions.md` — Explicit (glob-triggered)

```yaml
---
description: "Use when creating or editing Python source files..."
applyTo: "src/**/*.py"
---
```

This loads automatically for any Python file in `src/`. Copilot applies
snake_case, type hints, docstring, and f-string conventions.

#### 3. `documentation.instructions.md` — On-demand (description-triggered)

```yaml
---
description: "Use when writing, reviewing, or restructuring project documentation..."
---
```

No `applyTo` — this loads only when Copilot determines the task is about
documentation (based on keywords in the `description` field). The description
acts as the discovery surface.

### The `description` field is critical

The `description` field is how Copilot decides whether to load an instruction
file. If trigger phrases aren't in the description, the agent won't find it.

**Pattern**: Start with `"Use when..."` followed by specific keywords:
```
"Use when creating or editing JSON data files in data/..."
```

### 🧪 Try It

1. Open `data/tasks.json` and ask Copilot to add a new task.
   - **Expected**: The new task includes all required fields with valid enum
     values, matching `data-files.instructions.md` rules.
2. Open `src/task_utils.py` and ask Copilot to add a new function.
   - **Expected**: snake_case name, type hints, docstring — matching
     `python-style.instructions.md`.
3. Ask Copilot: "Write a user guide for the task tracker."
   - **Expected**: Markdown formatting with ATX headings, tables, and links —
     matching `documentation.instructions.md` (loaded on-demand).
4. Use `/debug` to verify which instruction files were loaded.

### 📝 Exercise

Create a new file `.github/instructions/scripts.instructions.md` with:
- `applyTo: "scripts/**/*.sh"` 
- Rules: always include `set -euo pipefail`, add a header comment with purpose
  and exit codes.

Then ask Copilot to write a new shell script — verify it follows your rules.

---

## Chapter 6: Prompt Files

**Files**: `.github/prompts/*.prompt.md`

**Concept**: Prompt files are reusable task templates that appear as `/`
commands in chat. Each one defines a focused, repeatable task you can invoke
with a slash command.

### The two example files

#### 1. `generate-test-cases.prompt.md`

```yaml
---
description: "Generate test cases for the selected code or function..."
agent: "agent"
---
```

- **Invocation**: Type `/generate-test-cases` in chat.
- **`agent: "agent"`** tells Copilot to run this in full agent mode (can read
  files, search code, and make edits).
- The body defines what kind of tests to generate (pytest conventions, edge
  cases, descriptive names).

#### 2. `summarize-tasks.prompt.md`

```yaml
---
description: "Summarize tasks from data/tasks.json..."
argument-hint: "Optional: path to tasks.json or filter criteria"
---
```

- **Invocation**: Type `/summarize-tasks` in chat.
- **`argument-hint`** shows help text in the chat input field, guiding the
  user on what to type after the command.
- The body defines the report structure (counts, overdue, in-progress, blockers).

### Prompts vs Skills

Both appear after typing `/` in chat. The difference:

| | Prompts | Skills |
|-|---------|--------|
| **Complexity** | Single focused task | Multi-step workflow |
| **Assets** | Just one `.prompt.md` file | Folder with SKILL.md + scripts, templates, references |
| **Use case** | "Generate tests for this code" | "Run this entire QA workflow" |

### Frontmatter options

```yaml
---
description: "..."           # What it does (for discovery)
argument-hint: "..."         # Hint shown in chat input
agent: "agent"               # Which agent runs it: agent, ask, plan, or custom
model: "Claude Sonnet 4"     # Preferred AI model
tools: [search, web]         # Tools available during execution
---
```

### 🧪 Try It

1. Select the `filter_by_status` function in `src/task_utils.py`.
2. Type `/generate-test-cases` in chat.
   - **Expected**: Copilot generates pytest tests with happy path, edge cases,
     and error cases for the selected function.
3. Type `/summarize-tasks` in chat.
   - **Expected**: A formatted summary of all tasks with counts, overdue items,
     and blockers.
4. Type `/summarize-tasks only high priority`
   - **Expected**: Filtered summary showing only high-priority tasks (the
     argument hint guided you).

### 📝 Exercise

Create `.github/prompts/code-review.prompt.md` that:
- Reviews selected code for potential bugs and style issues
- Uses the `ask` agent (no file changes, just analysis)
- Includes an `argument-hint` like "Select code to review"

Test it on `src/task_utils.py`.

---

## Chapter 7: Hooks

**Files**: `.github/hooks/validate-json.json` + `scripts/hooks/enforce-todo-format.*`

**Concept**: Hooks are **deterministic** automation — they run shell commands at
specific lifecycle events in the agent session. Unlike instructions (which
*guide* behavior), hooks *enforce* it.

### How hooks work

```
Agent lifecycle event  →  Hook fires  →  Shell script runs  →  Returns JSON/exit code
```

The hook system provides context as JSON on stdin. Your script processes it and
communicates back:
- **Exit 0**: Continue normally
- **Exit 2**: Blocking error — stop the operation
- Other exit codes: Non-blocking warning

### Hook events

| Event | When it fires |
|-------|--------------|
| `SessionStart` | First prompt of a new agent session |
| `UserPromptSubmit` | User sends a prompt |
| `PreToolUse` | Before a tool is invoked |
| `PostToolUse` | After a tool completes successfully |
| `PreCompact` | Before context compaction |
| `SubagentStart` | A subagent starts |
| `SubagentStop` | A subagent ends |
| `Stop` | Agent session ends |

### The example: validate-json.json

This project uses a `PostToolUse` hook:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "bash ./scripts/hooks/enforce-todo-format.sh",
        "windows": "powershell -ExecutionPolicy Bypass -File ./scripts/hooks/enforce-todo-format.ps1",
        "timeout": 15
      }
    ]
  }
}
```

**What it does**: After every file edit, the hook script checks:
1. Was the edited file `tasks.json`?
2. If yes, run `scripts/validate.sh` to check the data structure.
3. If validation fails → exit 2 (blocking error) → Copilot sees the failure
   and can self-correct.
4. If the edit wasn't `tasks.json` → exit 0 (do nothing).

### The hook script flow

```
stdin (JSON payload)
  │
  ├─ toolName != "editFiles" or "createFile"?  →  exit 0 (skip)
  │
  ├─ no "tasks.json" in edited files?  →  exit 0 (skip)
  │
  └─ run validate.sh/validate.ps1
       ├─ passes  →  exit 0 (continue)
       └─ fails   →  exit 2 (block, agent sees error)
```

### Hooks vs Instructions

| | Instructions | Hooks |
|-|-------------|-------|
| **Behavior** | Guide (non-deterministic) | Enforce (deterministic) |
| **How** | AI interprets text guidance | Shell script runs automatically |
| **Guarantee** | Best-effort | 100% — the script always runs |
| **Use case** | "Prefer snake_case" | "Block if JSON is invalid" |

### 🧪 Try It

1. Ask Copilot: "Add a new task to tasks.json with missing required fields."
   - **Expected**: After the edit, the PostToolUse hook fires, validation fails
     (exit 2), and Copilot sees the error. It will attempt to fix the task
     to include all required fields.
2. Ask Copilot: "Add a valid task TASK-009 to tasks.json."
   - **Expected**: The hook fires, validation passes, no blocking error.
3. Use `/debug` to see hook execution in the agent logs.

### 📝 Exercise

Create a new hook in `.github/hooks/no-secrets.json` that fires on
`PreToolUse` and blocks any `editFiles` call to files in a `config/` folder.
This would prevent accidentally writing secrets to config files.

Hint: Use `PreToolUse` event and check for `permissionDecision: "deny"` in
output.

---

## Chapter 8: Custom Agents

**Files**: `.github/agents/*.agent.md`

**Concept**: Custom agents are specialized AI personas with defined tools,
instructions, and behaviors. Think of each one as a team member with a specific
role and limited access.

### The two example agents

#### 1. `task-analyst.agent.md` — Read-only analyst

```yaml
---
name: Task Analyst
description: "Use when analyzing task data, finding overdue items..."
tools: [read, search]
---
```

- **User-invocable**: Yes (default) — appears in the agent picker dropdown.
- **Tools**: Only `read` and `search` — cannot edit files or run commands.
- **Role**: Analyzes task data and answers questions about project status.

#### 2. `doc-writer.agent.md` — Subagent-only writer

```yaml
---
name: Doc Writer
description: "Use when generating or updating project documentation..."
tools: [read, search, edit]
user-invocable: false
---
```

- **`user-invocable: false`**: Hidden from the agent picker. Only accessible
  when another agent delegates to it as a subagent.
- **Tools**: Can `read`, `search`, and `edit` — but only Markdown files
  (enforced by instructions in the body).
- **Role**: Generates documentation when delegated to by a parent agent.

### Tool restrictions are your main lever

The `tools:` field defines what the agent can do:

```yaml
tools: [read, search]             # Read-only research
tools: [read, search, edit]       # Can modify files
tools: [read, edit, execute]      # Full access including terminal
tools: []                         # Conversational only — no tools at all
tools: [read, search, fetch/*]    # Read + MCP server tools
```

### Invocation control

| Setting | Effect |
|---------|--------|
| `user-invocable: true` (default) | Appears in agent picker |
| `user-invocable: false` | Hidden — subagent only |
| `disable-model-invocation: true` | Other agents cannot invoke as subagent |

### The `description` is the discovery surface

When a parent agent decides which subagent to delegate to, it reads the
`description` field. Include trigger phrases:

```yaml
# Good — specific trigger phrases
description: "Use when analyzing task data, finding overdue items..."

# Bad — vague, won't be discovered
description: "A helpful analysis tool"
```

### 🧪 Try It

1. In Chat, open the agent picker (dropdown at the top) and select **Task Analyst**.
2. Ask: "How many tasks are overdue?"
   - **Expected**: The Task Analyst reads `tasks.json`, identifies overdue items,
     and presents a Markdown summary. It does NOT try to edit files.
3. While using **Task Analyst**, ask: "Fix the overdue tasks."
   - **Expected**: The agent refuses or explains it cannot edit files — it only
     has `read` and `search` tools.
4. Switch back to the default **Agent** and ask: "Write a contributor guide for
   this project."
   - **Expected**: The main agent may delegate to the **Doc Writer** subagent
     (visible in agent logs via `/debug`).

### 📝 Exercise

Create `.github/agents/code-reviewer.agent.md` with:
- `tools: [read, search]` (read-only)
- Role: Reviews Python code for bugs, style issues, and missing tests
- `user-invocable: true`

Test it by selecting it from the agent picker and asking it to review
`src/task_utils.py`.

---

## Chapter 9: Skills

**Files**: `.github/skills/task-report/`

**Concept**: A skill is a folder containing a `SKILL.md` file plus supporting
assets (scripts, templates, reference docs). Skills represent multi-step
workflows and appear as `/` commands in chat — just like prompts, but with
bundled resources.

### Skill folder structure

```
.github/skills/task-report/
├── SKILL.md                          # Required — entry point
├── references/
│   └── report-format.md             # Output format specification
└── assets/
    └── report-template.md           # Markdown template with placeholders
```

### How progressive loading works

Skills load in three stages to conserve the context window:

| Stage | What loads | Size |
|-------|-----------|------|
| **Discovery** | `name` + `description` from frontmatter | ~100 tokens |
| **Instructions** | Full `SKILL.md` body | <5000 tokens |
| **Resources** | Referenced files (`references/`, `assets/`) | On demand |

This means the agent only loads the full skill content when it's relevant to
your request.

### The SKILL.md frontmatter

```yaml
---
name: task-report           # Must match the folder name!
description: "Generate a Markdown status report from data/tasks.json..."
argument-hint: "Optional: report scope like 'high priority only'"
---
```

Critical: The `name` field **must exactly match** the folder name
(`task-report`). A mismatch causes a silent failure.

### Slash command behavior

| Configuration | Slash command? | Auto-loaded by agents? |
|---------------|---------------|----------------------|
| Default (both omitted) | ✅ Yes | ✅ Yes |
| `user-invocable: false` | ❌ No | ✅ Yes |
| `disable-model-invocation: true` | ✅ Yes | ❌ No |
| Both set | ❌ No | ❌ No |

### 🧪 Try It

1. In Chat, type `/task-report`
   - **Expected**: Copilot loads the skill, reads `tasks.json`, applies the
     report template, and generates a formatted status report.
2. Type `/task-report overdue items only`
   - **Expected**: A filtered report focusing on overdue tasks.
3. Type `/debug` and inspect the context — you should see the skill was loaded
   progressively (first discovery, then instructions, then template).

### 📝 Exercise

Create a new skill `.github/skills/data-quality/`:

```
.github/skills/data-quality/
├── SKILL.md
└── references/
    └── quality-rules.md
```

The skill should:
- Check `tasks.json` against validation rules from the spec
- Report any issues (missing fields, invalid values, duplicate IDs)
- Reference the quality rules file for detailed criteria

Test with `/data-quality`.

---

## Chapter 10: MCP Integration

**File**: `.vscode/mcp.json`

**Concept**: MCP (Model Context Protocol) lets you connect Copilot to external
tools and services. An MCP server exposes tools that agents can invoke — like
database queries, API calls, or file system operations on remote machines.

### How MCP works

```
Agent  ──►  MCP Client (VS Code)  ──►  MCP Server  ──►  External Service
```

1. You configure MCP servers in `.vscode/mcp.json`.
2. VS Code discovers available tools from each server.
3. Agents can invoke these tools during conversations.

### The built-in `fetch` server

This project configures the simplest possible MCP server — VS Code's built-in
`fetch` server, which retrieves web content:

```json
{
  "servers": {
    "fetch": {
      "type": "copilot",
      "description": "Built-in web fetch tool — retrieves content from URLs."
    }
  }
}
```

- **`type: "copilot"`**: This is a built-in server — no installation needed.
- Agents can now use `#fetch` to retrieve web pages.

### Server types

| Type | Where it runs | Example |
|------|--------------|---------|
| `copilot` | Built-in to VS Code | `fetch` |
| `stdio` | Local process (stdin/stdout) | Anthropic's `filesystem` MCP server |
| `sse` | Remote HTTP server | Cloud APIs |

### Referencing MCP tools in agents

You can give a custom agent access to MCP tools:

```yaml
# In an .agent.md frontmatter
tools: [read, search, fetch/*]    # Built-in tools + all fetch server tools
tools: [read, myserver/*]          # Built-in read + all tools from "myserver"
```

### Example: stdio MCP server config

For a more advanced setup, here's how you'd configure a local MCP server
(not included in this project, but shown for reference):

```json
{
  "servers": {
    "my-db-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@example/db-mcp-server"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432"
      }
    }
  }
}
```

### 🧪 Try It

1. In Chat, type: `Summarize the latest VS Code release notes #fetch https://code.visualstudio.com/updates`
   - **Expected**: Copilot fetches the page via the MCP fetch server and
     summarizes the content.
2. Use `/tools` to see the list of available tools — `fetch` should appear.
3. Use `/debug` to see the MCP tool invocation in the agent logs.

### 📝 Exercise

Research an MCP server for a tool your team uses (e.g., Jira, database,
Confluence). Add it to `.vscode/mcp.json` and reference its tools from the
Task Analyst agent. Test that the agent can invoke the external tool.

---

# Appendices

---

## Appendix A: Decision Flow

Use this flowchart to choose the right primitive for your need:

```
Is this guidance that should apply to EVERY request?
├── Yes → Workspace Instructions (.github/copilot-instructions.md)
└── No
    ├── Does it apply to specific FILE TYPES?
    │   └── Yes → File Instructions with applyTo (.github/instructions/)
    ├── Does it apply to specific TASKS?
    │   └── Yes → File Instructions with description only
    ├── Is it a REPEATABLE single task?
    │   └── Yes → Prompt File (.github/prompts/)
    ├── Is it a MULTI-STEP workflow with templates/scripts?
    │   └── Yes → Skill (.github/skills/)
    ├── Does it need ROLE-BASED tool restrictions?
    │   └── Yes → Custom Agent (.github/agents/)
    ├── Must behavior be DETERMINISTICALLY enforced?
    │   └── Yes → Hook (.github/hooks/)
    └── Does it need EXTERNAL tools/services?
        └── Yes → MCP Server (.vscode/mcp.json)
```

### Quick Decision Table

| Need | Use |
|------|-----|
| "Always follow these conventions" | Workspace Instructions |
| "Python files should use type hints" | File Instructions (`applyTo`) |
| "When writing docs, follow this style" | File Instructions (description) |
| "Generate tests for selected code" | Prompt File |
| "Run this complete reporting workflow" | Skill |
| "This agent can only read, not edit" | Custom Agent |
| "Block edits if validation fails" | Hook |
| "Query our Jira/database from chat" | MCP Server |

---

## Appendix B: Common Pitfalls & Debugging

### Debugging tools

| Tool | What it shows |
|------|-------------|
| `/debug` | Opens Chat Debug view — system prompt, loaded context, tool invocations |
| `/troubleshoot` | AI analysis of debug logs for the current session |
| Agent Logs | Chronological event log (View → Output → select "Agent" channel) |

### Common pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Instruction not loading | Vague `description` without trigger keywords | Use `"Use when..."` pattern with specific keywords |
| Instruction always loading | `applyTo: "**"` on a narrow concern | Use specific globs: `"src/**/*.py"` |
| Skill not appearing as `/` command | Folder name doesn't match `name` in SKILL.md | Ensure exact match: folder `task-report` → `name: task-report` |
| Hook not firing | Wrong event or JSON syntax error | Validate JSON, check event name matches exactly |
| YAML frontmatter silently failing | Unescaped colons, tabs instead of spaces | Quote descriptions with colons: `description: "Use when: doing X"` |
| Agent not discovered as subagent | Vague description | Include specific trigger phrases in description |
| MCP server not available | Config error or server not installed | Check `.vscode/mcp.json` syntax, verify server is accessible |
| Both `copilot-instructions.md` and `AGENTS.md` | Conflicting workspace instructions | Use only one — `copilot-instructions.md` recommended |

### Testing checklist

After creating any customization file:

- [ ] YAML frontmatter parses (no tabs, colons are quoted)
- [ ] `description` uses "Use when..." pattern
- [ ] `applyTo` globs match real files
- [ ] Skill folder name = SKILL.md `name` field
- [ ] Hook JSON is valid and script paths are correct
- [ ] Use `/debug` to verify the file loads when expected

---

## Appendix C: File Reference

| Type | Location | Frontmatter | Discovery |
|------|----------|-------------|-----------|
| Workspace Instructions | `.github/copilot-instructions.md` | None | Always loaded |
| File Instructions | `.github/instructions/*.instructions.md` | `description`, `applyTo` | Explicit (glob) or on-demand (description) |
| Prompts | `.github/prompts/*.prompt.md` | `description`, `agent`, `argument-hint`, `model`, `tools` | `/` command or manual |
| Hooks | `.github/hooks/*.json` | None (JSON) | Automatic at lifecycle events |
| Custom Agents | `.github/agents/*.agent.md` | `description`, `tools`, `user-invocable`, `model` | Agent picker or subagent delegation |
| Skills | `.github/skills/<name>/SKILL.md` | `name`, `description`, `argument-hint` | `/` command or agent auto-load |
| MCP Config | `.vscode/mcp.json` | None (JSON) | Automatic tool discovery |

### User-level locations (personal, not version-controlled)

| Type | Location |
|------|----------|
| Instructions | `<profile>/instructions/*.instructions.md` |
| Prompts | `<profile>/prompts/*.prompt.md` |
| Agents | `<profile>/agents/*.agent.md` |

Where `<profile>` is your VS Code user profile prompts folder
(`%APPDATA%\Code\User\prompts\` on Windows).

---

## Appendix D: Complete Slash Command Reference

All `/` commands available in VS Code Copilot Chat, organized by category.

### Coding Actions

| Command | Description |
|---------|-------------|
| `/explain` | Explain selected code — purpose, logic, edge cases |
| `/fix` | Propose fixes for errors guided by Problems panel or stack traces |
| `/tests` | Generate tests using your project's test framework conventions |
| `/doc` | Generate documentation comments (inline chat) |
| `/setupTests` | Scaffold a test framework — config, deps, example tests |
| `/fixTestFailure` | Analyze failing tests and suggest fixes |

### Scaffolding

| Command | Description |
|---------|-------------|
| `/new` | Create a new file or project from natural language description |
| `/newNotebook` | Create a new Jupyter notebook from a description |

### Session Management

| Command | Description |
|---------|-------------|
| `/clear` | Archive current session and start fresh |
| `/fork` | Copy conversation into a new independent session |
| `/compact` | Summarize history to free context window space |
| `/rename` | Rename the current chat session |

### Planning & Search

| Command | Description |
|---------|-------------|
| `/plan` | Create a detailed step-by-step implementation plan |
| `/search` | Semantic search across workspace |
| `/startDebugging` | Generate `launch.json` and start a debug session |

### Customization Creators

| Command | What it creates |
|---------|----------------|
| `/init` | `copilot-instructions.md` from project structure |
| `/create-prompt` | `.prompt.md` file |
| `/create-instruction` | `.instructions.md` file |
| `/create-skill` | Skill folder with `SKILL.md` |
| `/create-agent` | `.agent.md` file |
| `/create-hook` | Hook `.json` configuration |
| `/agent-customization` | Opens the agent customization workflow |

### Management UIs

| Command | Opens |
|---------|-------|
| `/agents` | Custom agents list |
| `/hooks` | Hook configurations |
| `/instructions` | Instruction files |
| `/prompts` | Prompt files |
| `/skills` | Agent skills |
| `/tools` | Tool availability and permissions |
| `/models` | AI model picker |
| `/plugins` | Chat plugins and extensions |

### Permission Control

| Command | Description |
|---------|-------------|
| `/autoApprove` | Auto-approve all tool calls (skip confirmations) |
| `/disableAutoApprove` | Re-enable tool call confirmations |
| `/yolo` | Maximum autonomy — auto-approve + auto-respond |
| `/disableYolo` | Return to normal approval mode |

### Debug & Troubleshoot

| Command | Description |
|---------|-------------|
| `/debug` | Open Chat Debug view — inspect prompts, context, and tools |
| `/troubleshoot` | AI analysis of agent debug logs for current session |

### Custom Commands

| Command | Description |
|---------|-------------|
| `/<prompt-name>` | Run a prompt file (e.g., `/generate-test-cases`) |
| `/<skill-name>` | Run a skill (e.g., `/task-report`) |

---

## Appendix E: `@` and `#` Cheat Sheet

### `@` Chat Participants

| Participant | Domain | Example |
|-------------|--------|---------|
| `@vscode` | VS Code features, settings, keybindings | `@vscode how to change theme?` |
| `@terminal` | Shell commands, terminal help | `@terminal how to find large files?` |
| `@github` | GitHub repos, PRs, issues, commits | `@github show my open PRs` |

> Extensions can add more `@` participants. Type `@` in chat to see all available.

### `#` Context References

| Reference | What it adds to context |
|-----------|------------------------|
| `#file:path` | A specific file |
| `#folder:path` | All files in a directory |
| `#symbol:name` | A function, class, or variable |
| `#codebase` | Semantic search across the entire workspace |
| `#selection` | Current editor text selection |
| `#changes` | Uncommitted source control changes |

### `#` Tool References

| Tool | What it does |
|------|-------------|
| `#fetch` | Retrieve content from a URL |
| `#terminalSelection` | Read the current terminal selection |
| `#terminalLastCommand` | Get the last terminal command and output |
| `#problems` | Workspace errors and warnings |

### Tool Set Aliases (for `tools:` frontmatter)

| Alias | Capability |
|-------|-----------|
| `read` | Read files, notebook summaries, terminal output |
| `edit` | Create/edit files and notebooks |
| `execute` | Run terminal commands, notebook cells, tasks |
| `search` | File search, text search, codebase search, directory listing |
| `web` | Fetch web content |
| `agent` | Delegate to subagents |
| `vscode` | VS Code commands, extensions |
| `browser` | Interact with integrated browser (experimental) |
| `todos` | Manage task lists in chat |

### Drag & Drop Context

| Source | Drop target |
|--------|-----------|
| Explorer file or tab | Chat view |
| Explorer folder | Chat view |
| Problems panel item | Chat view |
| Browser image | Chat view |
| External image file | Chat view |

---

## Project File Map

```
copilot-features-demo/
├── .github/
│   ├── copilot-instructions.md              ← Ch. 4: Workspace Instructions
│   ├── instructions/
│   │   ├── data-files.instructions.md       ← Ch. 5: Explicit (glob)
│   │   ├── python-style.instructions.md     ← Ch. 5: Explicit (glob)
│   │   └── documentation.instructions.md    ← Ch. 5: On-demand (description)
│   ├── prompts/
│   │   ├── generate-test-cases.prompt.md    ← Ch. 6: Prompt (agent mode)
│   │   └── summarize-tasks.prompt.md        ← Ch. 6: Prompt (argument-hint)
│   ├── hooks/
│   │   └── validate-json.json               ← Ch. 7: PostToolUse hook
│   ├── agents/
│   │   ├── task-analyst.agent.md            ← Ch. 8: Read-only agent
│   │   └── doc-writer.agent.md              ← Ch. 8: Subagent-only
│   └── skills/
│       └── task-report/                     ← Ch. 9: Skill
│           ├── SKILL.md
│           ├── references/report-format.md
│           └── assets/report-template.md
├── .vscode/
│   └── mcp.json                             ← Ch. 10: MCP config
├── data/
│   └── tasks.json                           ← Sample task data
├── docs/
│   └── task-tracker-spec.md                 ← Domain specification
├── scripts/
│   ├── validate.sh                          ← Data validation (macOS/Linux)
│   ├── validate.ps1                         ← Data validation (Windows)
│   └── hooks/
│       ├── enforce-todo-format.sh           ← Hook script (macOS/Linux)
│       └── enforce-todo-format.ps1          ← Hook script (Windows)
├── src/
│   └── task_utils.py                        ← Python utilities
├── .gitignore
└── README.md                                ← This file
```
