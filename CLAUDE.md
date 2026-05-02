# pyx12

HIPAA X12 EDI document validator and converter. Parses ANSI X12N data files and validates against HIPAA Implementation Guidelines. Generates 997 (4010) / 999 (5010) acknowledgements.

## Project
- Python 3.11+, BSD
- Active branch: `dev/py3-modernize` — modernizing Python 2→3 patterns
- Tests live in `pyx12/test/`, use `unittest.TestCase` style
- Run tests: `.venv/Scripts/python.exe -m pytest pyx12/test/`
- Line length: 100 (ruff format), imports sorted via `ruff check --select I --fix`

## Tech stack
- **Language:** Python 3.11+ (CI matrix: 3.11, 3.12, 3.13, 3.14)
- **Runtime deps:** `defusedxml>=0.7` (only)
- **Build backend:** setuptools (>=61) via `pyproject.toml`; no `setup.py`
- **Package manager:** `uv` — install Python packages with `uv pip install ...`, not pip
- **Local environment:** `.venv/` at project root. Always invoke tools via `.venv/Scripts/python.exe -m <tool>` — never `source .venv/Scripts/activate`, since shell state does not persist across Bash tool calls
- **Test runner:** pytest (+ pytest-cov for coverage); tests written in `unittest.TestCase` style
- **Format / lint:** ruff (line length 100); `ruff format` + `ruff check --select I` for imports
- **CI:** GitHub Actions — `.github/workflows/main.yml` runs the matrix; `release.yml` and `publish-to-test-pypi.yml` handle PyPI
- **XML parsing:** `defusedxml.ElementTree` (never `xml.etree.ElementTree` directly — DTD/entity DoS protection)
- **Package data:** XML maps + DTDs/XSDs in `pyx12/map/` are loaded via `importlib.resources`

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
See the [/test](.claude/commands/test.md) skill for invocation, reporting, and authoring conventions.

## Preferences
- Save preferences to this CLAUDE.md file so they persist across sessions