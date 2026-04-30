"""Sphinx configuration for pyx12 documentation."""

from importlib.metadata import version as _get_version

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
    "sphinxcontrib.programoutput",
    "myst_parser",
]

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
