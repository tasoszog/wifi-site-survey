---
description: "Use when creating or editing Python source files. Covers naming, style, type hints, and docstrings."
applyTo: "src/**/*.py"
---
# Python Style Guidelines

- Use `snake_case` for functions, variables, and file names.
- Add a docstring to every public function and class.
- Prefer type hints on function signatures (`def foo(x: int) -> str:`).
- Keep functions short — aim for under 25 lines.
- Use `pathlib.Path` for file paths instead of string concatenation.
- Import standard library modules first, then third-party, then local.
- Use f-strings for formatting, not `%` or `.format()`.
