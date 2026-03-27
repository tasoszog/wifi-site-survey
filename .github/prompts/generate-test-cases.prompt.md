---
description: "Generate test cases for the selected code or function. Produces pytest-style tests with edge cases."
agent: "agent"
---
Generate comprehensive test cases for the provided code:

- Use **pytest** conventions (`test_` prefix, assert statements).
- Include:
  - Happy-path tests for normal inputs
  - Edge cases (empty input, boundary values)
  - Error cases (invalid input that should raise exceptions)
- Use descriptive test names that explain the scenario: `test_<function>_<scenario>`.
- Add brief inline comments explaining non-obvious test logic.
- If the code reads files, mock file I/O rather than requiring real files.
