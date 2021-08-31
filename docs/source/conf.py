# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

lib = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Public_Sensor_Evaluation\sensortoolkit'
sys.path.insert(0, os.path.abspath(lib))
sys.path.insert(0, os.path.abspath(lib + '/_analysis'))
sys.path.insert(0, os.path.abspath(lib + '/_evaluation'))
sys.path.insert(0, os.path.abspath(lib + '/_format'))
sys.path.insert(0, os.path.abspath(lib + '/_ingest'))
sys.path.insert(0, os.path.abspath(lib + '/_models'))
sys.path.insert(0, os.path.abspath(lib + '/_performancereport'))
sys.path.insert(0, os.path.abspath(lib +  '/_pkg'))
sys.path.insert(0, os.path.abspath(lib + '/_plotting'))
sys.path.insert(0, os.path.abspath(lib + '/_qc'))
sys.path.insert(0, os.path.abspath(lib + '/_reference'))


# -- Project information -----------------------------------------------------
import sensortoolkit
project = 'sensortoolkit'
copyright = '2021, Samuel Frederick'
author = 'Samuel Frederick'

# The full version, including alpha/beta/rc tags
version = sensortoolkit.__version__
release = version

rst_epilog = '.. |sensortoolkit_version| replace:: ``%s``' % version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]


autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
#html_show_sourcelink = False  # Remove 'view source code' from top of page (for html, not python)
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
nbsphinx_allow_errors = True  # Continue through  errors
#autodoc_typehints = "description" # Sphinx-native method. Not as good as sphinx_autodoc_typehints
add_module_names = False # Remove namespaces from class/method signatures
#napoleon_google_docstring = False
#napoleon_use_param = False
#napoleon_use_ivar = True

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
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "collapse_navigation" : False,
    'navigation_depth': 4,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
