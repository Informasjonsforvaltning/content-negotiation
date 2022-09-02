"""Sphinx configuration."""
project = "content-negotiation"
author = "Stig B. Dørmænen"
copyright = f"2022, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
