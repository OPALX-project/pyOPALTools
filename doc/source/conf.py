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
import unittest.mock
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# Mock dependencies
MOCK_MODULES = ['h5py',
                'matplotlib',
                'matplotlib.cm',
                'matplotlib.gridspec',
                'matplotlib.pyplot',
                'matplotlib.ticker',
                'matplotlib.widgets',
                'numpy',
                'pandas',
                'pylab',
                'seaborn',
                'scipy',
                'scipy.interpolate',
                'yt']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = unittest.mock.Mock()

# -- Project information -----------------------------------------------------

project = 'pyOPALTools'
copyright = '2020, Matthias Frey, Jochem Snuverink, Andreas Adelmann, Nicole Neveu, Renato Bellotti, Philippe Ganz'
author = 'Matthias Frey, Jochem Snuverink, Andreas Adelmann, Nicole Neveu, Renato Bellotti, Philippe Ganz'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
#    'sphinx.ext.napoleon' # For conversion from non-rst documentation
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Extension configuration -------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True
#    'private-members': True,
#    'special-members': True

}
