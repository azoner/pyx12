# Run pyx12 unit tests

Run the unit test suite using the local virtual environment. Accepts an optional argument: a specific test module name (e.g. `test_validation`) or file path to run a subset of tests. No argument runs the full suite.

## Steps

### 1. Determine scope

- No argument → run the full suite
- Argument matches a file in `pyx12/test/` → run that module only
- Argument is a path → pass it directly to pytest

### 2. Run tests

**Full suite:**
```
.venv/Scripts/python -m pytest pyx12/test/ -v
```

**Single module:**
```
.venv/Scripts/python -m pytest pyx12/test/{module}.py -v
```

**With coverage (use when explicitly requested):**
```
.venv/Scripts/python -m pytest pyx12/test/ -v --cov=pyx12 --cov-report=term-missing
```

### 3. Report results

- State pass/fail counts and any failures.
- For failures, show the test name, the assertion that failed, and the relevant source location.
- If all tests pass, confirm the count and move on — no recap needed.

### 4. On failure

- Read the failing test and the code under test to understand the root cause.
- If the failure is a pre-existing issue unrelated to recent changes, flag it and ask the user how to proceed before fixing anything.
- Do not modify tests to make them pass without understanding the intent.

## Notes
- If `.venv` is missing or `pytest` is not installed: `pip install -e ".[dev]"` inside the venv, or `.venv/Scripts/pip install pytest pytest-cov`.
- Tests use `unittest.TestCase` style but are discovered and run by pytest.
- Always run the full suite before reporting a task complete.
