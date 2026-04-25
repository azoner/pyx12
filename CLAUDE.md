# pyx12

HIPAA X12 EDI document validator and converter. Parses ANSI X12N data files and validates against HIPAA Implementation Guidelines. Generates 997 (4010) / 999 (5010) acknowledgements.

## Project
- Python 3.11+, BSD
- Active branch: `dev/py3-modernize` — modernizing Python 2→3 patterns
- Tests live in `pyx12/test/`, use `unittest.TestCase` style
- Run tests: `pytest pyx12/test/`
- Line length: 100 (black), imports sorted with isort (black profile)

## Coding style
- No comments unless the WHY is non-obvious (hidden constraint, subtle invariant, workaround)
- No unnecessary abstractions — match scope to the task; three similar lines beats a premature helper
- No error handling for scenarios that can't happen; validate only at system boundaries
- No backwards-compatibility shims for removed code
- No docstrings beyond a single short line when truly needed
- Prefer functional programming patterns over object oriented patterns

## Response style
- Trailing summaries and recaps of what was done are welcome
- Some emojis
- Reference code locations as `file:line` (or markdown links in VSCode)
- Short updates at key moments; silent is not acceptable

## Testing
- Tests use `unittest.TestCase` with descriptive class + method names
- No mocking internal logic — test real behavior
- Run the full suite before reporting a task complete

## Preferences
- Save preferences to this CLAUDE.md file so they persist across sessions