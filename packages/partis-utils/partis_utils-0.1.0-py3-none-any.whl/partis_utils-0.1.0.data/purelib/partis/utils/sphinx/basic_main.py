# -*- coding: utf-8 -*-
"""CLI for running sphinx-build

.. code-block:: bash

  python -m doc -b html latexpdf

"""

import sys
import os
import os.path as osp
import shutil
import re
import subprocess
import argparse
from argparse import RawTextHelpFormatter

from partis.pyproj import (
  norm_dist_name,
  join_dist_filename,
  dist_targz )

from partis.utils import caller_module

try:
  from importlib.metadata import metadata

except ImportError:
  from importlib_metadata import metadata

from .basic_conf import get_meta


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def basic_main(
  conf_dir,
  src_dir,
  root_dir,
  package = None,
  project = None,
  project_normed = None,
  project_filename = None,
  version = None ):
  """Convenience implementation of the ``__main__`` to build documentation and
  distribution file.


  Parameters
  ----------
  package : str
    Name of installed package to build documentation
  conf_dir : str
    Directory where conf.py is located
  src_dir : str
    Directory where 'index' document is located
  root_dir : str
    Directory for root project

  Returns
  -------
  int
    returncode

  Example
  -------

  .. code-block:: python

  from partis.utils.sphinx import basic_main

  if __name__ == "__main__":

    conf_dir = osp.abspath( osp.dirname(__file__) )
    root_dir = osp.abspath( osp.join( conf_dir, os.pardir ) )

    basic_main(
      package = 'partis',
      conf_dir = conf_dir,
      src_dir = root_dir,
      root_dir = root_dir )

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

  project = project or root_doc
  project_normed = project_normed or project
  version = version or ''

  # for filenames etc., replace all non-word characters with underscores
  project_normed = re.sub(r'[^\w]+', '_', project_normed.strip() ).lstrip('_')

  if not project_filename:
    if version:
      project_filename = join_dist_filename( [project_normed, version] )
    else:
      project_filename = project_normed

  dist_name = project_filename
  doc_dist_name = dist_name + '-doc'
  doc_dist_file = doc_dist_name + '.tar.gz'
  pdf_name = dist_name + '.pdf'

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-b", "--builder",
    type = str,
    nargs = '+',
    default = [ 'html' ],
    help = "builder to use passed to sphinx-build `-b` option. "
      "May give multiple builders to run in series." )

  parser.add_argument( "-o", "--outdir",
    type = str,
    default = None,
    help = "Output directory" )

  parser.add_argument( "--no-dist",
    action = 'store_true',
    help = f"Do not create a documentation distribution: {doc_dist_file}" )

  args = parser.parse_args()


  outdir = args.outdir

  if not outdir:
    outdir = osp.join( root_dir, 'dist' )

  build_dir = osp.join( root_dir, 'build' )

  if not osp.exists( outdir ):
    os.makedirs( outdir )

  if not osp.exists( build_dir ):
    os.makedirs( build_dir )

  doctrees = osp.join( build_dir, '.doctrees' )


  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  builds = list()

  for builder in args.builder:
    if builder == 'latexpdf':
      if shutil.which("pdflatex") is None:
        print(f"Command not found 'pdflatex'. Skipping: {builder}\n")
        continue
      
      elif os.name != 'nt' and shutil.which("latexmk") is None:
        # required to build on non-windows OS
        print(f"Command not found 'latexmk'. Skipping: {builder}\n")
        continue
    

    print(f"Running sphinx-doc builder: {builder}\n")

    builder_dir = osp.join( build_dir, builder )
    builds.append( (builder, builder_dir) )

    subprocess.check_call([
      'python3',
      '-m',
      'sphinx.cmd.build',
      '-M',
      builder,
      src_dir,
      build_dir,
      '-c',
      conf_dir ])

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  if not args.no_dist:

    print(f'Packaging documentation: {doc_dist_file}\n')
    
    
    with dist_targz(
      outname = doc_dist_file,
      outdir = outdir ) as dist:

      for builder, builder_dir in builds:
        if builder == 'latexpdf':
          # only copy in the generated pdf
          dist.copyfile(
            src = osp.join( build_dir, 'latex', pdf_name ),
            dst = '/'.join([ doc_dist_name, pdf_name ]) )

          shutil.copyfile(
            osp.join( build_dir, 'latex', pdf_name ), 
            osp.join( outdir, pdf_name ) )

        else:
          dist.copytree(
            src = builder_dir,
            dst = osp.join( doc_dist_name, builder ) )

  return 0
