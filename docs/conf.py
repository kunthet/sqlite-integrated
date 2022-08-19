# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# imports
import sphinx_bootstrap_theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# import src.sqlite_integrated

# -- Project information -----------------------------------------------------

project = 'Sqlite-Integrated'
copyright = '2022, Balder Holst'
author = 'Balder Holst'

# The full version, including alpha/beta/rc tags
release = '0.0.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'


html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()


########################################
# html_theme = 'sphinx_rtd_theme'

# html_theme_options = {
#     'display_version': True,
#     'vcs_pageview_mode': '',
#     'style_nav_header_background': 'purple',
#     # Toc options
#     'collapse_navigation': False,
#     'sticky_navigation': False,
#     'navigation_depth': 4,
#     'includehidden': True,
#     'titles_only': False
# }

###################################
# import guzzle_sphinx_theme

# html_theme_path = guzzle_sphinx_theme.html_theme_path()
# html_theme = 'guzzle_sphinx_theme'

# # Register the theme as an extension to generate a sitemap.xml
# extensions.append("guzzle_sphinx_theme")

# # Guzzle theme options (see theme.conf for more information)
# html_theme_options = {
#     # Set the name of the project to appear in the sidebar
#     "project_nav_name": "Project Name",
# }

################################

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
