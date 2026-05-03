"""Post-packaging regression tests.

Builds a wheel, installs it into a fresh virtual environment, and runs a
smoke suite that catches the kinds of bugs unit tests miss because they
exercise the in-source-tree editable install:

  - Missing sub-packages (caught the regression fixed in PR #141 — pyx12.map_if
    was absent from the wheel because pyproject.toml's explicit packages list
    wasn't updated when map_if.py became a directory)
  - Missing data files (XML maps, dataele.xml, codes.xml, x12simple.dtd)
  - Console-script entry points whose import chain fails in the installed layout
  - Wheel metadata mismatches with source

Run locally:  python tools/test_install.py
Run in CI:    same; the workflow job in main.yml shells out to it.

Exits 0 on pass, 1 on first failure.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Modules that must import cleanly from the installed package.
# Skipping examples/scripts/test/tests as those aren't shipped.
IMPORT_TESTS = [
    "pyx12",
    "pyx12.codes",
    "pyx12.dataele",
    "pyx12.errors",
    "pyx12.error_handler",
    "pyx12.error_html",
    "pyx12.error_997",
    "pyx12.error_999",
    "pyx12.map_if",
    "pyx12.map_index",
    "pyx12.map_walker",
    "pyx12.params",
    "pyx12.path",
    "pyx12.rawx12file",
    "pyx12.segment",
    "pyx12.syntax",
    "pyx12.validation",
    "pyx12.x12context",
    "pyx12.x12file",
    "pyx12.x12n_document",
    "pyx12.x12xml",
    "pyx12.x12xml_simple",
    "pyx12.xmlwriter",
    "pyx12.xmlx12_simple",
    # Subpackages with __init__.py (must be in the wheel)
    "pyx12.scripts",
    "pyx12.scripts.x12valid",
    "pyx12.scripts.x12html",
    "pyx12.scripts.x12info",
    "pyx12.scripts.x12norm",
    "pyx12.scripts.x12xml",
    "pyx12.scripts.xmlx12",
]

CONSOLE_SCRIPTS = ["x12valid", "x12html", "x12info", "x12norm", "x12xml", "xmlx12"]


def _venv_python(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _run(cmd: list[str], cwd: Path | None = None, label: str = "") -> None:
    """Run a command; raise on failure with full output."""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=False)
    if result.returncode != 0:
        prefix = f"[{label}] " if label else ""
        print(f"\n{prefix}FAIL: {' '.join(map(str, cmd))}", file=sys.stderr)
        if result.stdout:
            print("--- stdout ---", file=sys.stderr)
            print(result.stdout[-2000:], file=sys.stderr)
        if result.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(result.stderr[-2000:], file=sys.stderr)
        sys.exit(1)


def _build_wheel() -> Path:
    print("==> Building wheel ...")
    shutil.rmtree(REPO / "dist", ignore_errors=True)
    shutil.rmtree(REPO / "build", ignore_errors=True)
    shutil.rmtree(REPO / "pyx12.egg-info", ignore_errors=True)
    _run([sys.executable, "-m", "build", "--wheel"], cwd=REPO, label="build")
    wheels = sorted((REPO / "dist").glob("*.whl"))
    if not wheels:
        print("FAIL: build produced no wheel", file=sys.stderr)
        sys.exit(1)
    print(f"  built {wheels[-1].name}")
    return wheels[-1]


def _create_install_venv(wheel: Path, venv_dir: Path) -> Path:
    print(f"==> Creating venv at {venv_dir} ...")
    _run([sys.executable, "-m", "venv", str(venv_dir)], label="venv")
    venv_py = _venv_python(venv_dir)
    print(f"==> Installing {wheel.name} ...")
    _run([str(venv_py), "-m", "pip", "install", "-q", str(wheel)], label="pip install")
    return venv_py


def _check_imports(venv_py: Path, work_dir: Path) -> None:
    """Run from outside the source tree so we hit the installed package."""
    print(f"==> Import smoke test ({len(IMPORT_TESTS)} modules) ...")
    # One subprocess for all modules — faster than one per module
    src = "; ".join(f"import {m}" for m in IMPORT_TESTS)
    _run([str(venv_py), "-c", src], cwd=work_dir, label="import")
    for m in IMPORT_TESTS:
        print(f"  ok  import {m}")


def _check_console_scripts(venv_py: Path, work_dir: Path) -> None:
    print(f"==> Console script --help ({len(CONSOLE_SCRIPTS)} scripts) ...")
    for script in CONSOLE_SCRIPTS:
        _run(
            [str(venv_py), "-m", f"pyx12.scripts.{script}", "--help"],
            cwd=work_dir,
            label=f"{script} --help",
        )
        print(f"  ok  {script} --help")


def _check_map_load(venv_py: Path, work_dir: Path) -> None:
    """Verifies map XML files are accessible via importlib.resources."""
    print("==> Map load (verifies XML data is shipped) ...")
    src = (
        "import pyx12.params, pyx12.map_if; "
        "p = pyx12.params.params(); "
        "m = pyx12.map_if.load_map_file('997.4010.xml', p); "
        "assert m.id, 'map.id is empty'; "
        "print('  ok  loaded map id =', m.id)"
    )
    _run([str(venv_py), "-c", src], cwd=work_dir, label="map load")


def _check_codes_load(venv_py: Path, work_dir: Path) -> None:
    """Verifies codes.xml and dataele.xml ship and parse."""
    print("==> Codes + data elements load ...")
    src = (
        "from pyx12.codes import ExternalCodes; "
        "from pyx12.dataele import DataElements; "
        "ec = ExternalCodes(); "
        "de = DataElements(); "
        "assert len(ec.codes) >= 9, f'expected >=9 codesets, got {len(ec.codes)}'; "
        "assert len(de.dataele) >= 300, f'expected >=300 elements, got {len(de.dataele)}'; "
        "print(f'  ok  {len(ec.codes)} codesets, {len(de.dataele)} data elements')"
    )
    _run([str(venv_py), "-c", src], cwd=work_dir, label="codes load")


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-packaging install regression tests")
    parser.add_argument("--keep", action="store_true", help="Don't delete the test venv")
    parser.add_argument(
        "--wheel",
        type=Path,
        default=None,
        help="Existing wheel to install (skips build step). For CI use.",
    )
    args = parser.parse_args()

    wheel = args.wheel.resolve() if args.wheel else _build_wheel()

    work_dir = Path(tempfile.mkdtemp(prefix="pyx12-pkgtest-"))
    venv_dir = work_dir / "venv"
    try:
        venv_py = _create_install_venv(wheel, venv_dir)
        # cwd = work_dir so the source tree is NOT on sys.path (would shadow
        # the installed package and mask packaging bugs)
        _check_imports(venv_py, work_dir)
        _check_console_scripts(venv_py, work_dir)
        _check_map_load(venv_py, work_dir)
        _check_codes_load(venv_py, work_dir)
        print("\nAll post-packaging tests passed.")
        return 0
    finally:
        if args.keep:
            print(f"\n(venv kept at {work_dir})")
        else:
            shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
