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

#lib = r'C:\Users\mkumar01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Master\sensortoolkit'
#sys.path.insert(0, os.path.abspath(lib))
sys.path.insert(0, os.path.abspath('../../sensortoolkit/'))

# -- Read the Docs Specific Configuration --------------------------------------

# This needs to be done before sensortoolkit is imported
#on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
#if on_rtd:
#    os.environ['SENSORTOOLKIT_CONFIGDIR'] = '/home/docs/source/'
#    os.environ['HOME'] = '/home/docs/'

# -- Project information -----------------------------------------------------
import sensortoolkit
project = 'sensortoolkit'
copyright = '2022, United States Environmental Protection Agency'
author = 'Samuel Frederick'

# The full version, including alpha/beta/rc tags
version = sensortoolkit.__version__
release = version

rst_epilog = '.. |formatted_version| replace:: ``%s``' % version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_panels',
    'rst2pdf.pdfbuilder'
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
html_theme = "sphinx_rtd_theme"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# rst2pdf
# -- Options for PDF output --------------------------------------------------

# Grouping the document tree into PDF files. List of tuples
# (source start file, target name, title, author, options).
#
# If there is more than one author, separate them with \\.
# For example: r'Guido van Rossum\\Fred L. Drake, Jr., editor'
#
# The options element is a dictionary that lets you override
# this config per-document. For example:
#
# ('index', 'MyProject', 'My Project', 'Author Name', {'pdf_compressed': True})
#
# would mean that specific document would be compressed
# regardless of the global 'pdf_compressed' setting.

#pdf_documents = [
#    ('index', u'sensortoolkit', u'sensortoolkit Documentation', u'Samuel Frederick'),
#]

# A comma-separated list of custom stylesheets. Example:
#pdf_stylesheets = ['sphinx', 'kerning', 'a4', 'twocolumn']

# A list of folders to search for stylesheets. Example:
#pdf_style_path = ['.', '_styles']

# Create a compressed PDF
# Use True/False or 1/0
# Example: compressed=True
# pdf_compressed = False

# A colon-separated list of folders to search for fonts. Example:
# pdf_font_path = ['/usr/share/fonts', '/usr/share/texmf-dist/fonts/']

# Language to be used for hyphenation support
# pdf_language = "en_US"

# Mode for literal blocks wider than the frame. Can be
# overflow, shrink or truncate
#pdf_fit_mode = "shrink"

# Section level that forces a break page.
# For example: 1 means top-level sections start in a new page
# 0 means disabled
# pdf_break_level = 0

# When a section starts in a new page, force it to be 'even', 'odd',
# or just use 'any'
# pdf_breakside = 'any'

# Insert footnotes where they are defined instead of
# at the end.
# pdf_inline_footnotes = True

# verbosity level. 0 1 or 2
#pdf_verbosity = 0

# If false, no index is generated.
# pdf_use_index = True

# If false, no modindex is generated.
# pdf_use_modindex = True

# If false, no coverpage is generated.
# pdf_use_coverpage = True

# Name of the cover page template to use
# pdf_cover_template = 'sphinxcover.tmpl'

# Documents to append as an appendix to all manuals.
# pdf_appendices = []

# Enable experimental feature to split table cells. Use it
# if you get "DelayedTable too big" errors
#pdf_splittables = False

# Set the default DPI for images
# pdf_default_dpi = 72

# Enable rst2pdf extension modules
# pdf_extensions = []

# Page template name for "regular" pages
# pdf_page_template = 'cutePage'

# Show Table Of Contents at the beginning?
# pdf_use_toc = True

# How many levels deep should the table of contents be?
#pdf_toc_depth = 9999

# Add section number to section references
#pdf_use_numbered_links = False

# Background images fitting mode
#pdf_fit_background_mode = 'scale'

# Repeat table header on tables that cross a page boundary?
#pdf_repeat_table_rows = True






###########################################################################
#          auto-created readthedocs.org specific configuration            #
###########################################################################


#
# The following code was added during an automated build on readthedocs.org
# It is auto created and injected for every build. The result is based on the
# conf.py.tmpl file found in the readthedocs.org codebase:
# https://github.com/rtfd/readthedocs.org/blob/main/readthedocs/doc_builder/templates/doc_builder/conf.py.tmpl
#
# Note: this file shouldn't rely on extra dependencies.

import importlib
import sys
import os.path

# Borrowed from six.
PY3 = sys.version_info[0] == 3
string_types = str if PY3 else basestring

from sphinx import version_info

# Get suffix for proper linking to GitHub
# This is deprecated in Sphinx 1.3+,
# as each page can have its own suffix
if globals().get('source_suffix', False):
    if isinstance(source_suffix, string_types):
        SUFFIX = source_suffix
    elif isinstance(source_suffix, (list, tuple)):
        # Sphinx >= 1.3 supports list/tuple to define multiple suffixes
        SUFFIX = source_suffix[0]
    elif isinstance(source_suffix, dict):
        # Sphinx >= 1.8 supports a mapping dictionary for multiple suffixes
        SUFFIX = list(source_suffix.keys())[0]  # make a ``list()`` for py2/py3 compatibility
    else:
        # default to .rst
        SUFFIX = '.rst'
else:
    SUFFIX = '.rst'

# Add RTD Static Path. Add to the end because it overwrites previous files.
if not 'html_static_path' in globals():
    html_static_path = []
if os.path.exists('_static'):
    html_static_path.append('_static')

# Add RTD Theme only if they aren't overriding it already
using_rtd_theme = (
    (
        'html_theme' in globals() and
        html_theme in ['default'] and
        # Allow people to bail with a hack of having an html_style
        'html_style' not in globals()
    ) or 'html_theme' not in globals()
)
if using_rtd_theme:
    theme = importlib.import_module('sphinx_rtd_theme')
    html_theme = 'sphinx_rtd_theme'
    html_style = None
    html_theme_options = {}
    if 'html_theme_path' in globals():
        html_theme_path.append(theme.get_html_theme_path())
    else:
        html_theme_path = [theme.get_html_theme_path()]

if globals().get('websupport2_base_url', False):
    websupport2_base_url = 'https://readthedocs.org/websupport'
    websupport2_static_url = 'https://assets.readthedocs.org/static/'


#Add project information to the template context.
context = {
    'using_theme': using_rtd_theme,
    'html_theme': html_theme,
    'current_version': "latest",
    'version_slug': "latest",
    'MEDIA_URL': "https://media.readthedocs.org/",
    'STATIC_URL': "https://assets.readthedocs.org/static/",
    'PRODUCTION_DOMAIN': "readthedocs.org",
    'proxied_static_path': "/_/static/",
    'versions': [
    ("latest", "/en/latest/"),
    ("stable", "/en/stable/"),
    ("v.0.9.0b3", "/en/v.0.9.0b3/"),
    ],
    'downloads': [ 
    ("pdf", "//sensortoolkit.readthedocs.io/_/downloads/en/latest/pdf/"),
    ("html", "//sensortoolkit.readthedocs.io/_/downloads/en/latest/htmlzip/"),
    ("epub", "//sensortoolkit.readthedocs.io/_/downloads/en/latest/epub/"),
    ],
    'subprojects': [ 
    ],
    'slug': 'sensortoolkit',
    'name': u'sensortoolkit',
    'rtd_language': u'en',
    'programming_language': u'words',
    'canonical_url': 'https://sensortoolkit.readthedocs.io/en/latest/',
    'analytics_code': 'None',
    'single_version': False,
    'conf_py_path': '/docs/source/',
    'api_host': 'https://readthedocs.org',
    'github_user': 'USEPA',
    'proxied_api_host': '/_',
    'github_repo': 'sensortoolkit',
    'github_version': 'master',
    'display_github': True,
    'bitbucket_user': 'None',
    'bitbucket_repo': 'None',
    'bitbucket_version': 'master',
    'display_bitbucket': False,
    'gitlab_user': 'None',
    'gitlab_repo': 'None',
    'gitlab_version': 'master',
    'display_gitlab': False,
    'READTHEDOCS': True,
    'using_theme': (html_theme == "default"),
    'new_theme': (html_theme == "sphinx_rtd_theme"),
    'source_suffix': SUFFIX,
    'ad_free': False,
    'docsearch_disabled': False,
    'user_analytics_code': '',
    'global_analytics_code': 'UA-17997319-1',
    'commit': '564a38f3',
}

# For sphinx >=1.8 we can use html_baseurl to set the canonical URL.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_baseurl
if version_info >= (1, 8):
    if not globals().get('html_baseurl'):
        html_baseurl = context['canonical_url']
    context['canonical_url'] = None





if 'html_context' in globals():
    
    html_context.update(context)
    
else:
    html_context = context

# Add custom RTD extension
if 'extensions' in globals():
    # Insert at the beginning because it can interfere
    # with other extensions.
    # See https://github.com/rtfd/readthedocs.org/pull/4054
    extensions.insert(0, "readthedocs_ext.readthedocs")
else:
    extensions = ["readthedocs_ext.readthedocs"]

# Add External version warning banner to the external version documentation
if 'branch' == 'external':
    extensions.insert(1, "readthedocs_ext.external_version_warning")
    readthedocs_vcs_url = 'None'
    readthedocs_build_url = 'https://readthedocs.org/projects/sensortoolkit/builds/19360943/'

project_language = 'en'

# User's Sphinx configurations
language_user = globals().get('language', None)
latex_engine_user = globals().get('latex_engine', None)
latex_elements_user = globals().get('latex_elements', None)

# Remove this once xindy gets installed in Docker image and XINDYOPS
# env variable is supported
# https://github.com/rtfd/readthedocs-docker-images/pull/98
latex_use_xindy = False

chinese = any([
    language_user in ('zh_CN', 'zh_TW'),
    project_language in ('zh_CN', 'zh_TW'),
])

japanese = any([
    language_user == 'ja',
    project_language == 'ja',
])

if chinese:
    latex_engine = latex_engine_user or 'xelatex'

    latex_elements_rtd = {
        'preamble': '\\usepackage[UTF8]{ctex}\n',
    }
    latex_elements = latex_elements_user or latex_elements_rtd
elif japanese:
    latex_engine = latex_engine_user or 'platex'

# Make sure our build directory is always excluded
exclude_patterns = globals().get('exclude_patterns', [])
exclude_patterns.extend(['_build'])