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
sys.path.insert(0, os.path.abspath('./../../sciPyFoam'))
sys.path.insert(0, os.path.abspath('./../../sciPyFoam/postProcessing'))
sys.path.insert(0, os.path.abspath('_extensions'))

# -- Project information -----------------------------------------------------

project = 'sciPyFoam'
copyright = '2020, Zhikui Guo'
author = 'Zhikui Guo'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.mathjax', 
            'jinja',
            'sphinx.ext.autodoc',
            'sphinx.ext.autosummary',
            'sphinx.ext.coverage',
            'sphinx.ext.mathjax',
            'sphinx.ext.doctest',
            'sphinx.ext.viewcode',
            'sphinx.ext.extlinks',
            "sphinx.ext.intersphinx",
            # 'matplotlib.sphinxext.plot_directive',
            'sphinx.ext.napoleon',
            # 'sphinx_gallery.gen_gallery'
            ]
# avoid errors from import modules
autodoc_mock_imports = ["vtk", 'sciPyFoam']
# # intersphinx configuration
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3/", None),
#     "numpy": ("https://docs.scipy.org/doc/numpy/", None),
#     "matplotlib": ("https://matplotlib.org/", None),
# }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'rtd'
html_theme_path = ["themes"]
html_theme_options = {
    'sticky_navigation': False,
    'includehidden': False,
}
html_context = {
    "menu_links": [
        (
            '<i class="fa fa-book fa-fw"></i> License',
            "xxx",
        ),
        (
            '<i class="fa fa-comment fa-fw"></i> Contact',
            "xxx",
        ),
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            "https://gitlab.com/hydrothermal-openfoam/hydrothermalfoam",
        ),
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']