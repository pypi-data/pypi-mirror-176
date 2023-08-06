# -*- coding: utf-8 -*-
"""
"""

import sys
import os
import os.path as osp
import re
import subprocess
import shutil
import warnings
import datetime
from email.utils import parseaddr
import glob

from partis.pyproj import (
  norm_dist_name,
  join_dist_filename,
  dist_targz )

from partis.utils import caller_module

try:
  from importlib.metadata import metadata

except ImportError:
  from importlib_metadata import metadata


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
LATEX_FONTPKG = r"""
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
"""
# '\\usepackage[sfdefault]{roboto}' + '\n' +
# '\\usepackage[ttdefault]{nimbusmononarrow}', # change sans serif font

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
LATEX_PREAMBLE = r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{unicode-math}

% fix warnings with some fonts
\renewcommand{\textbar}{|}

% compatibility with mathjax, since < and > are sometimes treated as a security issue
\newcommand{\lt}{<}
\newcommand{\gt}{>}

\newcommand{\iunit}{\mathrm{i}}

\newcommand{\func}[2]{#1\left(#2\right)}
\newcommand{\ofunc}[2]{\operatorname{#1}\left(#2\right)}

\newcommand{\diag}[1]{\operatorname{diag}\left(#1\right)}
\newcommand{\tr}[1]{\operatorname{tr}\left(#1\right)}

\newcommand{\dsvec}[1]{\mathsf{#1}}
\newcommand{\dsmat}[1]{\boldsymbol{\mathsf{#1}}}
\newcommand{\dsop}[1]{\boldsymbol{\mathcal{#1}}}

\newcommand{\rankzero}[1]{\mathrm{#1}}
\newcommand{\rankone}[1]{\boldsymbol{\mathrm{#1}}}
\newcommand{\ranktwo}[1]{\boldsymbol{\mathit{#1}}}
\newcommand{\rankthree}[1]{\underline{\boldsymbol{\mathrm{#1}}}}
\newcommand{\rankfour}[1]{\underline{\boldsymbol{\mathit{#1}}}}
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
LATEX_SPHINXSETUP = ""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_meta(package):

  meta = metadata( package )
  project = meta['Name']
  version = meta['Version']
  description = meta['Summary']

  author = (
    meta['Author']
    or meta['Author-email']
    or meta['Maintainer']
    or meta['Maintainer-email'] )

  if not isinstance(author, str):
    author = next(iter(author))

  author, email = parseaddr( author )

  project_normed = norm_dist_name( project )

  return (
    project,
    project_normed,
    version,
    description,
    author,
    email )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def basic_conf(
  package = None,
  project = None,
  project_normed = None,
  project_filename = None,
  version = None,
  description = None,
  author = None,
  email = None,
  copyright_year = None,
  src_dir = None,
  root_doc = 'index',
  latex_theme = 'manual' ):
  """Convenience method for basic Sphinx and theme configuration options.

  Within the documentation ``conf.py``, call this method and set the ``globals``
  from the returned dictionary of options.
  Any option may be overritten after calling.

  Parameters
  ----------
  package : str
    Name of importable package for which documentation is being generated
  copyright_year : str | int

  Returns
  -------
  dict
    Sphinx options to be set

  Note
  ----
  Any 'list' options set by this method must be appended, instead of assigned,
  using ``+=`` or ``.append(...)``.


  Example
  -------

  .. code-block:: python

    from partis.utils.sphinx import basic_conf

    globals().update( basic_conf(
      package = 'partis',
      copyright_year = '2022' ) )

    exclude_patterns += [
      'src/partis-nwl/src/nwl' ]

    extensions += [
      'partis.utils.sphinx.ext' ]

  """

  

  if package:
    ( _project,
      _project_normed,
      _version,
      _description,
      _author,
      _email ) = get_meta(package)

    project = project or _project
    project_normed = project_normed or _project_normed
    version = version or _version
    description = description or _description
    author = author or _author
    email = email or _email

  project = project or root_doc
  project_normed = project_normed or project
  version = version or ''
  description = description or ''
  author = author or ''
  email = email or ''
  copyright_year = copyright_year or str(datetime.date.today().year)

  # NOTE: leading underscore can cause syntax errors in generated latex (.tex) files
  project = project.strip().lstrip('_')

  # for filenames etc., replace all non-word characters with underscores
  project_normed = re.sub(r'[^\w]+', '_', project_normed.strip() ).lstrip('_')

  static_path = osp.join( osp.dirname(osp.abspath(__file__)), '_static' )

  if not project_filename:
    if version:
      project_filename = join_dist_filename( [project_normed, version] )
    else:
      project_filename = project_normed

  copyright = f'{copyright_year}, {author} ( {email} )'

  print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print(f"package: {package}")
  print(f"project: {project} ({project_normed})")
  print(f"version: {version}")
  print(f"description: {description}")
  print(f"author: {author}")
  print(f"email: {email}")
  print(f"copyright_year: {copyright_year}")
  print(f"project_filename: {project_filename}")
  

  svgconverter = list()

  try:
    import cairosvg
    svgconverter = ['sphinxcontrib.cairosvgconverter']
  except:
    if shutil.which('inkscape'):
      svgconverter = ['sphinxcontrib.inkscapeconverter']
    else:
      warnings.warn('No svg conversion backend found: cairosvg, inkscape')


  bibtex_bibfiles = []

  if src_dir:
    bibtex_bibfiles += [
      osp.relpath(f, start = src_dir)
      for f in glob.glob(f"{src_dir}/*.bib") + glob.glob(f"{src_dir}/refs/*.bib") ]

  if bibtex_bibfiles:
    print(f"bibtex_bibfiles: {', '.join(bibtex_bibfiles)}")

  print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

  options = dict(
    # General information about the project.
    project = project,
    version = version,
    release = version,
    copyright = copyright,
    description = description,

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # general sphinx-doc configuration
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # If your documentation needs a minimal Sphinx version, state it here.
    #
    needs_sphinx = '3.1',

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = [
      # 'builtin' extensions
      # NOTE: this extension makes it so section titles would have to be unique
      # 'sphinx.ext.autosectionlabel',
      'sphinx.ext.autodoc',
      "sphinx.ext.intersphinx",
      'sphinx.ext.napoleon',
      'sphinx.ext.mathjax',
      'sphinx.ext.viewcode',
      # installed extensions
      'sphinx_copybutton',
      # 'sphinx_inline_tabs',
      # 'sphinx_tabs.tabs',
      'sphinx_design',
      'sphinx_subfigure',
      'sphinx_paramlinks',
      #'sphinx_tabs.tabs',
      'sphinxcontrib.bibtex',
      # custom extension
      'partis.utils.sphinx.ext',
      # svg image converter extension
      *svgconverter ],

    # Add any paths that contain templates here, relative to this directory.
    templates_path = ['_templates'],

    # The suffix(es) of source filenames.
    # You can specify multiple suffix as a list of string:
    #
    # source_suffix = ['.rst', '.md']
    source_suffix = '.rst',

    # The master toctree document.
    root_doc = root_doc,

    # The language for content autogenerated by Sphinx. Refer to documentation
    # for a list of supported languages.
    #
    # This is also used if you do content translation via gettext catalogs.
    # Usually you set "language" from the command line for these cases.
    language = None,

    # List of patterns, relative to source directory, that match files and
    # directories to ignore when looking for source files.
    # This patterns also effect to html_static_path and html_extra_path
    exclude_patterns = [
      '.git',
      '.nox',
      'tmp',
      'build',
      'dist',
      'examples',
      'venv*',
      'test',
      'Thumbs.db',
      '.DS_Store'],

    # The name of the Pygments (syntax highlighting) style to use.
    # pygments_style = 'sphinx'
    pygments_style = 'partis.utils.theme.pygments_light.PygmentsStyle',

    # If true, `todo` and `todoList` produce output, else they produce nothing.
    todo_include_todos = False,

    # If true, the current module name will be prepended to all description
    # unit titles (such as .. function::).
    add_module_names = False,

    # If true, figures, tables and code-blocks are automatically numbered if
    # they have a caption. At same time, the numref role is enabled. For now,
    # it works only with the HTML builder and LaTeX builder. Default is False.
    numfig = True,

    # If true, footnotes and citation include links back to text sections
    # that references them
    footenote_backlinks = False,

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # sphinxcontrib.bibtex
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    bibtex_bibfiles = bibtex_bibfiles,
    bibtex_reference_style = 'author_year',

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # sphinx.ext.autodoc
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # This value is a list of autodoc directive flags that should be automatically
    # applied to all autodoc directives. The supported flags are 'members',
    # 'undoc-members', 'private-members', 'special-members', 'inherited-members'
    # and 'show-inheritance'.
    autodoc_default_options = {
      'members': True,
      'special-members': False,
      # 'undoc-members': False,
      'exclude-members': None,
      'private-members': False,
      'special-members': False,
      # alphabetical, groupwise, or bysource
      'member-order': 'bysource',
      'show-inheritance' : True },


    autodoc_inherit_docstrings = True,

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # sphinx.ext.intersphinx
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    intersphinx_mapping = {
      "python": ("https://docs.python.org/3", None),
      "setuptools": ("https://setuptools.pypa.io/en/latest", None) },


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # sphinx.ext.napoleon
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    napoleon_google_docstring = False,
    napoleon_numpy_docstring = True,
    napoleon_include_init_with_doc = True,
    napoleon_include_private_with_doc = False,
    napoleon_include_special_with_doc = False,
    napoleon_use_admonition_for_examples = False,
    napoleon_use_admonition_for_notes = False,
    napoleon_use_admonition_for_references = False,
    napoleon_use_ivar = False,
    napoleon_use_param = True,
    napoleon_use_rtype = True,
    napoleon_use_keyword = False,
    napoleon_attr_annotations = True,


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # matplotlib.sphinxext.plot_directive
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    plot_include_source = True,
    plot_html_show_source_link = False,
    plot_html_show_formats = False,

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # html
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # The theme to use for HTML and HTML Help pages.  See the documentation for
    # a list of builtin themes.

    html_theme = 'furo',

    # Add any paths that contain custom static files (such as style sheets) here,
    # relative to this directory. They are copied after the builtin static files,
    # so a file named "default.css" will overwrite the builtin "default.css".

    html_static_path = [
      static_path ],

    html_css_files = [
      'tables.css' ],

    mathjax_path = "mathjax-3.2.0/es5/tex-chtml-full.js",

    html_logo = osp.join( static_path, 'app_icon.svg' ),

    html_title = f'{project} {version}',

    html_theme_options = {
      #-----------------------------------------------------------------------------
      # light theme
      'light_css_variables': {

        'color-foreground-primary' : '#31363B',
        'color-foreground-muted' : '#454545',
        'color-foreground-secondary' : '#292727',
        'color-foreground-border' : '#BAB9B8',

        'color-background-primary' : '#EFF0F1',
        'color-background-secondary' : '#dbe5ee',
        'color-background-border' : '#b1b5b9',

        'color-brand-primary' : '#4a7fac',
        'color-brand-content' : '#4a7fac',

        'color-highlighted-background' : '#3daee90',

        'color-guilabel-background' : '#30506b80',
        'color-guilabel-border' : '#1c466a80',

        'color-highlight-on-target' : '#e2d0b7',
        'color-problematic' : '#875e05'
      },
      #-----------------------------------------------------------------------------
      # dark theme
      'dark_css_variables': {

        'color-foreground-primary' : '#eff0f1',
        'color-foreground-muted' : '#736f6f',
        'color-foreground-secondary' : '#a7aaad',
        'color-foreground-border' : '#76797c',

        'color-background-primary' : '#31363b',
        'color-background-secondary' : '#3b4045',
        'color-background-border' : '#51575d',

        'color-brand-primary' : '#6ab5f4',
        'color-brand-content' : '#6ab5f4',

        'color-highlighted-background' : '#3daee90',

        'color-guilabel-background' : '#30506b80',
        'color-guilabel-border' : '#1c466a80',

        'color-highlight-on-target' : '#7c5418',
        'color-problematic' : '#e6c07b'
      }
    },

    pygments_light_style = 'partis.utils.theme.pygments_light.PygmentsStyle',
    pygments_dark_style = 'partis.utils.theme.pygments_dark.PygmentsStyle',

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # htmlhelp
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Output file base name for HTML help builder.
    htmlhelp_basename = f'{project_filename}_doc',

    html_copy_source = True,

    mathjax3_config = {'tex': {
      'macros': {
        'si': [r'\mathrm{#1}', 1],
        'iunit': r'\mathrm{i}',
        'func': [r'#1\left(#2\right)', 2],
        'ofunc': [ r'\operatorname{#1}\left(#2\right)', 2 ],
        'diag': [ r'\operatorname{diag}\left(#1\right)', 1 ],
        'tr': [ r'\operatorname{tr}\left(#1\right)', 1 ],
        'dsvec': [r'\mathsf{#1}', 1],
        'dsmat': [r'\boldsymbol{\mathsf{#1}}', 1],
        'dsop': [r'\boldsymbol{\mathcal{#1}}', 1],
        'rankzero': [r'\mathit{#1}', 1],
        'rankone': [r'\boldsymbol{\mathrm{#1}}', 1],
        'ranktwo': [r'\boldsymbol{\mathit{#1}}', 1],
        'rankthree': [r'\underline{\boldsymbol{\mathrm{#1}}}', 1],
        'rankfour': [r'\underline{\boldsymbol{\mathit{#1}}}', 1] } }},

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # latex
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    latex_engine = 'xelatex',
    latex_elements = {
      'pointsize': '10pt',
      'papersize': 'letterpaper',
      'fontpkg': LATEX_FONTPKG,
      'preamble': LATEX_PREAMBLE,
      'sphinxsetup': LATEX_SPHINXSETUP,
      'fncychap': '\\usepackage[Sonny]{fncychap}',
      # 'maketitle': '\\maketitle',
      'releasename': '',
      'babel': '',
      'printindex': '',
      'fontenc': '',
      'inputenc': '',
      'classoptions': '',
      'figure_align': 'htbp',
      # remove even/odd blank pages
      'extraclassoptions': 'openany' },

    # Grouping the document tree into LaTeX files. List of tuples
    # (source start file, target name, title,
    #  author, documentclass [howto, manual, or own class]).
    latex_documents = [
      ( root_doc, 
        f'{project_filename}.tex', 
        # LaTeX document title. Can be empty to use the title of the root_doc document. 
        '',
        # Author for the LaTeX document. 
        # The same LaTeX markup caveat as for title applies. 
        # Use \\and to separate multiple authors, as in: 
        # 'John \\and Sarah' (backslashes must be Python-escaped to reach LaTeX).
        author, 
        # theme [howto, manual, or own class]
        latex_theme, 
        # toctree_only: If true, the startdoc document itself is not included 
        # in the output, only the documents referenced by it via TOC trees.
        False ) ],

    # -- Options for manual page output ---------------------------------------

    # One entry per manual page. List of tuples
    # (source start file, name, description, authors, manual section).
    man_pages = [
        (root_doc, project_normed, f'{project} Documentation',
         [author], 1)
    ],

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # texinfo
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Grouping the document tree into Texinfo files. List of tuples
    # (source start file, target name, title, author,
    #  dir menu entry, description, category)
    texinfo_documents = [
        (root_doc, project_filename, f'{project} Documentation',
         author, project_normed, description,
         'Miscellaneous'),
    ] )

  return options
