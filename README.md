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
- [Chapter 0: Git & GitHub Essentials](#chapter-0--git--github-essentials)
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

This project uses a minimal **WiFi site-survey toolkit** as its domain:
- `data/ap_inventory.json` — 8 sample access points with deployment statuses, signal quality, and locations
- `src/wifi_utils.py` — Python utilities for loading and analysing AP data
- `docs/wifi-survey-spec.md` — the survey data specification
- `scripts/validate.sh` / `validate.ps1` — AP inventory validation scripts

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
git commit -m "Initial commit: WiFi site-survey toolkit"
```

**On macOS / Linux (Terminal):**

```bash
cd ~/path/to/copilot-features-demo
git init
git add .
git commit -m "Initial commit: WiFi site-survey toolkit"
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

## Chapter 0 · Git & GitHub Essentials

**Concept**: Git is the version control system that tracks every change you make
to your project. GitHub is the cloud platform that hosts your Git repositories
and enables collaboration. Understanding both is essential — Copilot's
customization files (instructions, prompts, hooks, agents, skills) are all
designed to be version-controlled and shared via Git.

### Why this matters for Copilot

- Every customization file you create in `.github/` should be committed so your
  team shares the same AI behavior.
- Copilot can read your Git history (`#changes`, `git log`) to generate commit
  messages, summarize work, and understand project evolution.
- Hooks (Chapter 7) rely on Git to revert failed edits.

### Git Command Reference

#### Configuration

| Command | What it does | Example |
|---------|-------------|---------|
| `git config --global user.name "Name"` | Sets your name for all commits | `git config --global user.name "Alice Smith"` |
| `git config --global user.email "email"` | Sets your email for all commits | `git config --global user.email "alice@example.com"` |
| `git config --list` | Shows all current configuration values | Check what name/email is set |

#### Repository Setup

| Command | What it does | Example |
|---------|-------------|---------|
| `git init` | Creates a new Git repository in the current directory | Start tracking a new project |
| `git clone <url>` | Downloads a repository from GitHub to your machine | `git clone https://github.com/user/repo.git` |

#### Staging & Committing

| Command | What it does | Example |
|---------|-------------|---------|
| `git status` | Shows which files are modified, staged, or untracked | Check what changed before committing |
| `git add <file>` | Stages a specific file for the next commit | `git add src/wifi_utils.py` |
| `git add .` | Stages all changed files in the current directory | Stage everything at once |
| `git commit -m "message"` | Saves staged changes as a new commit | `git commit -m "feat(survey): add channel-overlap detection"` |
| `git commit --amend` | Modifies the most recent commit (message or content) | Fix a typo in your last commit message |

#### Viewing History

| Command | What it does | Example |
|---------|-------------|---------|
| `git log` | Shows the full commit history | Review all past commits |
| `git log --oneline` | Shows a compact one-line-per-commit history | Quick overview of recent work |
| `git log --graph --oneline` | Shows commit history as a visual branch graph | Understand branching and merges |
| `git diff` | Shows unstaged changes line by line | See exactly what you changed |
| `git diff --staged` | Shows staged changes (what will be committed) | Review before committing |
| `git show <commit>` | Shows the details and diff of a specific commit | `git show abc1234` |

#### Branching & Merging

| Command | What it does | Example |
|---------|-------------|---------|
| `git branch` | Lists all local branches | See which branches exist |
| `git branch <name>` | Creates a new branch | `git branch feature/channel-overlap` |
| `git checkout <branch>` | Switches to an existing branch | `git checkout main` |
| `git checkout -b <name>` | Creates and switches to a new branch in one step | `git checkout -b fix/weak-signal-threshold` |
| `git merge <branch>` | Merges the specified branch into the current branch | `git merge feature/channel-overlap` |
| `git branch -d <name>` | Deletes a branch that has been merged | `git branch -d feature/channel-overlap` |

#### Remote Repositories (GitHub)

| Command | What it does | Example |
|---------|-------------|---------|
| `git remote -v` | Shows configured remote repositories | Verify your GitHub remote URL |
| `git remote add origin <url>` | Connects your local repo to a GitHub repo | `git remote add origin https://github.com/user/repo.git` |
| `git push -u origin main` | Pushes your local `main` branch to GitHub (first time) | Publish your project to GitHub |
| `git push` | Pushes committed changes to the remote | Share your latest commits |
| `git pull` | Fetches and merges remote changes into your branch | Get your teammate's latest work |
| `git fetch` | Downloads remote changes without merging | Check what's new before merging |

#### Undoing Changes

| Command | What it does | Example |
|---------|-------------|---------|
| `git checkout -- <file>` | Discards unstaged changes to a file | Revert a file to its last committed state |
| `git restore <file>` | Discards unstaged changes (modern syntax) | `git restore src/wifi_utils.py` |
| `git restore --staged <file>` | Unstages a file (keeps your edits) | `git restore --staged data/ap_inventory.json` |
| `git reset --soft HEAD~1` | Undoes the last commit but keeps changes staged | Redo a commit with a better message |
| `git stash` | Temporarily shelves uncommitted changes | Switch branches without committing |
| `git stash pop` | Restores the most recently stashed changes | Resume work after switching back |

#### GitHub-Specific Workflows

| Command / Action | What it does | Example |
|-----------------|-------------|---------|
| `git push` then open PR on GitHub | Proposes changes for team review | Standard collaboration workflow |
| **Fork** (GitHub UI) | Creates your own copy of someone else's repository | Contribute to open-source projects |
| **Pull Request** (GitHub UI) | Requests that your branch be merged into the main branch | Code review before merging |
| **Issue** (GitHub UI) | Tracks a bug, feature request, or task | Organize project work |
| `gh pr create` | Creates a pull request from the CLI (GitHub CLI) | `gh pr create --title "Add channel-overlap detection" --body "..."` |
| `gh issue list` | Lists open issues from the CLI (GitHub CLI) | `gh issue list --label rf-issue` |

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Configure Git and make your first commit

**What you'll do**: Set up Git identity and create an initial commit.

**Step 1 — Check your Git configuration**
- Open the integrated terminal: **Ctrl+`** (backtick).
- Run:
  ```powershell
  git config --global user.name
  git config --global user.email
  ```
- **What you see**: Your configured name and email. If blank, set them:
  ```powershell
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

**Step 2 — Initialize and commit**
- If you haven't already initialized git (from Getting Started), run:
  ```powershell
  cd C:\Projects\copilot-features-demo
  git init
  git add .
  git commit -m "Initial commit: Copilot features demo"
  ```
- **What you see**: A message like `[main (root-commit) abc1234] Initial commit...`
  confirming the snapshot was saved.

**Step 3 — View the commit**
- Run:
  ```powershell
  git log --oneline
  ```
- **What you see**: A single line showing the commit hash and message.

---

#### Exercise 2 · Track changes with `git status` and `git diff`

**What you'll do**: Make a small edit to the WiFi utilities and observe
how Git tracks it.

**Step 1** — Open `src/wifi_utils.py` and add a comment at the top:
```python
# Channel planning constants
```
Save the file (**Ctrl+S**).

**Step 2** — In the terminal, run:
```powershell
git status
```
- **What you see**: `src/wifi_utils.py` listed under **Changes not staged for
  commit** — Git detected your edit.

**Step 3** — Run:
```powershell
git diff
```
- **What you see**: A line-by-line diff showing the added comment in green
  with a `+` prefix.

**Step 4 — Stage and commit**
```powershell
git add src/wifi_utils.py
git commit -m "docs(wifi_utils): add channel planning constants comment"
```

**Step 5 — Verify**
```powershell
git log --oneline
```
- **What you see**: Two commits — your new one on top.

**Step 6 — Clean up**
- Remove the practice comment from `src/wifi_utils.py` and commit:
  ```powershell
  git add src/wifi_utils.py
  git commit -m "chore: remove practice comment"
  ```

---

#### Exercise 3 · Create and merge a branch

**What you'll do**: Practice the branch-edit-merge workflow — simulating
a new AP deployment update on a feature branch.

**Step 1 — Create a branch**
```powershell
git checkout -b feature/add-floor3-aps
```
- **What you see**: `Switched to a new branch 'feature/add-floor3-aps'`.

**Step 2 — Make an edit on the branch**
- Open `data/ap_inventory.json` and add a temporary field to any AP
  (e.g., `"note": "pending floor 3 survey"`).
- Stage and commit:
  ```powershell
  git add data/ap_inventory.json
  git commit -m "feat(survey): add floor 3 deployment note"
  ```

**Step 3 — Switch back and merge**
```powershell
git checkout main
git merge feature/add-floor3-aps
```
- **What you see**: A fast-forward merge message — the change from your
  branch is now on `main`.

**Step 4 — Delete the branch**
```powershell
git branch -d feature/add-floor3-aps
```

**Step 5 — Clean up**
- Revert the temporary edit:
  ```powershell
  git checkout -- data/ap_inventory.json
  git commit -am "chore: revert temporary note field"
  ```

---

#### Exercise 4 · Use `git stash` to shelve work temporarily

**What you'll do**: Stash uncommitted changes so you can switch context
without losing work — for example, pausing an AP config update to handle
an urgent channel-conflict fix.

**Step 1** — Open `src/wifi_utils.py` and add a new comment:
```python
# TODO: add DFS channel fallback logic
```
Save but **do not commit**.

**Step 2** — Run:
```powershell
git stash
```
- **What you see**: `Saved working directory and index state...`. Your edit
  disappears from the file.

**Step 3** — Verify the file is clean:
```powershell
git status
```
- **What you see**: `nothing to commit, working tree clean`.

**Step 4** — Restore your stashed changes:
```powershell
git stash pop
```
- **What you see**: Your comment reappears in the file. The stash is removed.

**Step 5 — Clean up**
- Discard the practice edit:
  ```powershell
  git checkout -- src/wifi_utils.py
  ```

---

#### Exercise 5 · View detailed commit history

**What you'll do**: Explore different ways to read the project history.

**Step 1 — Full log**
```powershell
git log
```
- **What you see**: Each commit with its full hash, author, date, and message.
  Press **q** to exit the pager.

**Step 2 — Compact log**
```powershell
git log --oneline
```

**Step 3 — Graph view**
```powershell
git log --graph --oneline --all
```
- **What you see**: A text-based branch graph showing how commits relate.

**Step 4 — Inspect a single commit**
- Copy a commit hash from the log, then run:
  ```powershell
  git show <hash>
  ```
  (Replace `<hash>` with the actual hash.)
- **What you see**: The commit metadata and the full diff of what changed.

---

#### Exercise 6 · Undo mistakes safely

**What you'll do**: Practice reverting changes without losing work —
essential when experimenting with AP configuration updates.

**Step 1 — Discard an unstaged edit**
- Edit `src/wifi_utils.py` (e.g., change a tx_power default), save, then run:
  ```powershell
  git restore src/wifi_utils.py
  ```
- **What you see**: The file reverts to its last committed state.

**Step 2 — Unstage a file**
- Make an edit, stage it, then unstage:
  ```powershell
  git add src/wifi_utils.py
  git restore --staged src/wifi_utils.py
  ```
- **What you see**: `git status` now shows the file as modified but
  **not staged**. Your edits are still in the file.

**Step 3 — Soft-reset the last commit**
- Make a throwaway commit:
  ```powershell
  git add src/wifi_utils.py
  git commit -m "throwaway commit"
  ```
- Undo it (keeps changes staged):
  ```powershell
  git reset --soft HEAD~1
  ```
- **What you see**: `git log --oneline` no longer shows "throwaway commit",
  but `git status` shows your changes still staged.

**Step 4 — Clean up**
```powershell
git restore --staged src/wifi_utils.py
git restore src/wifi_utils.py
```

---

#### Exercise 7 · Connect to GitHub and push

**What you'll do**: Link your local WiFi survey repository to GitHub and
push your commits so the team can access the AP inventory.

> **Prerequisite**: You need a GitHub account and a repository created on
> GitHub (empty — no README or .gitignore).

**Step 1 — Create a GitHub repository**
- Go to [https://github.com/new](https://github.com/new).
- Name it `wifi-site-survey` (or any name).
- Leave it **empty** (no README, no .gitignore, no license).
- Click **Create repository**.

**Step 2 — Add the remote**
```powershell
git remote add origin https://github.com/YOUR-USERNAME/wifi-site-survey.git
```
(Replace `YOUR-USERNAME` with your GitHub username.)

**Step 3 — Push**
```powershell
git push -u origin main
```
- **What you see**: Git uploads your commits to GitHub. Visit the repository
  URL in your browser to confirm.

**Step 4 — Verify the remote**
```powershell
git remote -v
```
- **What you see**: The `origin` URL pointing to your GitHub repository.

---

#### Exercise 8 · Use Copilot with Git context

**What you'll do**: Combine Copilot's `#changes` context mention with Git
to generate a commit message automatically for an AP inventory update.

**Step 1** — Open `data/ap_inventory.json` and update the `tx_power` value
of any access point. Save the file. **Do not commit.**

**Step 2** — Open Chat (**Ctrl+Alt+I**) and type:
```
Write a conventional commit message for #changes
```
Press **Enter**.

- **What you see**: Copilot reads your uncommitted diff via Git and produces
  a Conventional Commits message (e.g., `fix(survey): update tx_power for AP-03`).

**Step 3** — Copy the message and use it:
```powershell
git add .
git commit -m "<paste the message here>"
```

> **Key insight**: This is where Git and Copilot complement each other —
> Copilot understands your Git state and can automate repetitive Git tasks
> like writing commit messages.

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

| Command | What it does | Example |
|---------|-------------|--------|
| `/explain` | Explains selected code — purpose, logic, edge cases | You inherited `find_weak_signals` and don't know what it does — select it and use `/explain` |
| `/fix` | Proposes fixes for errors (reads Problems panel / stack traces) | A red underline appears under your code and you're unsure why — use `/fix` to let Copilot read the error and suggest a fix |
| `/tests` | Generates tests for selected code using your project's test framework | You just wrote `filter_aps_by_band` but have no tests yet — select it and use `/tests` |
| `/doc` | Generates documentation comments (inline chat) | You wrote a utility function but left no docstring — select it and use `/doc` in inline chat |
| `/setupTests` | Scaffolds a test framework (config, dependencies, example tests) | Your project has no test framework and you don't want to configure it manually — use `/setupTests` |
| `/fixTestFailure` | Analyzes failing tests and suggests fixes | A pytest run just failed with an unclear error — use `/fixTestFailure` to let Copilot diagnose it |

### Category 2: Scaffolding

| Command | What it does | Example |
|---------|-------------|--------|
| `/new` | Creates a new file or project from a description | You need a new utility script but don't want to write boilerplate — use `/new Python script that reads a CSV` |
| `/newNotebook` | Creates a new Jupyter notebook from a description | You want to explore `ap_inventory.json` interactively — use `/newNotebook analyze ap_inventory.json` |

### Category 3: Session Management

| Command | What it does | Example |
|---------|-------------|--------|
| `/clear` | Starts a fresh chat session (archives current one) | You finished one task and want a clean slate for the next — use `/clear` |
| `/fork` | Copies the conversation into a new independent session | You want to try a different approach without losing the current conversation — use `/fork` |
| `/compact` | Summarizes conversation history to free context window space | Your chat history grew long and Copilot is losing early context — use `/compact` |
| `/rename` | Renames the current chat session (for organization) | You want to find this session later by topic — use `/rename Fix channel-overlap detection` |

### Category 4: Planning & Search

| Command | What it does | Example |
|---------|-------------|--------|
| `/plan` | Creates a step-by-step implementation plan before writing code | Before coding a new feature, you want to see all steps outlined first — use `/plan Add channel-overlap detection to wifi_utils.py` |
| `/search` | Semantic search across your workspace | You can't remember where AP schema validation is implemented — use `/search where is AP status validated` |
| `/startDebugging` | Generates a `launch.json` and starts a debug session | You want to debug `wifi_utils.py` but have no launch config — use `/startDebugging` |

### Category 5: Customization Creators

These create the files you'll learn about in Part B:

| Command | What it creates | Example |
|---------|----------------|--------|
| `/init` | Generates `copilot-instructions.md` from your project structure | You opened a new project and want Copilot to generate workspace instructions automatically — use `/init` |
| `/create-prompt` | Creates a `.prompt.md` file | You keep typing the same changelog task in chat — turn it into a reusable command with `/create-prompt Generate a changelog` |
| `/create-instruction` | Creates a `.instructions.md` file | You want all TypeScript files to follow specific style rules — use `/create-instruction for TypeScript files` |
| `/create-skill` | Creates a `SKILL.md` and skill folder | You want to package a multi-step RF coverage audit workflow with templates — use `/create-skill rf-coverage-audit` |
| `/create-agent` | Creates an `.agent.md` file | You need a read-only agent that can only review AP data, not edit it — use `/create-agent rf-analyst` |
| `/create-hook` | Creates a hook `.json` config | You want to automatically block any edit that produces invalid JSON — use `/create-hook to block invalid JSON` |
| `/agent-customization` | Opens the agent customization workflow | You're new to agent config and want a guided setup walkthrough — use `/agent-customization` |

### Category 6: Management UIs

These open configuration panels for managing customization files:

| Command | Opens | Example |
|---------|-------|--------|
| `/agents` | Custom agents configuration | You want to check which custom agents exist in this project — use `/agents` |
| `/hooks` | Hook configuration | You want to verify that `validate-json.json` is configured correctly — use `/hooks` |
| `/instructions` | Instruction files | You want to see which instruction files are currently active — use `/instructions` |
| `/prompts` | Prompt files | You forgot the name of the test-generation prompt — use `/prompts` to find it |
| `/skills` | Agent skills | You want to review the `wifi-survey-report` skill before invoking it — use `/skills` |
| `/tools` | Tool availability and permissions | Your agent isn't finding files and you suspect a tool is disabled — use `/tools` |
| `/models` | AI model picker | You want a faster model for a quick question — use `/models` to switch |
| `/plugins` | Chat plugins/extensions | You want to see which chat extensions are installed and active — use `/plugins` |

### Category 7: Permission Control

| Command | What it does | Example |
|---------|-------------|--------|
| `/autoApprove` | Auto-approve all tool calls (skip confirmation dialogs) | You're running a large automated refactor and don't want a confirmation dialog on every file edit — use `/autoApprove` |
| `/disableAutoApprove` | Re-enable confirmation dialogs | You've finished the bulk refactor and want to review each tool call individually again — use `/disableAutoApprove` |
| `/yolo` | Maximum autonomy — auto-approve + auto-respond to questions | You're in a throwaway sandbox and want Copilot to work end-to-end without any prompts — use `/yolo` |
| `/disableYolo` | Return to normal approval mode | You're done experimenting and want to restore normal confirmation and approval — use `/disableYolo` |

> **Warning**: `/yolo` mode gives Copilot full autonomy with no confirmation
> prompts. Use it only in safe environments where you understand the
> consequences.

### Category 8: Debugging

| Command | What it does | Example |
|---------|-------------|--------|
| `/debug` | Opens the Chat Debug view — inspect system prompts, tools, and context that Copilot received | Your instruction file doesn't seem to be loading — use `/debug` to inspect exactly what Copilot received |
| `/troubleshoot` | Analyzes agent debug logs for the current session | An agent produced unexpected output and you can't tell why — use `/troubleshoot` to have Copilot analyze its own logs |

### Key Insight

**Custom prompts and skills also appear as `/` commands.** Once you create a
prompt file (`.prompt.md`) or a skill (`SKILL.md`), you can invoke them by
typing `/` followed by the file name. For example, this project includes
`/generate-test-cases` and `/summarize-aps` (prompts) and `/wifi-survey-report`
(skill).

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Explain then test a function

**What you'll do**: Use `/explain` and `/tests` on a real WiFi analysis
function in this project.

**Step 1 — Open the file**
- In VS Code, press **Ctrl+P** (Windows/Linux) or **Cmd+P** (macOS).
- Type `wifi_utils.py` and press **Enter**.

**Step 2 — Select the function**
- Scroll to the `find_weak_signals` function (around line 30).
- Click the function name, then press **Ctrl+Shift+K** to select the whole block,
  or click and drag to highlight the entire function body.

**Step 3 — Explain it**
- Open Chat: **Ctrl+Alt+I** (Windows/Linux) or **Cmd+Alt+I** (macOS).
- Type `/explain` and press **Enter**.
- **What you see**: Copilot describes what `find_weak_signals` does, what
  parameters it takes, what it returns, and any edge cases (e.g., what happens
  if the signal threshold is missing or a tx_power value is malformed).

**Step 4 — Generate tests**
- Keep the same selection in the editor.
- In Chat, type `/tests` and press **Enter**.
- **What you see**: Copilot generates a `test_find_weak_signals.py` file (or
  inline code) with at least three pytest test cases: a happy path, an empty
  list case, and an edge case with a missing tx_power field.

> **Why it works**: `/explain` and `/tests` use the current editor *selection* as
> context. If nothing is selected, Copilot uses the entire active file.

---

#### Exercise 2 · Plan before coding

**What you'll do**: Use `/plan` to get a structured implementation plan for
a new WiFi analysis feature.

**Step 1** — In Chat, type exactly:
```
/plan Add a function to detect channel conflicts between nearby access points
```
Press **Enter**.

**Step 2 — Read the plan**
- **What you see**: Copilot returns a numbered list of steps — e.g.,
  *"1. Define function signature with type hints"*, *"2. Group APs by
  channel and band"*, *"3. Flag overlapping channels within the same
  location zone"*, etc. — without writing any code yet.
- Notice that `/plan` **does not modify any files**. It only plans.

**Step 3 — Approve and implement**
- Reply in Chat: `Looks good, implement it.`
- **What you see**: Copilot now writes the function into `wifi_utils.py`,
  following the plan it just outlined.

---

#### Exercise 3 · Inspect what Copilot sees

**What you'll do**: Use `/debug` to see the exact context injected into each request.

**Step 1** — In Chat, type `/debug` and press **Enter**.
- **What you see**: The Chat Debug view opens — a panel showing the full system
  prompt, which instruction files were loaded, and what tools are available.

**Step 2 — Look for workspace instructions**
- Scroll through the debug output until you find a section labelled
  `copilot-instructions.md` or similar. This is the project-level context
  from `.github/copilot-instructions.md`.

---

#### Exercise 4 · Free up context window space

**What you'll do**: Use `/compact` after a long conversation.

**Step 1** — Send 4–5 messages in the same chat session (e.g., ask a few
questions about `ap_inventory.json` or the channel-overlap function you
just planned).

**Step 2** — In Chat, type `/compact` and press **Enter**.
- **What you see**: Copilot summarises the conversation history into a short
  paragraph and replaces the raw history with the summary.
- The token count shown in the debug view drops significantly.

> **When to use this**: Use `/compact` when you notice Copilot forgetting earlier
> context in a long session. It is the fastest way to reclaim context window
> space without ending the session.

---

#### Exercise 5 · Fix an error with `/fix` and add docs with `/doc`

**What you'll do**: Use `/fix` to resolve a real error and `/doc` to generate a
docstring through inline chat.

**Step 1 — Introduce an error**
- Open `src/wifi_utils.py`.
- Temporarily break a function: delete the `:` at the end of any `def` line
  and save (**Ctrl+S**).
- The Problems panel (View → Problems) will show a red error.

**Step 2 — Fix it with `/fix`**
- In Chat, type `/fix` and press **Enter**.
- **What you see**: Copilot reads the Problems panel, identifies the syntax
  error, and proposes the corrected line. Accept the suggestion to restore
  the file.

**Step 3 — Add a docstring with `/doc`**
- Select the `find_weak_signals` function (or any function without a docstring).
- Press **Ctrl+I** (Windows/Linux) or **Cmd+I** (macOS) to open **inline chat**.
- Type `/doc` and press **Enter**.
- **What you see**: Copilot inserts a docstring directly above the function body
  — in-place in the editor, not in the chat panel.

---

#### Exercise 6 · Scaffold with `/new`, `/newNotebook`, and `/setupTests`

**What you'll do**: Create new files and scaffold a test framework without
writing boilerplate.

**Step 1 — Create a new utility script**
- In Chat, type:
  ```
  /new Python script that reads ap_inventory.json and prints a signal-strength summary table
  ```
  Press **Enter**.
- **What you see**: Copilot creates a new `.py` file with boilerplate imports,
  argument parsing, and the core logic sketched out. A file picker may ask
  where to save it.

**Step 2 — Create a Jupyter notebook**
- In Chat, type:
  ```
  /newNotebook analyze ap_inventory.json — show AP distribution by band as a bar chart
  ```
  Press **Enter**.
- **What you see**: A new `.ipynb` file opens with cells for loading the JSON,
  computing counts by band (2.4 GHz / 5 GHz / 6 GHz), and plotting with
  matplotlib.

**Step 3 — Scaffold a test framework**
- In Chat, type `/setupTests` and press **Enter**.
- **What you see**: Copilot detects the project uses Python and generates a
  `pytest.ini` (or `pyproject.toml` section), installs pytest, and creates
  an example test file. If pytest is already configured it reports that.

---

#### Exercise 7 · Manage sessions — `/clear`, `/fork`, and `/rename`

**What you'll do**: Organise your chat sessions so you can find them later and
work in parallel without losing context.

**Step 1 — Rename the current session**
- In Chat, type:
  ```
  /rename Chapter 1 WiFi analysis slash commands
  ```
  Press **Enter**.
- **What you see**: The session tab or title updates to *"Chapter 1 WiFi
  analysis slash commands"*. Useful for finding sessions in Chat history.

**Step 2 — Fork a session**
- In Chat, type `/fork` and press **Enter**.
- **What you see**: A **new** chat session opens containing a copy of the
  current conversation. Changes in the fork don't affect the original.
- Use this when you want to try a risky or experimental approach while
  preserving the current thread.

**Step 3 — Clear and start fresh**
- In the forked session, type `/clear` and press **Enter**.
- **What you see**: The current session is archived and a blank new session
  opens. The previous conversation is still accessible in Chat history.

---

#### Exercise 8 · Search and debug — `/search` and `/startDebugging`

**What you'll do**: Find code semantically and set up a debug configuration.

**Step 1 — Semantic search**
- In Chat, type:
  ```
  /search where is AP status validated
  ```
  Press **Enter**.
- **What you see**: Copilot searches the workspace and returns file paths and
  line references — likely pointing to `scripts/validate.sh` and
  `docs/wifi-survey-spec.md`. Click a result to jump to that location.

**Step 2 — Generate a debug configuration**
- In Chat, type `/startDebugging` and press **Enter**.
- **What you see**: Copilot creates a `.vscode/launch.json` with a Python
  configuration targeting `src/wifi_utils.py`, then starts a debug session.
  The Run & Debug panel opens with a breakpoint-ready environment.

---

#### Exercise 9 · Create customization files — the `/create-*` commands

**What you'll do**: Use the creator commands to scaffold each customization
primitive directly from chat.

**Step 1 — Generate workspace instructions**
- In a **fresh project** (or a temp folder), type:
  ```
  /init
  ```
  - **What you see**: Copilot scans the project structure (files, folders,
    languages detected) and generates a `.github/copilot-instructions.md`
    with a project summary, folder table, and inferred conventions. In
    *this* project it will note the file already exists.

**Step 2 — Create a prompt file**
- In Chat, type:
  ```
  /create-prompt Generate an RF coverage summary from ap_inventory.json
  ```
  Press **Enter**.
- **What you see**: Copilot creates
  `.github/prompts/generate-rf-coverage-summary.prompt.md` with appropriate
  frontmatter and a body describing the task. You can now invoke it with
  `/generate-rf-coverage-summary`.

**Step 3 — Create an instruction file**
- In Chat, type:
  ```
  /create-instruction for all Python files in src/ — enforce type hints and RF-analysis naming conventions
  ```
  Press **Enter**.
- **What you see**: A new `.instructions.md` file is created with
  `applyTo: "src/**/*.py"` and the rules you described.

**Step 4 — Create an agent**
- In Chat, type:
  ```
  /create-agent rf-analyst — read-only, focuses on WiFi survey data analysis
  ```
  Press **Enter**.
- **What you see**: `.github/agents/rf-analyst.agent.md` is created
  with `tools: [read, search]` and a body describing the RF analysis role.

**Step 5 — Create a hook**
- In Chat, type:
  ```
  /create-hook to block any edit that produces invalid AP inventory JSON
  ```
  Press **Enter**.
- **What you see**: A `.github/hooks/*.json` file is created with a
  `PostToolUse` event and a shell command stub for JSON validation.

**Step 6 — Create a skill**
- In Chat, type:
  ```
  /create-skill rf-coverage-audit — audits ap_inventory.json for schema violations
  ```
  Press **Enter**.
- **What you see**: The folder `.github/skills/rf-coverage-audit/` is created with
  a `SKILL.md` frontmatter and a stub body.

**Step 7 — Open the guided setup**
- In Chat, type `/agent-customization` and press **Enter**.
- **What you see**: An interactive guided workflow opens, asking questions
  about what you want to build. Useful when you're unsure which primitive
  to use.

---

#### Exercise 10 · Browse configuration — the management `/` commands

**What you'll do**: Use the management commands to inspect everything that is
currently configured in this project.

**Step 1** — Type each command below in Chat and press **Enter** after each one.
Observe what each panel shows.

| Command | What to look for |
|---------|-----------------|
| `/agents` | Lists `rf-analyst` and `report-writer` — note their tool sets |
| `/hooks` | Shows `validate-json.json` with its `PostToolUse` event |
| `/instructions` | Lists all three `.instructions.md` files and their `applyTo` globs |
| `/prompts` | Lists `generate-test-cases` and `summarize-aps` with descriptions |
| `/skills` | Lists `wifi-survey-report` — note the `argument-hint` displayed |
| `/tools` | Lists every tool currently available — including MCP tools |
| `/models` | Opens the model picker — note the model currently selected |
| `/plugins` | Lists any chat extensions installed |

**Step 2 — Spot something unexpected?**
- If a file you created in an earlier exercise doesn't appear in the
  corresponding panel, the file likely has a YAML syntax error. Open it and
  check for unquoted colons or tabs.

---

#### Exercise 11 · Control permissions — `/autoApprove`, `/yolo`, and their undos

**What you'll do**: Experience how permission modes change the approval flow.

> **Safety note**: Run these exercises in a sandbox. `/yolo` removes *all*
> confirmation prompts. Revert any unintended changes with `git checkout .`

**Step 1 — Enable auto-approve**
- In Chat, type `/autoApprove` and press **Enter**.
- Now ask Copilot to make a small edit:
  ```
  Add a comment at the top of src/wifi_utils.py saying "# RF analysis module"
  ```
- **What you see**: Copilot makes the edit **without** showing a confirmation
  dialog. No "Apply" button appears.

**Step 2 — Disable auto-approve**
- Type `/disableAutoApprove` and press **Enter**.
- Ask for the same small edit again.
- **What you see**: The confirmation dialog returns — you must click **Apply**
  before the change is made.

**Step 3 — Enable yolo mode**
- Type `/yolo` and press **Enter**.
- Ask Copilot a multi-step task:
  ```
  Add a function get_aps_by_location, generate a test for it, then run the test
  ```
- **What you see**: Copilot completes all three steps back-to-back — edit,
  create test, run terminal — without any confirmation or clarification prompts.

**Step 4 — Return to normal**
- Type `/disableYolo` and press **Enter**.
- Confirmation prompts are restored.
- **Clean up**: Run `git checkout src/wifi_utils.py` in the terminal to revert
  the practice edits.

---

#### Exercise 12 · Troubleshoot unexpected behaviour — `/troubleshoot` and `/fixTestFailure`

**What you'll do**: Use the diagnostic commands to investigate problems.

**Step 1 — /troubleshoot**
- After running several agent tasks (the earlier exercises work well), type:
  ```
  /troubleshoot
  ```
  Press **Enter**.
- **What you see**: Copilot analyses the current session's debug log and
  summarises any anomalies — missed tool calls, instruction files that
  weren't loaded, hooks that fired unexpectedly, etc.

**Step 2 — /fixTestFailure**
- First, introduce a failing test. In the terminal run:
  ```powershell
  python -m pytest --tb=short 2>&1
  ```
  If there are no tests yet, create a deliberately failing one:
  ```powershell
  echo "def test_fail(): assert 1 == 2" > test_temp.py
  python -m pytest test_temp.py --tb=short 2>&1
  ```
- Switch to Chat and type `/fixTestFailure`.
- **What you see**: Copilot reads the pytest output from the terminal, identifies
  the failing assertion, and proposes a fix. Accept or reject as appropriate.
- **Clean up**: Delete `test_temp.py` after the exercise.

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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Ask `@vscode` a settings question

**What you'll do**: Use the `@vscode` participant to get VS Code help relevant
to your WiFi engineering workflow.

**Step 1** — Open Chat (**Ctrl+Alt+I** / **Cmd+Alt+I**).

**Step 2** — Type exactly:
```
@vscode what extensions are useful for network engineers working with JSON data?
```
Press **Enter**.

- **What you see**: Copilot responds with VS Code-specific extension
  recommendations — JSON tools, REST clients, remote SSH extensions —
  with exact extension IDs and how to install them.
- **Why the difference matters**: Without `@vscode`, Copilot might answer about
  general networking tools. The participant scopes the answer to VS Code.

---

#### Exercise 2 · Ask `@terminal` for a shell command

**What you'll do**: Use `@terminal` to get a WiFi diagnostic shell command
without leaving chat.

**Step 1** — In Chat, type:
```
@terminal how do I list available WiFi networks on Windows using netsh?
```
Press **Enter**.

- **What you see**: Copilot returns a PowerShell or `cmd` command
  (e.g., `netsh wlan show networks mode=bssid`), not a Linux command.
  The `@terminal` participant is aware of your OS and active shell.

**Step 2** — Click **Insert into Terminal** (if the button appears) to run
the command without copy-pasting.

---

#### Exercise 3 · Spot the difference

**What you'll do**: Compare `@vscode` vs plain chat to see scoping in action.

**Step 1** — In a fresh chat, type (no `@`):
```
How do I view WiFi signal strength from a terminal?
```

**Step 2** — Then type:
```
@vscode Is there an extension to visualise WiFi heatmaps or signal data?
```

- **What you see**: The `@vscode` version returns VS Code-specific answers —
  extension names, install commands, or setting paths. The plain version may
  give a generic answer about OS-level tools or third-party apps.

---

#### Exercise 4 · Use `@github` for repository information

**What you'll do**: Query GitHub directly from chat to check the status of
your WiFi survey project's pull requests.

> **Prerequisite**: Install the [GitHub Pull Requests](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
> extension and sign in to GitHub. If you are not signed in, VS Code will
> prompt you when you first use `@github`.

**Step 1** — In Chat, type:
```
@github what are my open pull requests?
```
Press **Enter**.

- **What you see**: A list of your open PRs across GitHub repositories —
  titles, repo names, and links — fetched live from the GitHub API.

**Step 2** — Try a search query:
```
@github show recent issues labelled "rf-issue" in this repo
```
- **What you see**: GitHub issues matching the filter, with titles and links.
  You can click through to open them in a browser.

**Step 3 — Discover participant capabilities**
- Type `@github ` (with a trailing space) in the chat input and pause.
- **What you see**: A tooltip or autocomplete list showing the sub-commands
  `@github` supports (e.g., `/search`, `/pr`, `/issue`).

> **If `@github` is not in your list**: Type `@` in chat — if it's missing,
> install the GitHub Pull Requests extension from the Extensions view
> (**Ctrl+Shift+X**) and reload VS Code.

---

#### Exercise 5 · Discover extension-contributed participants

**What you'll do**: See all `@` participants available in your VS Code
installation, including any contributed by extensions.

**Step 1** — In Chat, type `@` and **pause** (do not press Enter).
- **What you see**: An autocomplete dropdown listing every available
  participant — built-ins (`@vscode`, `@terminal`, `@github`) and any added
  by installed extensions.

**Step 2** — Open the Command Palette (**Ctrl+Shift+P**) and run:
```
Chat: List Participants
```
- **What you see**: The full list of registered participants with their
  descriptions — a reliable inventory if the dropdown list is hard to read.

---

## Chapter 3 · `#` Context Mentions & Tools

**Concept**: The `#` symbol lets you explicitly control what context and tools
are available to Copilot. Type `#` in the chat input to see all options.

### Context References

These add specific items from your workspace as context:

| Reference | What it adds | Example |
|-----------|-------------|--------|
| `#file:path/to/file` | A specific file's contents | You want Copilot to explain a whole file without copy-pasting it — use `Explain #file:src/wifi_utils.py` |
| `#folder:path/to/dir` | Files within a directory | You want Copilot to review all source files at once — use `Review #folder:src` |
| `#symbol:functionName` | A specific code symbol (function, class, variable) | You want docs generated for one specific function — use `Document #symbol:find_weak_signals` |
| `#codebase` | Searches your entire codebase for relevant context | You can't find where AP schema validation is implemented — use `Where is AP status validated? #codebase` |
| `#selection` | The current editor text selection | You highlighted a complex block and want an explanation — select it and ask about `#selection` |
| `#changes` | Uncommitted source control changes | You want a commit message based on everything you've changed — use `Summarize my changes #changes` |

### Tool References

These invoke specific tools during the conversation:

| Tool | What it does | Example |
|------|-------------|--------|
| `#fetch` | Retrieves content from a URL | You want Copilot to summarize the latest VS Code release notes without leaving chat — use `Summarize #fetch https://code.visualstudio.com/updates` |
| `#terminalSelection` | Reads the current terminal selection | You selected a stack trace in the terminal and want it explained — use `Explain #terminalSelection` |
| `#terminalLastCommand` | Gets the last terminal command and its output | Your last shell command failed and you want Copilot to diagnose the output — use `What went wrong? #terminalLastCommand` |
| `#problems` | Adds workspace errors/warnings from the Problems panel | The Problems panel shows several errors and you want Copilot to fix them all at once — use `Fix these errors #problems` |

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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Attach a file with `#file`

**What you'll do**: Give Copilot the full context of `wifi_utils.py` using `#file`.

**Step 1** — Open Chat.

**Step 2** — Type exactly (do **not** open the file first):
```
Explain #file:src/wifi_utils.py
```
Press **Enter**.

- **What you see**: Copilot explains *every* function in the file — it has read
  the entire file, not just a selection. You did not need to open the file.
- **Why this is useful**: `#file` attaches the file to the request without
  making it the active editor. Great for referencing related files while
  working in a different file.

---

#### Exercise 2 · Answer a data question with `#file`

**Step 1** — In Chat, type:
```
Which access points have weak signal quality based on #file:data/ap_inventory.json
```
Press **Enter**.

- **What you see**: Copilot reads the JSON and lists any APs with low
  tx_power or `"signal_quality": "critical"`. It identifies them by `ap_id`
  and `location`.

---

#### Exercise 3 · Search the whole project with `#codebase`

**What you'll do**: Find where AP validation rules are defined — without knowing
which file to open.

**Step 1** — In Chat, type:
```
What are the AP inventory validation rules? #codebase
```
Press **Enter**.

- **What you see**: Copilot searches across all project files and cites the
  specific files where validation rules appear — likely
  `docs/wifi-survey-spec.md` and `scripts/validate.sh`.
- **How to verify**: Click the file names in Copilot's response to jump to
  those locations in your editor.

---

#### Exercise 4 · Use `#terminalLastCommand` to diagnose output

**What you'll do**: Run the WiFi analysis script, then ask Copilot to explain
the output.

**Step 1** — Open the integrated terminal: **Ctrl+`** (backtick).

**Step 2** — Run:
```powershell
python src/wifi_utils.py
```

**Step 3** — Switch back to Chat and type:
```
Explain the output #terminalLastCommand
```
- **What you see**: Copilot reads the exact terminal output (it does not ask
  you to paste it) and explains what the AP inventory summary means — counts
  by status, weak signals, or any errors.

---

#### Exercise 5 · Fetch external content with `#fetch`

**Step 1** — In Chat, type:
```
Summarize #fetch https://code.visualstudio.com/updates
```
Press **Enter**.

- **What you see**: Copilot fetches the remote page and returns a bullet-point
  summary of the latest VS Code release notes — without you leaving VS Code.
- **Note**: This requires the MCP `fetch` server configured in
  `.vscode/mcp.json` (see Chapter 10).

---

#### Exercise 6 · Reference a folder with `#folder` and a symbol with `#symbol`

**What you'll do**: Attach an entire directory and a single named symbol as
context.

**Step 1 — `#folder`**
- In Chat, type:
  ```
  Review all files in #folder:src for any missing type hints
  ```
  Press **Enter**.
- **What you see**: Copilot reads every file inside `src/` and reports
  functions that are missing type annotations — without you opening each
  file individually.

**Step 2 — `#symbol`**
- In Chat, type:
  ```
  Document #symbol:find_weak_signals
  ```
  Press **Enter**.
- **What you see**: Copilot generates a docstring for `find_weak_signals` using
  only that function's source, not the whole file. The response is more
  focused than attaching the entire `wifi_utils.py`.

---

#### Exercise 7 · Use `#selection` for in-place context

**What you'll do**: Reference your current editor selection so Copilot does not
need you to copy-paste code into chat.

**Step 1** — Open `src/wifi_utils.py` and highlight any multi-line block
(e.g., the body of `filter_aps_by_band`).

**Step 2** — In Chat, type:
```
What edge cases are not handled in #selection?
```
Press **Enter**.

- **What you see**: Copilot analyses specifically the selected lines and lists
  edge cases — e.g., empty AP list, unknown band string, `None` values
  in the `band` field.
- **Why use this instead of `/explain`**: `#selection` works mid-sentence in
  any prompt; `/explain` is a standalone command. Use `#selection` when you
  want to compose a more specific question.

---

#### Exercise 8 · Summarise uncommitted changes with `#changes`

**What you'll do**: Use `#changes` to generate a commit message from your
current git diff.

**Step 1** — Make a small edit anywhere in the project (e.g., update a
`tx_power` value in `data/ap_inventory.json`) and save the file.
**Do not commit yet.**

**Step 2** — In Chat, type:
```
Write a conventional commit message for #changes
```
Press **Enter**.

- **What you see**: Copilot reads your uncommitted diff from source control and
  produces a commit message following the Conventional Commits format (e.g.,
  `fix(survey): update tx_power for AP-03 in Building North`).
- **How to verify**: Open the Source Control panel (**Ctrl+Shift+G**) — the
  diff Copilot read is the same as what appears there.

---

#### Exercise 9 · Diagnose a terminal selection with `#terminalSelection`

**What you'll do**: Read a specific portion of terminal output without running
a new command.

**Step 1** — Open the integrated terminal (**Ctrl+`**) and run:
```powershell
python src/wifi_utils.py
```

**Step 2** — In the terminal, **click and drag** to select a portion of the
output — for example, just the line that shows the count of offline APs.

**Step 3** — In Chat, type:
```
Explain #terminalSelection
```
Press **Enter**.

- **What you see**: Copilot explains only the lines you selected in the
  terminal — not the full output. Use this when the terminal output is long
  and you only need one section explained.
- **Difference from `#terminalLastCommand`**: `#terminalLastCommand` captures
  the entire last command + output. `#terminalSelection` captures only what
  you highlighted.

---

#### Exercise 10 · Fix all Problems panel errors with `#problems`

**What you'll do**: Feed the entire Problems panel into Copilot in a single
request.

**Step 1 — Introduce some problems**
- Open `src/wifi_utils.py` and make two small syntax errors (e.g., remove
  two closing parentheses on separate lines). Save the file.
- Open the Problems panel: **View → Problems** (or **Ctrl+Shift+M**).
  You should see at least two errors listed.

**Step 2** — In Chat, type:
```
Fix these errors #problems
```
Press **Enter**.

- **What you see**: Copilot reads *all* errors in the Problems panel at once
  and proposes fixes for each one in a single response — not just the error
  in the active editor.

**Step 3 — Apply and verify**
- Accept the proposed changes.
- Check that the Problems panel is now empty (or reduced).

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
2. **Link, don't embed** — Reference `docs/wifi-survey-spec.md` instead of
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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Verify it loads automatically

**What you'll do**: Confirm that workspace instructions load without any explicit
attachment on your part.

**Step 1** — Open a **new** chat session: type `/clear` or click the **+** icon
in the Chat panel.

**Step 2** — Type (do **not** attach any file):
```
What are the coding conventions for this project?
```
Press **Enter**.

- **What you see**: Copilot describes the conventions from
  `.github/copilot-instructions.md` — snake_case Python, 2-space JSON
  indentation, Markdown docs, no secrets. You never attached the file.
- **Why it works**: VS Code injects `copilot-instructions.md` automatically at
  the top of every request's system prompt.

---

#### Exercise 2 · Verify the quick-start command

**Step 1** — In Chat, type:
```
How do I validate the AP inventory data?
```
- **What you see**: Copilot mentions the `bash scripts/validate.sh` and
  `powershell scripts/validate.ps1` commands from the Quick Start section —
  quoting the file path exactly as written in the instructions file.

---

#### Exercise 3 · Inspect with `/debug`

**Step 1** — Type `/debug` in Chat.

**Step 2** — In the debug panel that opens, scroll to the **System prompt**
section.

- **What you look for**: A block of text matching the content of
  `.github/copilot-instructions.md` — the project summary, folder table,
  and conventions.

---

### 📝 Exercise — Add a new convention and verify it

**Goal**: Add a JSON indentation rule and confirm Copilot obeys it when
creating a new AP inventory file.

**Step 1 — Edit the instructions file**

Open `.github/copilot-instructions.md` and add this line under the
**Conventions** section:

```markdown
- **JSON formatting**: All JSON files must use 2-space indentation.
```

Save the file.

**Step 2 — Test it**

In Chat, type:
```
Create a new file data/sample_ap.json with a single example access-point object
```
Press **Enter**.

- **What you see**: The generated `sample_ap.json` uses 2-space indentation —
  Copilot picked up the new rule you just added.

**Step 3 — Verify and clean up**

- Open `data/sample_ap.json` and confirm the indentation.
- Delete the file: in the Explorer, right-click `sample_ap.json` → **Delete**.

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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Trigger `data-files` instructions automatically

**What you'll do**: Ask Copilot to add an AP while `ap_inventory.json` is in
context and watch it enforce the schema rules from `data-files.instructions.md`.

**Step 1** — Open `data/ap_inventory.json` in the editor (**Ctrl+P** →
`ap_inventory.json`).

**Step 2** — Open Chat and type:
```
Add a new access point to ap_inventory.json
```
Press **Enter**.

- **What you see**: Copilot generates a complete AP object with *all* required
  fields (`ap_id`, `ssid`, `bssid`, `channel`, `band`, `tx_power`, `location`,
  `status`, `firmware_version`) and only uses valid enum values like
  `"planned"`, `"deployed"`, `"offline"` for `status`.
- **What's loading this**: Because `ap_inventory.json` is the active file, the
  `applyTo: "data/**/*.json"` glob in `data-files.instructions.md` matches,
  and the instruction file is injected automatically.

---

#### Exercise 2 · Trigger `python-style` instructions automatically

**What you'll do**: Ask Copilot to add a function while `wifi_utils.py` is open
and confirm it follows the Python style guide.

**Step 1** — Open `src/wifi_utils.py` in the editor.

**Step 2** — In Chat, type:
```
Add a function that returns all APs in a specific location zone
```
Press **Enter**.

- **What you see**: Copilot writes a function with:
  - A snake_case name (e.g., `get_aps_by_location`)
  - Type hints on parameters and return value
  - A docstring describing purpose, parameters, and return type
  - An f-string (not `.format()` or `%`) if string formatting is needed
- **Why**: `python-style.instructions.md` with `applyTo: "src/**/*.py"` was
  automatically loaded because the active file lives in `src/`.

---

#### Exercise 3 · Trigger `documentation` instructions on demand

**What you'll do**: Ask for documentation and confirm the on-demand instruction
is loaded (no `applyTo` — purely description-based).

**Step 1** — Close all files (so no specific file is active).

**Step 2** — In Chat, type:
```
Write a user guide for the WiFi site-survey toolkit
```
Press **Enter**.

- **What you see**: Copilot generates Markdown with ATX headings (`#`, `##`),
  tables for structured data, and links to other project docs rather than
  inline-pasting content.
- **How to verify**: Type `/debug` — in the loaded instructions list you should
  see `documentation.instructions.md` was loaded (matched by its description,
  not a glob).

---

#### Exercise 4 · Confirm with `/debug`

**Step 1** — Open `data/ap_inventory.json` in the editor.

**Step 2** — Type `/debug` in Chat.

- **What you look for**: In the debug panel, under **Instructions**, you should
  see `data-files.instructions.md` listed as loaded. Open
  `src/wifi_utils.py` and type `/debug` again — this time you should see
  `python-style.instructions.md` loaded instead.

---

### 📝 Exercise — Create a new instruction file

**Goal**: Create a new instruction that enforces shell scripting standards for
`scripts/*.sh` files.

**Step 1 — Create the file**

Create `.github/instructions/scripts.instructions.md` with this exact content:

```markdown
---
description: "Use when creating or editing shell scripts in the scripts/ directory. Covers safety flags and header conventions."
applyTo: "scripts/**/*.sh"
---
# Shell Script Conventions

- Always begin with `#!/usr/bin/env bash`.
- Always include `set -euo pipefail` on the second line.
- Add a header comment block with: script purpose, inputs, outputs, and exit codes.
- Use lowercase variable names.
- Quote all variable expansions: `"$variable"` not `$variable`.
```

Save the file.

**Step 2 — Test it**

In Chat, with a `.sh` script open (or by asking):
```
Create a new script scripts/cleanup.sh that removes all .pyc files
```
Press **Enter**.

- **What you see**: The generated script starts with `#!/usr/bin/env bash`,
  has `set -euo pipefail` on line 2, and includes a header comment.

**Step 3 — Verify**

Open the generated file and confirm all conventions are followed. Delete it
when done.

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

#### 2. `summarize-aps.prompt.md`

```yaml
---
description: "Summarize AP data from data/ap_inventory.json..."
argument-hint: "Optional: path to ap_inventory.json or filter criteria"
---
```

- **Invocation**: Type `/summarize-aps` in chat.
- **`argument-hint`** shows help text in the chat input field, guiding the
  user on what to type after the command.
- The body defines the report structure (counts by status, offline APs, signal quality).

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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Run the `generate-test-cases` prompt

**What you'll do**: Use the prompt file as a `/` command to generate tests for
a real WiFi analysis function.

**Step 1** — Open `src/wifi_utils.py` in the editor.

**Step 2** — Scroll to `filter_aps_by_band` and select the entire function
(click the function name → **Ctrl+Shift+K** or click-drag).

**Step 3** — Open Chat and type:
```
/generate-test-cases
```
Press **Enter**.

- **What you see**: Copilot generates a pytest test file containing:
  - A happy-path test (valid band, APs returned)
  - An empty-result test (band with no matching APs)
  - An invalid-input test (unrecognised band string like `"7 GHz"`)
  - Descriptive test names (e.g., `test_filter_aps_by_band_returns_matching_aps`)
- **Why it knows to use pytest**: The prompt body in
  `generate-test-cases.prompt.md` specifies pytest conventions.

---

#### Exercise 2 · Run the `summarize-aps` prompt

**Step 1** — In Chat, type:
```
/summarize-aps
```
Press **Enter**.

- **What you see**: A formatted Markdown report with totals by status
  (planned, deployed, offline), weak-signal APs, and any blockers.

**Step 2 — Try the argument hint**

Type:
```
/summarize-aps only critical signal quality
```
Press **Enter**.

- **What you see**: A filtered report showing only APs where `signal_quality`
  is `"critical"`.
- **Why the hint appeared**: The `argument-hint` in the prompt frontmatter
  displayed help text below the chat input while you were typing.

---

#### Exercise 3 · Inspect the prompt frontmatter

**Step 1** — Open `.github/prompts/generate-test-cases.prompt.md`.

**Step 2** — Read the frontmatter and the body. Notice:
- `agent: "agent"` tells VS Code to run in full agent mode.
- The body instructs Copilot to generate edge cases, not just happy paths.

**Step 3** — Open `/prompts` in Chat to see both prompts listed.

---

### 📝 Exercise — Create a `code-review` prompt

**Goal**: Build a reusable prompt that reviews selected code for bugs and style.

**Step 1 — Create the file**

Create `.github/prompts/code-review.prompt.md` with this content:

```markdown
---
description: "Review selected code for bugs, style issues, and missing tests. Reports findings as a structured Markdown list."
argument-hint: "Optional: focus area, e.g. 'only security issues' or 'only style'"
agent: "ask"
---

Review the selected code for the following:

1. **Bugs**: Logic errors, off-by-one errors, unhandled edge cases.
2. **Style**: Does it follow the project's Python conventions (snake_case, type
   hints, docstrings)?
3. **Tests**: Are there obvious cases that lack test coverage?

Format the output as three sections with bullet-point findings.
If no issues are found in a category, write "No issues found."

Selected code: {{selection}}
```

Save the file.

**Step 2 — Test it**

1. Open `src/wifi_utils.py` and select the `find_weak_signals` function.
2. In Chat, type `/code-review` and press **Enter**.
3. **What you see**: A three-section Markdown report — Bugs, Style, Tests —
   each with bullet points or "No issues found."

**Step 3 — Try with an argument**

Type:
```
/code-review only security issues
```
- Copilot narrows its review to security-relevant findings only.

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
1. Was the edited file `ap_inventory.json`?
2. If yes, run `scripts/validate.sh` to check the data structure.
3. If validation fails → exit 2 (blocking error) → Copilot sees the failure
   and can self-correct.
4. If the edit wasn't `ap_inventory.json` → exit 0 (do nothing).

### The hook script flow

```
stdin (JSON payload)
  │
  ├─ toolName != "editFiles" or "createFile"?  →  exit 0 (skip)
  │
  ├─ no "ap_inventory.json" in edited files?  →  exit 0 (skip)
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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Force a hook failure

**What you'll do**: Ask Copilot to write an *invalid* AP entry to
`ap_inventory.json` and watch the `PostToolUse` hook catch it.

**Step 1** — Open Chat and type:
```
Add a new access point to ap_inventory.json. Include the ap_id and ssid fields
only — skip all other fields.
```
Press **Enter**.

- **What happens**: Copilot writes the incomplete AP object to
  `ap_inventory.json`. The `PostToolUse` hook fires immediately after the file
  is saved. `scripts/validate.ps1` (Windows) or `scripts/validate.sh`
  (macOS/Linux) runs. Validation fails and exits with code 2.
- **What you see in chat**: Copilot receives the exit-2 error and reports it.
  It then attempts to self-correct by adding the missing required fields
  (bssid, channel, band, tx_power, location, status, firmware_version).
- **Key insight**: You did not manually catch this error — the hook
  *automatically* enforced the AP inventory schema.

---

#### Exercise 2 · Confirm a valid AP passes the hook

**Step 1** — In Chat, type:
```
Add a valid access point AP-09 to ap_inventory.json with all required fields
populated.
```
Press **Enter**.

- **What happens**: Copilot writes a complete AP entry. The hook fires,
  validation passes (exit 0), and no error is shown.
- **Verify**: Open `data/ap_inventory.json` and confirm AP-09 was added with
  all required fields.

---

#### Exercise 3 · Watch the hook in agent logs

**Step 1** — Type `/debug` in Chat.

**Step 2** — Look for **PostToolUse** entries in the debug output. You should
see the hook command and its stdout/exit code logged for the previous edits.

---

### 📝 Exercise — Create a `no-secrets` pre-edit hook

**Goal**: Block any file edit in a `config/` folder to prevent accidental
credential commits — important when your WiFi controller configs may contain
SNMP community strings or admin passwords.

**Step 1 — Create the hook config**

Create `.github/hooks/no-secrets.json` with this content:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "bash ./scripts/hooks/no-secrets.sh",
        "windows": "powershell -ExecutionPolicy Bypass -File ./scripts/hooks/no-secrets.ps1",
        "timeout": 10
      }
    ]
  }
}
```

**Step 2 — Create the hook script**

Create `scripts/hooks/no-secrets.ps1` with this content:

```powershell
# no-secrets.ps1 — Blocks edits to files in the config/ folder.
# Exit 2 to block, exit 0 to allow.

$input_json = $input | ConvertFrom-Json

$tool = $input_json.toolName
if ($tool -ne "editFiles" -and $tool -ne "createFile") {
    exit 0
}

$paths = @()
if ($input_json.toolInput.files) {
    $paths = $input_json.toolInput.files | ForEach-Object { $_.path }
} elseif ($input_json.toolInput.path) {
    $paths = @($input_json.toolInput.path)
}

foreach ($p in $paths) {
    if ($p -match "config[/\\]") {
        Write-Host "BLOCKED: Edits to config/ are not allowed. Move secrets to environment variables."
        exit 2
    }
}

exit 0
```

**Step 3 — Test it**

In Chat, type:
```
Create a file config/controller.json with a WLC connection string
```
- **What you see**: The hook intercepts the `createFile` call, exits 2, and
  Copilot reports that the operation was blocked.

**Step 4 — Verify it allows other edits**

Ask Copilot to edit `src/wifi_utils.py` — the hook should allow it (exit 0).

---

## Chapter 8: Custom Agents

**Files**: `.github/agents/*.agent.md`

**Concept**: Custom agents are specialized AI personas with defined tools,
instructions, and behaviors. Think of each one as a team member with a specific
role and limited access.

### The two example agents

#### 1. `rf-analyst.agent.md` — Read-only analyst

```yaml
---
name: RF Analyst
description: "Use when analyzing WiFi survey data, finding weak signals..."
tools: [read, search]
---
```

- **User-invocable**: Yes (default) — appears in the agent picker dropdown.
- **Tools**: Only `read` and `search` — cannot edit files or run commands.
- **Role**: Analyzes AP inventory data and answers questions about coverage.

#### 2. `report-writer.agent.md` — Subagent-only writer

```yaml
---
name: Report Writer
description: "Use when generating or updating WiFi site-survey documentation..."
tools: [read, search, edit]
user-invocable: false
---
```

- **`user-invocable: false`**: Hidden from the agent picker. Only accessible
  when another agent delegates to it as a subagent.
- **Tools**: Can `read`, `search`, and `edit` — but only Markdown files
  (enforced by instructions in the body).
- **Role**: Generates site-survey documentation when delegated to by a parent
  agent.

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
description: "Use when analyzing WiFi survey data, finding weak signals..."

# Bad — vague, won't be discovered
description: "A helpful analysis tool"
```

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Use the RF Analyst (read-only)

**What you'll do**: Switch to the RF Analyst agent and confirm it can analyse
AP data but cannot edit files.

**Step 1** — In the Chat panel, click the **agent picker** dropdown at the
top of the input area (it shows the current agent name, e.g., "Agent" or a
model name).

**Step 2** — Select **RF Analyst** from the list.

**Step 3** — Type:
```
How many access points have critical signal quality?
```
Press **Enter**.

- **What you see**: The RF Analyst reads `data/ap_inventory.json`, counts APs
  with `"signal_quality": "critical"`, and returns a Markdown table or
  bulleted list. It does not offer to edit any files.

---

#### Exercise 2 · Confirm tool restrictions

**Step 1** — Still using **RF Analyst**, type:
```
Fix the weak-signal APs by increasing their tx_power to 20 dBm.
```
Press **Enter**.

- **What you see**: The agent explains it cannot edit files — it only has
  `read` and `search` tools. It may describe *what* would need to change
  without making the change.
- **Why**: The `tools: [read, search]` line in the agent's frontmatter
  prevents `editFiles` from being available.

---

#### Exercise 3 · Trigger the Report Writer via delegation

**Step 1** — Click the agent picker and switch back to the default **Agent**.

**Step 2** — Type:
```
Write a site-survey summary report for this project in docs/site-survey-report.md
```
Press **Enter**.

- **What you see**: The main agent may delegate the writing task to the Report
  Writer subagent. Watch the agent logs (type `/debug`) for a
  `SubagentStart`/`SubagentStop` pair with "Report Writer" as the agent name.
- **Why**: The Report Writer's `description` contains trigger phrases like
  *"generating or updating WiFi site-survey documentation"*, which the main
  agent matches when it needs to delegate a documentation task.

---

### 📝 Exercise — Create a `code-reviewer` agent

**Goal**: Build a read-only agent that reviews WiFi analysis Python code for
bugs, style, and missing tests.

**Step 1 — Create the agent file**

Create `.github/agents/code-reviewer.agent.md` with this content:

```markdown
---
name: Code Reviewer
description: "Use when reviewing Python code for bugs, style violations, and missing test coverage. Read-only — does not modify files."
tools: [read, search]
user-invocable: true
---

You are a senior Python code reviewer. When given a file or function to review:

1. Check for logic errors, off-by-one bugs, and unhandled edge cases.
2. Verify the code follows the project's Python style guide:
   - snake_case function and variable names
   - Type hints on all function parameters and return values
   - Docstrings on all public functions
3. Identify functions that lack test coverage.

Format your response as a Markdown report with three sections:
**Bugs**, **Style Issues**, and **Missing Tests**.
Write "None found" in any section with no issues.

Do NOT suggest edits or attempt to modify any files.
```

Save the file.

**Step 2 — Test it**

1. Click the agent picker dropdown.
2. Select **Code Reviewer** (it should now appear because
   `user-invocable: true`).
3. Type:
```
Review src/wifi_utils.py
```
Press **Enter**.

- **What you see**: A three-section Markdown report — Bugs, Style Issues,
  Missing Tests — without any file edits being made.

**Step 3 — Verify tool restriction**

Ask the Code Reviewer:
```
Fix the style issues you found.
```
- **What you see**: It explains it cannot edit files and offers to describe
  the changes needed instead.

---

## Chapter 9: Skills

**Files**: `.github/skills/wifi-survey-report/`

**Concept**: A skill is a folder containing a `SKILL.md` file plus supporting
assets (scripts, templates, reference docs). Skills represent multi-step
workflows and appear as `/` commands in chat — just like prompts, but with
bundled resources.

### Skill folder structure

```
.github/skills/wifi-survey-report/
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
name: wifi-survey-report           # Must match the folder name!
description: "Generate a Markdown site-survey status report from data/ap_inventory.json..."
argument-hint: "Optional: report scope like 'critical signal only'"
---
```

Critical: The `name` field **must exactly match** the folder name
(`wifi-survey-report`). A mismatch causes a silent failure.

### Slash command behavior

| Configuration | Slash command? | Auto-loaded by agents? |
|---------------|---------------|----------------------|
| Default (both omitted) | ✅ Yes | ✅ Yes |
| `user-invocable: false` | ❌ No | ✅ Yes |
| `disable-model-invocation: true` | ✅ Yes | ❌ No |
| Both set | ❌ No | ❌ No |

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Run the skill

**What you'll do**: Invoke the `wifi-survey-report` skill as a `/` command.

**Step 1** — Open Chat.

**Step 2** — Type:
```
/wifi-survey-report
```
Press **Enter**.

- **What you see**: Copilot loads the skill (see the progress indicator), reads
  `data/ap_inventory.json`, applies the report template from
  `.github/skills/wifi-survey-report/assets/report-template.md`, and returns a
  formatted Markdown site-survey report with AP counts by status, weak-signal
  APs, and a summary table.

---

#### Exercise 2 · Pass an argument to the skill

**Step 1** — Type:
```
/wifi-survey-report offline APs only
```
Press **Enter**.

- **What you see**: A filtered report showing only APs with
  `"status": "offline"`. The argument was passed as the user's request context
  alongside the skill instructions.

---

#### Exercise 3 · Inspect progressive loading

**Step 1** — Type `/debug` after running the skill.

- **What you look for**: In the debug output, you should see the skill loaded
  in stages:
  1. **Discovery**: `name` and `description` from the frontmatter (~100 tokens).
  2. **Instructions**: The full `SKILL.md` body.
  3. **Resources**: The `report-format.md` and `report-template.md` files
     (only loaded when the skill ran).

---

### 📝 Exercise — Create a `rf-coverage-audit` skill

**Goal**: Build a skill that checks `ap_inventory.json` against the survey spec
rules and reports issues.

**Step 1 — Create the folder structure**

Create these files:

**`.github/skills/rf-coverage-audit/SKILL.md`**:

```markdown
---
name: rf-coverage-audit
description: "Check data/ap_inventory.json for schema violations, missing fields, invalid values, and duplicate AP IDs. Use when auditing WiFi survey data quality."
argument-hint: "Optional: specific check to run, e.g. 'check for channel conflicts only'"
---

You are an RF coverage auditor for this WiFi site-survey project.

## Your job

1. Read `data/ap_inventory.json`.
2. Check every AP against the rules in `references/quality-rules.md`.
3. Report all violations in a Markdown table with columns:
   **AP ID**, **Field**, **Issue**, **Expected Value**.
4. If no issues are found, write: "✅ All access points pass quality checks."

## Steps

1. Use the `read` tool to load `data/ap_inventory.json`.
2. Use the `read` tool to load `.github/skills/rf-coverage-audit/references/quality-rules.md`.
3. Validate each AP against every rule.
4. Produce the report.
```

**`.github/skills/rf-coverage-audit/references/quality-rules.md`**:

```markdown
# Data Quality Rules

## Required fields
Every access point must have: `ap_id`, `ssid`, `bssid`, `channel`, `band`,
`tx_power`, `location`, `status`, `firmware_version`.

## Enum constraints
- `status` must be one of: `planned`, `deployed`, `offline`, `decommissioned`
- `band` must be one of: `2.4 GHz`, `5 GHz`, `6 GHz`
- `signal_quality` must be one of: `good`, `marginal`, `critical`

## Format constraints
- `ap_id` must match the pattern `AP-NN` (e.g., `AP-01`)
- `bssid` must be a valid MAC address (`XX:XX:XX:XX:XX:XX`)
- `channel` must be a positive integer
- `tx_power` must be a number (in dBm)

## Uniqueness
- `ap_id` must be unique across all access points
- `bssid` must be unique across all access points
```

**Step 2 — Test the skill**

In Chat, type:
```
/rf-coverage-audit
```
Press **Enter**.

- **What you see**: Copilot reads both files and validates every AP. Any
  APs with missing fields, invalid enum values, or duplicate IDs appear in
  a violations table.

**Step 3 — Introduce a violation to test it**

Temporarily edit `data/ap_inventory.json` to set one AP's `status` to
`"invalid"`. Run `/rf-coverage-audit` again — it should report the violation.

Revert the edit when done.

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

### 🧪 Try It — Interactive Exercises

#### Exercise 1 · Fetch release notes from the web

**What you'll do**: Use the MCP `fetch` server to retrieve a live web page
inside chat.

**Step 1** — Open Chat.

**Step 2** — Type:
```
Summarize the latest firmware release notes for Aruba AP-515 #fetch https://www.arubanetworks.com/techdocs/AOS-CX/latest/release-notes
```
Press **Enter**.

- **What you see**: Copilot fetches the vendor documentation page via the MCP
  `fetch` server and returns a bullet-point summary of the latest firmware
  changes — without you opening a browser.
- **How it works**: `#fetch` tells Copilot to invoke the `fetch` tool from
  `.vscode/mcp.json`. The MCP client sends the HTTP request and returns the
  page content as tool output.

---

#### Exercise 2 · Verify the fetch tool is available

**Step 1** — Type `/tools` in Chat.

- **What you see**: A panel listing all available tools. `fetch` should appear
  in the list, contributed by the `fetch` MCP server in `.vscode/mcp.json`.

**Step 2** — If `fetch` is **not** listed:
1. Open `.vscode/mcp.json` and verify the JSON is valid.
2. Run the VS Code command **MCP: List Servers** from the Command Palette to
   see if the server is registerd.
3. Restart VS Code if the server was recently added.

---

#### Exercise 3 · Trace a fetch call in `/debug`

**Step 1** — Run the fetch command from Exercise 1 again.

**Step 2** — Type `/debug`.

- **What you look for**: In the agent logs, find a tool invocation for `fetch`
  with the URL as the input. This confirms the MCP server handled the request,
  not a built-in Copilot capability.

---

### 📝 Exercise — Add an MCP server for your team's tools

**Goal**: Configure a second MCP server in `.vscode/mcp.json`.

**Step 1 — Choose a server**

Pick one of these well-known MCP servers available via `npx`:

| Server | Purpose | Package |
|--------|---------|---------|
| Filesystem | Read/write local files via MCP | `@modelcontextprotocol/server-filesystem` |
| SQLite | Query a local SQLite database | `@modelcontextprotocol/server-sqlite` |
| GitHub | GitHub API (repos, issues, PRs) | `@modelcontextprotocol/server-github` |

**Step 2 — Edit `.vscode/mcp.json`**

Open `.vscode/mcp.json` and add a second server entry. For example, to add
the filesystem server:

```json
{
  "servers": {
    "fetch": {
      "type": "copilot",
      "description": "Built-in web fetch tool — retrieves content from URLs."
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${workspaceFolder}"
      ]
    }
  }
}
```

Save the file.

**Step 3 — Verify the new server**

1. Open the Command Palette (**Ctrl+Shift+P**).
2. Run **MCP: List Servers** — `filesystem` should appear.
3. Type `/tools` in Chat — the filesystem tools (e.g., `read_file`,
   `list_directory`) should appear alongside `fetch`.

**Step 4 — Test it in an agent**

Type in Chat:
```
Using the filesystem MCP server, list all JSON files in the data/ folder and summarise the AP inventory
```
- **What you see**: The agent invokes the MCP filesystem server's
  `list_directory` tool, finds `ap_inventory.json`, and summarises the
  access-point data.

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
| Skill not appearing as `/` command | Folder name doesn't match `name` in SKILL.md | Ensure exact match: folder `wifi-survey-report` → `name: wifi-survey-report` |
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

| Command | Description | Example |
|---------|-------------|--------|
| `/explain` | Explain selected code — purpose, logic, edge cases | You inherited `find_weak_signals` and don't know what it does — select it and use `/explain` |
| `/fix` | Propose fixes for errors guided by Problems panel or stack traces | A red underline appears under your code and you're unsure why — use `/fix` to let Copilot read the error and suggest a fix |
| `/tests` | Generate tests using your project's test framework conventions | You just wrote `filter_aps_by_band` but have no tests yet — select it and use `/tests` |
| `/doc` | Generate documentation comments (inline chat) | You wrote a utility function but left no docstring — select it and use `/doc` in inline chat |
| `/setupTests` | Scaffold a test framework — config, deps, example tests | Your project has no test framework and you don't want to configure it manually — use `/setupTests` |
| `/fixTestFailure` | Analyze failing tests and suggest fixes | A pytest run just failed with an unclear error — use `/fixTestFailure` to let Copilot diagnose it |

### Scaffolding

| Command | Description | Example |
|---------|-------------|--------|
| `/new` | Create a new file or project from natural language description | You need a new utility script but don't want to write boilerplate — use `/new Python script that reads a CSV` |
| `/newNotebook` | Create a new Jupyter notebook from a description | You want to explore `ap_inventory.json` interactively — use `/newNotebook analyze ap_inventory.json` |

### Session Management

| Command | Description | Example |
|---------|-------------|--------|
| `/clear` | Archive current session and start fresh | You finished one task and want a clean slate for the next — use `/clear` |
| `/fork` | Copy conversation into a new independent session | You want to try a different approach without losing your current conversation — use `/fork` |
| `/compact` | Summarize history to free context window space | Your chat history grew long and Copilot is losing early context — use `/compact` |
| `/rename` | Rename the current chat session | You want to find this session later by topic — use `/rename Fix task validation bug` |

### Planning & Search

| Command | Description | Example |
|---------|-------------|--------|
| `/plan` | Create a detailed step-by-step implementation plan | Before coding a new feature, you want to see all steps outlined first — use `/plan Add search by location to wifi_utils.py` |
| `/search` | Semantic search across workspace | You can't remember where band validation is implemented — use `/search where is AP band validated` |
| `/startDebugging` | Generate `launch.json` and start a debug session | You want to debug `wifi_utils.py` but have no launch config — use `/startDebugging` |

### Customization Creators

| Command | What it creates | Example |
|---------|----------------|--------|
| `/init` | `copilot-instructions.md` from project structure | You opened a new project and want Copilot to generate workspace instructions automatically — use `/init` |
| `/create-prompt` | `.prompt.md` file | You keep typing the same changelog task in chat — turn it into a reusable command with `/create-prompt Generate a changelog` |
| `/create-instruction` | `.instructions.md` file | You want all TypeScript files to follow specific style rules — use `/create-instruction for TypeScript files` |
| `/create-skill` | Skill folder with `SKILL.md` | You want to package a multi-step RF coverage audit workflow with templates — use `/create-skill rf-coverage-audit` |
| `/create-agent` | `.agent.md` file | You need a read-only agent that can only review code, not edit it — use `/create-agent security-reviewer` |
| `/create-hook` | Hook `.json` configuration | You want to automatically block any edit that produces invalid JSON — use `/create-hook to block invalid JSON` |
| `/agent-customization` | Opens the agent customization workflow | You're new to agent config and want a guided setup walkthrough — use `/agent-customization` |

### Management UIs

| Command | Opens | Example |
|---------|-------|--------|
| `/agents` | Custom agents list | You want to check which custom agents exist in this project — use `/agents` |
| `/hooks` | Hook configurations | You want to verify that `validate-json.json` is configured correctly — use `/hooks` |
| `/instructions` | Instruction files | You want to see which instruction files are currently active — use `/instructions` |
| `/prompts` | Prompt files | You forgot the name of the test-generation prompt — use `/prompts` to find it |
| `/skills` | Agent skills | You want to review the `wifi-survey-report` skill before invoking it — use `/skills` |
| `/tools` | Tool availability and permissions | Your agent isn't finding files and you suspect a tool is disabled — use `/tools` |
| `/models` | AI model picker | You want a faster model for a quick question — use `/models` to switch |
| `/plugins` | Chat plugins and extensions | You want to see which chat extensions are installed and active — use `/plugins` |

### Permission Control

| Command | Description | Example |
|---------|-------------|--------|
| `/autoApprove` | Auto-approve all tool calls (skip confirmations) | You're running a large automated refactor and don't want a confirmation dialog on every file edit — use `/autoApprove` |
| `/disableAutoApprove` | Re-enable tool call confirmations | You've finished the bulk refactor and want to review each tool call individually again — use `/disableAutoApprove` |
| `/yolo` | Maximum autonomy — auto-approve + auto-respond | You're in a throwaway sandbox and want Copilot to work end-to-end without any prompts — use `/yolo` |
| `/disableYolo` | Return to normal approval mode | You're done experimenting and want to restore normal confirmation and approval — use `/disableYolo` |

### Debug & Troubleshoot

| Command | Description | Example |
|---------|-------------|--------|
| `/debug` | Open Chat Debug view — inspect prompts, context, and tools | Your instruction file doesn't seem to be loading — use `/debug` to inspect exactly what Copilot received |
| `/troubleshoot` | AI analysis of agent debug logs for current session | An agent produced unexpected output and you can't tell why — use `/troubleshoot` to have Copilot analyze its own logs |

### Custom Commands

| Command | Description | Example |
|---------|-------------|--------|
| `/<prompt-name>` | Run a prompt file (e.g., `/generate-test-cases`) | You want to generate tests without typing the full instructions each time — use `/generate-test-cases` after selecting a function |
| `/<skill-name>` | Run a skill (e.g., `/wifi-survey-report`) | You need a formatted site-survey summary from `ap_inventory.json` — use `/wifi-survey-report critical signal only` |

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

| Reference | What it adds to context | Example |
|-----------|------------------------|--------|
| `#file:path` | A specific file | You want Copilot to explain a whole file without copy-pasting it — use `Explain #file:src/wifi_utils.py` |
| `#folder:path` | All files in a directory | You want Copilot to review all source files at once — use `Review #folder:src` |
| `#symbol:name` | A function, class, or variable | You want docs generated for one specific function — use `Document #symbol:find_weak_signals` |
| `#codebase` | Semantic search across the entire workspace | You can't find where band validation is implemented — use `Where is band validated? #codebase` |
| `#selection` | Current editor text selection | You highlighted a complex block and want an explanation — select it and ask about `#selection` |
| `#changes` | Uncommitted source control changes | You want a commit message based on everything you've changed — use `Summarize my changes #changes` |

### `#` Tool References

| Tool | What it does | Example |
|------|-------------|--------|
| `#fetch` | Retrieve content from a URL | You want Copilot to summarize the latest VS Code release notes without leaving chat — use `Summarize #fetch https://code.visualstudio.com/updates` |
| `#terminalSelection` | Read the current terminal selection | You selected a stack trace in the terminal and want it explained — use `Explain #terminalSelection` |
| `#terminalLastCommand` | Get the last terminal command and output | Your last shell command failed and you want Copilot to diagnose the output — use `What went wrong? #terminalLastCommand` |
| `#problems` | Workspace errors and warnings | The Problems panel shows several errors and you want Copilot to fix them all at once — use `Fix these errors #problems` |

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
│   │   └── summarize-aps.prompt.md          ← Ch. 6: Prompt (argument-hint)
│   ├── hooks/
│   │   └── validate-json.json               ← Ch. 7: PostToolUse hook
│   ├── agents/
│   │   ├── rf-analyst.agent.md              ← Ch. 8: Read-only agent
│   │   └── report-writer.agent.md           ← Ch. 8: Subagent-only
│   └── skills/
│       └── wifi-survey-report/              ← Ch. 9: Skill
│           ├── SKILL.md
│           ├── references/report-format.md
│           └── assets/report-template.md
├── .vscode/
│   └── mcp.json                             ← Ch. 10: MCP config
├── data/
│   └── ap_inventory.json                   ← Sample AP data
├── docs/
│   └── wifi-survey-spec.md                  ← Domain specification
├── scripts/
│   ├── validate.sh                          ← Data validation (macOS/Linux)
│   ├── validate.ps1                         ← Data validation (Windows)
│   └── hooks/
│       ├── enforce-todo-format.sh           ← Hook script (macOS/Linux)
│       └── enforce-todo-format.ps1          ← Hook script (Windows)
├── src/
│   └── wifi_utils.py                        ← Python utilities
├── .gitignore
└── README.md                                ← This file
```
