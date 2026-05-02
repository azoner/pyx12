---
name: tech-debt
description: Scan pyx12 for tech debt and produce a prioritized report
argument-hint: "[path | category]"
context: fork
agent: Explore
---

# Scan pyx12 for tech debt

Produce a prioritized report of tech debt in the codebase. Accepts an optional argument to scope the scan: a file path, a directory, or a category name (`type-ignores`, `todos`, `legacy-typing`, `bare-except`, `any`). No argument runs every category over `pyx12/`.

The goal is a short, actionable report — not a backlog dump. Lead with the items most worth fixing this week.

## Steps

### 1. Determine scope

- No argument → scan all of `pyx12/` for every category
- Argument is a path under `pyx12/` → restrict every category to that path
- Argument is a category name → run only that category over `pyx12/`

### 2. Run the scans

Run these in parallel (independent Grep / Bash calls) and collect counts + locations.

**a. `# type: ignore` comments** — explicit type holes. Group by error code (`arg-type`, `union-attr`, `assignment`, `unused-ignore`, etc.). The project enforces mypy strict, so each ignore is a deliberate concession worth re-examining.

```
Grep: pattern = "type:\s*ignore", glob = "*.py", output_mode = "content", -n = true
```

**b. TODO / FIXME / HACK / XXX** — author-flagged debt.

```
Grep: pattern = "(?i)#\s*(TODO|FIXME|HACK|XXX)\b", glob = "*.py", output_mode = "content", -n = true
```

**c. Legacy typing imports** — `from typing import List, Dict, Tuple, Optional, Union, Set, FrozenSet, Type`. Project is Python 3.11+, so prefer built-in generics (`list[X]`, `dict[K, V]`, `X | None`).

```
Grep: pattern = "^from typing import .*\b(List|Dict|Tuple|Optional|Union|Set|FrozenSet|Type)\b", glob = "*.py", output_mode = "content", -n = true
```

**d. Bare `except:`** — silently swallows everything.

```
Grep: pattern = "^\s*except\s*:", glob = "*.py", output_mode = "content", -n = true
```

**e. Explicit `Any` annotations** in production code. Tests, examples, scripts, and `pyx12/map/*` are excluded from mypy's strict-untyped-def rules — only flag `Any` outside those.

```
Grep: pattern = ":\s*Any\b|->\s*Any\b|list\[Any\]|dict\[[^]]+,\s*Any\]", glob = "*.py", output_mode = "files_with_matches"
```
Then filter out: `pyx12/test/`, `pyx12/tests/`, `pyx12/examples/`, `pyx12/scripts/`, `pyx12/map/`.

**f. Long modules** — files over 1000 lines are concentrate-of-debt candidates.

```
Bash: .venv/Scripts/python -c "import pathlib; [print(f'{len(p.read_text().splitlines())}\t{p}') for p in sorted(pathlib.Path('pyx12').rglob('*.py')) if len(p.read_text().splitlines()) > 1000]"
```

### 3. Sanity-check categories before reporting

For each `# type: ignore` location, glance at one line of context — some are load-bearing (e.g. intentional type holes around X12 map XML) and some are stale survivors of refactors. Note which look like clean wins.

For TODOs, check `git blame` on a sample to see whether they're recent (worth surfacing) or ancient (probably won't be fixed and could just be removed).

### 4. Write the report

Output to stdout as markdown — do not create a file. Structure:

```
## Tech debt summary — pyx12/{scope}

**Counts:** N type-ignores · N TODOs · N legacy-typing imports · N bare-except · N modules >1000 LOC

### Top 5 to fix next
1. [file.py:line](file.py#Lline) — short reason (e.g. "single unused-ignore — clean win")
2. ...

### By category

#### `# type: ignore` (N total)
- arg-type: N — list locations
- union-attr: N — list locations
- ... (group by error code)

#### TODO/FIXME/HACK (N total)
- [file.py:line](file.py#Lline) — comment text

#### Legacy typing imports (N total)
- file.py: List, Dict → use built-ins

#### Bare except (N total)
- ...

#### Long modules
- file.py: N lines

### Notes
Anything ambiguous or context-dependent the user should know before acting.
```

### 5. Top 5 selection criteria

Rank candidates for "Top 5 to fix next" by **impact ÷ effort**:

- **High impact, low effort** (top of list): `unused-ignore` codes, single-file legacy typing imports, bare-except in non-error-handling code
- **High impact, medium effort**: a module with both >1000 LOC and >5 type-ignores
- **Skip**: ancient TODOs nobody owns, type-ignores in `pyx12/map/` (XML-driven), anything in `examples/` or `scripts/` (excluded from strict mypy already)

If a fix is small enough to do in this session, say so explicitly and offer to do it.

## Notes

- The mypy strict overrides in `pyproject.toml` exclude `pyx12.test.*`, `pyx12.tests.*`, `pyx12.examples.*`, `pyx12.scripts.*`, `pyx12.map.*` from untyped-def checks. Don't flag missing annotations in those modules — they're intentional.
- This skill is read-only. Don't fix anything during the scan; produce the report and let the user decide.
- Keep the report under ~80 lines. If a category has more than 10 hits, summarize ("12 in `error_handler.py`") instead of listing each one.
