---
description: "Generate a Conventional Commits message from your current uncommitted changes."
argument-hint: "Optional: scope override or extra context"
---
Read the current uncommitted diff from #changes.

Then produce a single **Conventional Commits** message following this format:

<type>(<scope>): <short summary>

<optional body — 1-3 sentences explaining WHY, not what>

Rules:
- **type**: one of `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`
- **scope**: the folder or module most affected — omit if cross-cutting
- **summary**: imperative mood, lowercase, no period, ≤ 72 characters
- **body**: only if the reason isn't obvious from the summary

Output only the commit message — no additional explanation.