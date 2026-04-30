"""Sphinx configuration for pyx12 documentation."""

import subprocess
import sys
from importlib.metadata import version as _get_version
from pathlib import Path

project = "pyx12"
author = "John Holland"
copyright = "%Y, John Holland"

release = _get_version("pyx12")
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
]


# Capture --help output for each console script using sys.executable so
# Windows Smart App Control's reputation-based block on entry-point shims
# (and Windows' CreateProcess PATH resolution differing from PATH search)
# never matter. Output goes under docs/_generated/cli/ and is included by
# docs/cli.rst via literalinclude.
_CLI_SCRIPTS = ("x12valid", "x12norm", "x12html", "x12info", "x12xml", "xmlx12")


def _capture_cli_help() -> None:
    out_dir = Path(__file__).parent / "_generated" / "cli"
    out_dir.mkdir(parents=True, exist_ok=True)
    for script in _CLI_SCRIPTS:
        # Set sys.argv[0] before main() runs so argparse picks the entry-point
        # name as prog (instead of "python.exe -m pyx12.scripts.x12norm").
        runner = (
            f"import sys; sys.argv = ['{script}', '--help']; "
            f"from pyx12.scripts.{script} import main; main()"
        )
        result = subprocess.run(
            [sys.executable, "-c", runner],
            capture_output=True,
            text=True,
            check=False,
        )
        (out_dir / f"{script}.txt").write_text(result.stdout, encoding="utf-8")


_capture_cli_help()

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

autosectionlabel_prefix_document = True

html_theme = "furo"
html_title = f"pyx12 {release}"
html_baseurl = "https://pyx12.readthedocs.io/"
html_last_updated_fmt = "%Y-%m-%d"

html_theme_options = {
    "source_repository": "https://github.com/azoner/pyx12/",
    "source_branch": "master",
    "source_directory": "docs/",
}

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}
autodoc_member_order = "bysource"
autodoc_typehints = "description"
typehints_fully_qualified = False
always_document_param_types = True

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
