#
# Configuration file for the Sphinx documentation builder.
#
# See: # https://www.sphinx-doc.org/en/master/usage/configuration.html

project = "pyvboxcli"
copyright = "2021, Leonard Crestez"
author = "Leonard Crestez"

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinxarg.ext",
]

# Preserve order in source code
autodoc_member_order = "bysource"

html_theme = "sphinx_rtd_theme"
