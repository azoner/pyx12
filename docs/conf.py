"""Sphinx configuration for pyx12 documentation."""

import importlib
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
    "autoapi.extension",
]


# Capture --help output for each console script by importing each module's
# build_parser() and calling format_help() in-process. Previously this used
# a subprocess with sys.executable, which silently produced empty .txt files
# in environments where the subprocess Python could not import pyx12 (e.g.
# Read the Docs). In-process import surfaces any failure as a Sphinx build
# error instead of an empty <pre> block on the rendered page.
_CLI_SCRIPTS = ("x12valid", "x12norm", "x12html", "x12info", "x12xml", "xmlx12")


def _capture_cli_help() -> None:
    out_dir = Path(__file__).parent / "_generated" / "cli"
    out_dir.mkdir(parents=True, exist_ok=True)
    for script in _CLI_SCRIPTS:
        mod = importlib.import_module(f"pyx12.scripts.{script}")
        parser = mod.build_parser()
        (out_dir / f"{script}.txt").write_text(parser.format_help(), encoding="utf-8")


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

# sphinx-autoapi: parse the package source to generate the API reference.
# Output lands in docs/api/ at build time and is gitignored; the toctree
# entry "api" in docs/index.rst resolves to autoapi's generated index.
autoapi_dirs = ["../pyx12"]
autoapi_root = "api"
autoapi_keep_files = False
autoapi_add_toctree_entry = False
autoapi_member_order = "bysource"
autoapi_python_class_content = "both"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_ignore = [
    "*/test/*",
    "*/tests/*",
    "*/examples/*",
    "*/scripts/*",
    "*/map/*",
]
