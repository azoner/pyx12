---
name: publish
description: Publish pyx12 to PyPI or TestPyPI
argument-hint: "[test | release]"
disable-model-invocation: true
---

# Publish pyx12 to PyPI

Publish the pyx12 package. Accepts an optional argument: `test` to publish to TestPyPI, or no argument (or `release`) to publish to production PyPI.

## Steps

### 1. Read current version
Read the `version` field from `pyproject.toml`.

### 2. Confirm with user
Tell the user the version and target (TestPyPI or PyPI) and ask them to confirm before proceeding.

### 3. Clean previous builds
```
rm -rf dist/ build/ *.egg-info
```

### 4. Build the package
```
.venv/Scripts/python -m build
```
Verify that `dist/` contains both a `.whl` and `.tar.gz` for the correct version.

### 5. Check the distribution
```
.venv/Scripts/python -m twine check dist/*
```
Fix any errors before continuing.

### 6. Publish

**Test target** (`/publish test`):
```
.venv/Scripts/python -m twine upload --repository testpypi dist/*
```
Credentials use the `__token__` username and a TestPyPI API token.

**Release target** (`/publish` or `/publish release`):
```
.venv/Scripts/python -m twine upload dist/*
```
Credentials use the `__token__` username and a PyPI API token.

### 7. Tag the release in git (release target only)

After a successful production publish:
```
git tag -a v{version} -m "Release v{version}"
git push origin v{version}
```

### 8. Create the GitHub release (release target only)

For production releases (not pre-releases / RCs), always create a matching GitHub release so the tag isn't orphaned. Use auto-generated notes from the commit log, mark it `--latest`:

```
gh release create v{version} --title "v{version}" --generate-notes --latest
```

For pre-release tags (anything matching `v*rc*`, `v*beta*`, `v*alpha*`, `v*b{N}`, etc.), use `--prerelease` instead of `--latest` and skip the "latest" flag.

### 9. Report

Tell the user the tag has been pushed and show both URLs:
- PyPI: `https://pypi.org/project/pyx12/{version}/`
- GitHub release: `https://github.com/azoner/pyx12/releases/tag/v{version}`

### Notes
- Never hardcode tokens; let twine read them from `~/.pypirc` or prompt interactively.
- If `build` / `twine` are not installed, run `uv pip install -e ".[dev]"` (they are part of the `dev` extra in `pyproject.toml`).
- For TestPyPI, the install command to verify is: `pip install --index-url https://test.pypi.org/simple/ pyx12=={version}`
