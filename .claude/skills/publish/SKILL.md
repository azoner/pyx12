---
name: publish
description: Tag a release and watch the GitHub release workflow publish to TestPyPI + PyPI
argument-hint: "[release | dryrun]"
disable-model-invocation: true
---

# Publish pyx12

`.github/workflows/release.yml` runs on `v*` tag push and publishes to TestPyPI
then PyPI via PyPA trusted publishing — no local credentials required. This
skill drives the tag-and-watch side: pre-flight verification, tag, push, watch
the workflow, and create the GitHub release.

Accepts an optional argument:
- (no argument or `release`) — full publish flow.
- `dryrun` — pre-flight verification only; no tag, no push, no upload.

## Steps

### 1. Read current version
Read the `version` field from `pyproject.toml`. Confirm `pyx12/version.py` matches.

### 2. Confirm with user
Tell the user the version (e.g. `4.0.0rc1` or `4.0.0`) and what will happen
(tag → workflow → TestPyPI → PyPI → GitHub release). Ask them to confirm.

### 3. Pre-flight verification
All of these must pass before tagging:
```
uv lock --check          # version bump must have re-locked; CI runs uv sync --locked
.venv/Scripts/python.exe -m pytest pyx12/test/
.venv/Scripts/python.exe -m mypy --strict pyx12
.venv/Scripts/python.exe -m ruff check pyx12
.venv/Scripts/python.exe -m ruff format --check pyx12
.venv/Scripts/python.exe tools/check_maps.py
.venv/Scripts/python.exe tools/test_install.py
```

If `dryrun`, stop here.

### 4. Verify clean master
```
git status        # working tree must be clean
git rev-parse --abbrev-ref HEAD  # must be 'master'
git fetch origin && git status -sb  # must be in sync with origin/master
```
The release workflow trusts that the tag points at a master commit that has
already passed CI. Don't tag from a feature branch or with uncommitted changes.

### 5. Tag and push
```
git tag -a v{version} -m "Release v{version}"
git push origin v{version}
```

### 6. Watch the release workflow
The tag push triggers `.github/workflows/release.yml`, which runs three jobs in
sequence:
- `build` — sdist + wheel via `uv build`, runs `pytest -q` as a smoke test.
- `publish-testpypi` — uploads to TestPyPI (`skip-existing: true`).
- `publish-pypi` — uploads to PyPI.

```
gh run list --workflow=release.yml --limit=1
gh run watch <run-id>
```
If any job fails, surface the failure. Trusted publishing means no credentials
are local — failures are usually about version conflicts on PyPI or workflow
permissions.

### 7. Create the GitHub release

If a curated release-notes draft exists at
`~/.claude/plans/release-notes-{X.Y.Z}.md`, prefer `--notes-file` over
`--generate-notes`.

Breaking changes accumulate in `~/.claude/plans/release-notes-next.md` as PRs
land. Before tagging, rename it to `release-notes-{X.Y.Z}.md`, confirm its
**Breaking changes** section lists every behaviour change since the last
production tag (check `git log vPREV..HEAD` and the merged PR descriptions),
and fix the install line and compare link. Never publish a production release
whose notes omit a known breaking change.

**Production releases** (no `rc`/`beta`/`alpha` suffix) — mark `--latest`:
```
gh release create v{version} --title "v{version}" --generate-notes --latest
```

**Pre-releases** (`v*rc*`, `v*beta*`, `v*alpha*`, `v*b{N}*`) — mark
`--prerelease`, drop `--latest`:
```
gh release create v{version} --title "v{version}" --generate-notes --prerelease
```

### 8. Report

Show the user:
- PyPI: `https://pypi.org/project/pyx12/{version}/`
- GitHub release: `https://github.com/azoner/pyx12/releases/tag/v{version}`
- Workflow run: `https://github.com/azoner/pyx12/actions/runs/{run-id}`

## Notes

- **No credentials needed locally.** `release.yml` uses PyPA trusted publishing
  (`id-token: write`) against the `testpypi` and `pypi` GitHub environments.
  Token rotation happens in those environment settings, not in `~/.pypirc`.
- **Pre-release versions on PyPI** (e.g. `4.0.0rc1`) show as "Pre-release";
  `pip install pyx12` won't pick them up. Users need `pip install pyx12==4.0.0rc1`
  or `pip install pyx12 --pre`.
- **Re-tagging a version** is rejected by PyPI on the second upload.
  TestPyPI tolerates it because of `skip-existing: true`. To recut, bump the
  version (e.g. `4.0.0rc1` → `4.0.0rc2`) — never reuse a tag.
- **Manual local publish** (rare — only when CI is broken):
  ```
  .venv/Scripts/python.exe -m build
  .venv/Scripts/python.exe -m twine check dist/*
  .venv/Scripts/python.exe -m twine upload --repository {testpypi|pypi} dist/*
  ```
  Requires `~/.pypirc` or `TWINE_USERNAME=__token__` + `TWINE_PASSWORD=pypi-...`
  set locally. Then tag + push + `gh release create`.
- **Verify TestPyPI install** (optional, post-publish): in a fresh venv,
  `pip install --index-url https://test.pypi.org/simple/ pyx12=={version}` and
  smoke-test against an X12 file.
