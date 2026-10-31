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

## Testing
See the [/test](.claude/commands/test.md) skill for invocation, reporting, and authoring conventions.

## Preferences
- Record project conventions that every contributor should follow in this file. Personal working preferences belong in a gitignored `CLAUDE.local.md`
- This file and `.claude/` load into every contributor's Claude Code session, and `.claude/settings.json` can grant permissions and run hooks. Keep `settings.json` minimal (no hooks, no broad allows) and review changes to these paths like CI workflow changes
- No pickle / opaque deserialization for shipped or loaded artifacts — prefer generated `.py` modules (security: `__reduce__` is an arbitrary-code-execution surface unacceptable in a healthcare-data library)
- Every production release tag (`vN.N.N`) needs a matching `gh release create --latest` after the PyPI upload step
- Keep unreachable safety-net `return` statements in walker `while True` loops — they document intent and protect against future control-flow changes
- Prefer small, single-concern PRs. Refactors with broad test impact (>20 sites) get split: introduce the new shape with the old shape kept as a compat wrapper first, then migrate callers / tests / delete the wrapper in follow-up PRs
- Before introducing a `Protocol`, abstract base, or new wrapper type, check whether existing inheritance / concrete types already provide the contract — usually they do, and a parallel abstraction just shadows the existing structure
- When migrating tests off a last-error-wins stub (e.g. `errh_null`) reveals extra errors the stub had been hiding, tighten the input fixture to exercise only the scenario named in the test rather than rebadging the assertion to match the full error list
- Use "error" terminology consistently (`err_handler`, `seg_error`, `ErrorItem`); reuse the `ErrorItem` / `EleError` / `SegError` hierarchy for new validator return types instead of inventing "Finding" / "Issue" / etc. names
- IK4/AK4 error codes follow the X12 spec: `"1"` = required data element missing, `"2"` = conditional required missing, etc. When historical pyx12 emission disagrees with the spec (e.g. missing required composite was emitting `"2"` but the spec says `"1"`), fix the validator
- Preserve Sphinx `:param` / `:type` / `:return` / `:rtype` blocks when refactoring methods that have them; drop only the entries for dropped parameters
- Releases go through `.github/workflows/release.yml` on `v*` tag push (PyPA trusted publishing, no local credentials). Don't run `twine upload` locally — it duplicates the workflow and needs `~/.pypirc`. Use the `/publish` skill, which drives the tag + watch + GitHub-release side
- RC validation loop: every RC must be exercised against production-like traffic (real X12 files via the downstream worker) before promoting to final. If a regression surfaces, file a fix PR and cut a new RC — never re-tag a published version
- Use the [reviewer-writing](.claude/skills/reviewer-writing/SKILL.md) skill for PR descriptions, issue/PR comments, release notes and substantial commit messages: answer first, state the reader's job, evidence in the commit message or CI rather than pasted
- Merge PRs with **Squash and merge** (master history is one commit per PR, `subject (#N)`); the repo's squash message defaults to the commit messages, so a single-commit PR keeps its technical commit body and `Co-Authored-By` trailer
- Stale remote branch is deletable when (i) its content can't merge against current master AND (ii) its idea or bug fix is preserved elsewhere (architectural-review plan, already-fixed bug on master, etc.). Keep when it carries unique data not preserved elsewhere (e.g. XML map files for transactions not in master)
- Prefer both layers of test coverage for new behavior: (1) **unit tests** that exercise the tested code at a low level — pure-function `is_valid_errors` calls on a single segment_if/element_if, `apply_segment_errors` against a recording errh stub, etc. — and (2) **higher-level regression tests** that drive an entire X12 file through `x12n_document` and assert against the full ack / JSON output. Unit tests pin behavior at the producer; regression tests pin the integration shape. New invariants need both
- For end-to-end regression tests of X12 input → output behavior, add a key to `pyx12/test/x12testdata.py` with `source` + `resAck` / `res997` / `resJson` and use the existing `_test_999` / `_test_997` / `_test_json` helpers. Reserve ad-hoc tempfile-based tests for paths the fixture pattern can't reach (e.g. the file-open encoding path that needs a real filename, not a `StringIO`)
- Every input-derived value written into a 997/999 ack (IK4-04 / AK4-04 bad_value, IK3-01 seg_id, envelope ids, ...) goes through `pyx12.error_visitor.ack_safe`, which substitutes `?` (0x3F, in the X12 basic charset) for non-ASCII, control characters and the ack's own `~ * : ^` delimiters. Both ack visitors apply it to whole segments via `sanitize_ack_segment` in their `_write`; never write to the ack around that method
- Placeholder email addresses (test fixtures, PER04 values, docstring examples) are always `support@example.invalid`. `.invalid` is reserved by RFC 6761 and can never resolve; made-up domains like `null.com` turned out to be registered. Author/attribution addresses are not placeholders
- When an issue body or PR description quantifies expected test impact ("N tests will fail"), run the change locally to verify the count is current before scoping the plan around it. Such claims drift after refactors — issue #107 claimed 47 failures, actual was 0 once the producer-side errors-as-data refactor reshaped the test surface
- After running `ruff check --fix` or `ruff format` against a wide selection, check `git diff --stat` before staging and revert files outside the current PR's scope. Auto-cleanup of unrelated files (dead-comment removal, import sorting) inflates PR diffs and obscures the focused change
- For non-obvious technical choices in a fix (e.g. encoding=latin-1 vs utf-8, sanitize at output vs at input), explain the tradeoff before committing. Surface the decision so the user can redirect; don't bake it into a fait-accompli commit
- The `pypi` GitHub environment's `wait_timer` is 5 minutes (set 2026-05-05; was 15). The `required_reviewers` rule still gates on azoner approval. Adjust via `gh api repos/azoner/pyx12/environments/pypi -X PUT -F wait_timer=N ...`
- Segment validation routing rule (PR #182): element- and composite-level errors are preserved in `err_ele.errors` with their specific pyx12 code AND trigger exactly one `SEG_8_HAS_DATA_ELEMENT_ERRORS` in `err_seg.errors`. SEG-validator errors (`map_node is None`) collapse to that same single `SEG_8`. At most one `SEG_8` per segment regardless of how many child errors fired. Composite emissions in `_composite.py` set `map_node=self` so they flow through the `ele_error` path — `composite_if` has `data_ele`/`name`/`seq`, the right shape for `err_ele`. The single-emission invariant is what keeps ack output (IK3-04*8 / AK3-04*8) byte-identical via the visitor dedup
- When err_handler tree shape changes break resJson fixtures, write a one-shot AST-based regen tool (`tools/regen_resjson.py` pattern): use `ast.AnnAssign` (not `ast.Assign`) to find `datafiles: dict[str, ...] = {...}`, slice resJson values via `lineno`/`col_offset`/`end_lineno`/`end_col_offset`, regenerate via `x12n_document` with `fd_json`, write back, `ruff format`, then delete the tool. Keeps the diff to data-only changes
- TA1 emission gate (X12 spec): TA1 only emits when ISA14 (`ta1_req`) = `"1"`. The gate at `error_999.py`/`error_997.py` `visit_root_post` is correct and stays — never bypass it even when interchange errors are collected. Senders with ISA14=`"0"` are opting out of TA1 feedback; respect that.
- ISA loop content rule (X12 spec): an ISA loop is valid iff it contains at least one of a TA1 segment or a GS_LOOP. GS_LOOP is `usage="S"` in both control maps for that reason; bare `ISA/IEA` with neither emits `ISA_022_INVALID_CONTROL_STRUCTURE`. Tracked via the `isa_has_content` flag in the `x12n_document.py` main loop (reset on ISA, set on GS or TA1, checked on IEA).
- Implementation-dependent X12 codes (I4, I6, I9, I10, I11, I12, I13) keep their uppercase form in pyx12 string values: `ELE_I10_NOT_USED = "ELE_I10_NOT_USED"` (NOT `"ELE_I10_not_used"`). The X12 spec writes implementation-dependent codes uppercase, so mirror that in the constant value. Plain numeric-code constants still use the lowercase suffix convention (`ELE_1_MANDATORY_MISSING = "ELE_1_mandatory_missing"`)
- Envelope-level error-code migration pattern (used for ISA_* per issues #121/#160; reuse for future GS_*/ST_* work): (1) add the table entries + `x12_description` to `error_codes.py`; (2) extend `PREFIX_TO_LEVEL` in `test_error_codes.py` with the new prefix → level mapping; (3) migrate parser emissions to import the constants instead of raw X12 codes; (4) keep element validators in `map_if/_element.py` envelope-ignorant — they emit generic `ELE_*`; (5) translate at the boundary in `apply_segment_errors` via a position→code map (e.g. `ISA_ELE_POSITION_TO_CODE`) using `dataclasses.replace` (EleError is frozen, can't mutate `err_cde` directly); (6) visitors dereference via `ERROR_CODES[code].level == "<LEVEL>"` to get the X12 ack code, replacing fragile `err_str` substring matching
- Malformed input must never raise out of `X12Reader` iteration or the err_handler, not even `X12Error`: `x12n_document` only catches `X12Error` when it opens the reader, so any exception mid-file aborts with no 997/999. Record the fault through `_isa_error` / `_gs_error` / `_st_error` / `_seg_error` and keep reading. Uncaught exceptions on malformed X12 are ordinary public bugs (SECURITY.md scope)
- Segments outside an open transaction set (GS with no ST, stray/duplicate SE/GE/IEA) are reported on the innermost open envelope: an open GS of the current interchange gets gs `"5"` (AK9 R, per X12 RFI 1339), otherwise the interchange gets `ISA_024_INVALID_CONTENT`. Never put group-level faults on the TA1: X12 RFI 2435 scopes the TA1 to ISA/IEA. Rule and links live in `docs/errors.rst` ("Segments outside a transaction set"). A trailer closes every open loop up to its own header and never pops a non-matching one. Blank / whitespace-only segments are skipped silently
- Before settling an ack-code question, check X12's Requests for Interpretation (x12.org/resources/requests-for-interpretation) and cite the RFI in the code comment, commit message and docs; X12 has already ruled on many edge cases (e.g. RFI 1687: multiple TA1s are allowed)
- A public error-code constant that turns out to be dead stays importable until the next major version: mark it deprecated in `error_codes.py` and `docs/errors.rst` rather than deleting it in a patch release
- Credit external reporters and contributors: `Reported-by: Name (@handle)` for a report, `Co-authored-by: Name <commit email>` when their code lands (take the email from their PR's commits). When a fix supersedes an old open PR, use `Closes #N` in the landing PR and comment on the old PR where each part went. Thank them in the release notes
- When a merge conflict hits `pyx12/test/x12testdata.py` (two PRs inserting fixtures at the same anchor), take master's file and re-run the fixture generator for this PR's keys rather than hand-merging interleaved hunks. Review the regenerated ack lines against the PR's before merging
- When a PR's approach changes partway, write a standalone squash body for the final state; don't reuse a commit message written relative to an earlier commit on the branch (it won't exist on master)
- `CLAUDE.md` and `.claude/` have a code owner (`.github/CODEOWNERS`) and master requires code-owner review, so the maintainer's own PRs to them merge with the admin bypass (`gh pr merge --squash --admin`)