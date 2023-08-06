"""Usage of `setup.py` is deprecated, and is supplied only for legacy installation.
"""
import sys
import os
import os.path as osp
from pathlib import (
  Path,
  PurePath,
  PurePosixPath)
import importlib
import logging
import argparse
import subprocess
import tempfile
from argparse import RawTextHelpFormatter
logger = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def egg_info( args ):

  logger.warning(
    "running legacy 'setup.py egg_info'" )

  dir = Path(args.egg_base).joinpath(EGG_INFO_NAME)

  if not dir.exists():
    dir.mkdir(parents=True, exist_ok = True)

  with open(dir.joinpath('PKG-INFO'), 'wb' ) as fp:  
    fp.write( PKG_INFO )

  with open( dir.joinpath('setup_requires.txt'), 'wb' ) as fp: 
    fp.write( b'' )

  with open( dir.joinpath('requires.txt'), 'wb' ) as fp: 
    fp.write( REQUIRES )

  with open( dir.joinpath('SOURCES.txt'), 'wb' ) as fp:
    fp.write( SOURCES )

  with open( dir.joinpath('top_level.txt'), 'wb' ) as fp:
    fp.write( TOP_LEVEL )

  with open( dir.joinpath('entry_points.txt'), 'wb' ) as fp:
    fp.write( ENTRY_POINTS )

  with open(dir.joinpath('dependency_links.txt'), 'wb' ) as fp:
    fp.write( b'' )

  with open( dir.joinpath('not-zip-safe'), 'wb' ) as fp:
    fp.write( b'' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_wheel( args ):

  logger.warning(
    "running legacy 'setup.py bdist_wheel'" )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  backend.build_wheel(
    wheel_directory = args.dist_dir or args.bdist_dir or '.' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install( args ):

  logger.warning(
    "running legacy 'setup.py install'" )

  reqs = [ f"{r}" for r in build_requires ]

  subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    *reqs ] )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  with tempfile.TemporaryDirectory() as tmpdir:
    wheel_name = backend.build_wheel(
      wheel_directory = tmpdir )

    subprocess.check_call([
      sys.executable,
      '-m',
      'pip',
      'install',
      tmpdir.joinpath(wheel_name) ]) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dummy( args ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  logging.basicConfig(
    level = logging.INFO,
    format = "{name}:{levelname}: {message}",
    style = "{" )


  logger.warning(
    "'setup.py' is deprecated, limited support for legacy installs. Upgrade pip." )

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  subparsers = parser.add_subparsers()

  #.............................................................................
  egg_info_parser = subparsers.add_parser( 'egg_info' )

  egg_info_parser.set_defaults( func = egg_info )

  egg_info_parser.add_argument( "-e", "--egg-base",
    type = str,
    default = '.' )

  #.............................................................................
  bdist_wheel_parser = subparsers.add_parser( 'bdist_wheel' )

  bdist_wheel_parser.set_defaults( func = bdist_wheel )

  bdist_wheel_parser.add_argument( "-b", "--bdist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "-d", "--dist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "--python-tag",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--plat-name",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--py-limited-api",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--build-number",
    type = str,
    default = None )

  #.............................................................................
  install_parser = subparsers.add_parser( 'install' )

  install_parser.set_defaults( func = install )

  install_parser.add_argument( "--record",
    type = str,
    default = None )

  install_parser.add_argument( "--install-headers",
    type = str,
    default = None )

  install_parser.add_argument( "--compile",
    action='store_true' )

  install_parser.add_argument( "--single-version-externally-managed",
    action='store_true' )

  #.............................................................................
  clean_parser = subparsers.add_parser( 'clean' )

  clean_parser.set_defaults( func = dummy )

  clean_parser.add_argument( "-a", "--all",
    action='store_true' )

  args = parser.parse_args( )

  args.func( args )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE: these are templated literal values substituded by the backend when
# building the source distribution

build_backend = 'partis.pyproj.backend'
backend_path = []
build_requires = ['wheel', 'PySide2<5.15,>=5.14; python_version < "3.8"', 'PySide2<5.16,>=5.15; python_version >= "3.8"', 'lxml>=4.2.5', 'partis-pyproj>=0.1.0']

EGG_INFO_NAME = 'partis-view.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-view\nVersion: 0.1.0\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Graphical interface for viewing and editing workflow files\nLicense-File: LICENSE.txt\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Intended Audience :: Science/Research\nClassifier: Topic :: Scientific/Engineering\nClassifier: Topic :: System :: Clustering\nClassifier: Programming Language :: Python\nClassifier: Operating System :: POSIX :: Linux\nClassifier: Programming Language :: Python :: 3\nClassifier: Development Status :: 4 - Beta\nProvides-Extra: doc\nRequires-Dist: wheel\nRequires-Dist: partis-schema>=0.1.0\nRequires-Dist: PySide2<5.15,>=5.14; python_version < "3.8"\nRequires-Dist: Jinja2>=3.0.0\nRequires-Dist: lxml>=4.2.5\nRequires-Dist: partis-pyproj>=0.1.0\nRequires-Dist: scipy>=1.3.1\nRequires-Dist: partis-utils[asy,theme]>=0.1.0\nRequires-Dist: PySide2<5.16,>=5.15; python_version >= "3.8"\nRequires-Dist: partis-utils[sphinx]>=0.1.0; extra == "doc"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.view`` package is a graphical interface for viewing and editing workflow files.\n\nhttps://nanohmics.bitbucket.io/doc/partis/view'

REQUIRES = b'wheel\npartis-schema>=0.1.0\nPySide2<5.15,>=5.14; python_version < "3.8"\nJinja2>=3.0.0\nlxml>=4.2.5\npartis-pyproj>=0.1.0\nscipy>=1.3.1\npartis-utils[asy,theme]>=0.1.0\nPySide2<5.16,>=5.15; python_version >= "3.8"\npartis-utils[sphinx]>=0.1.0; extra == "doc"'

SOURCES = b'partis_view-0.1.0/src/view/__init__.py\npartis_view-0.1.0/src/view/dialog/__init__.py\npartis_view-0.1.0/src/view/dialog/hint.py\npartis_view-0.1.0/src/view/dialog/log.py\npartis_view-0.1.0/src/view/dialog/progress.py\npartis_view-0.1.0/src/view/__main__.py\npartis_view-0.1.0/src/view/main_window.py\npartis_view-0.1.0/src/view/edit/__init__.py\npartis_view-0.1.0/src/view/edit/workdir.py\npartis_view-0.1.0/src/view/edit/select_editor.py\npartis_view-0.1.0/src/view/edit/editor_map.py\npartis_view-0.1.0/src/view/edit/project.py\npartis_view-0.1.0/src/view/edit/file_editor.py\npartis_view-0.1.0/src/view/edit/plugin.py\npartis_view-0.1.0/src/view/edit/text/__init__.py\npartis_view-0.1.0/src/view/edit/text/plaintext.py\npartis_view-0.1.0/src/view/edit/text/find_replace.py\npartis_view-0.1.0/src/view/edit/text/code.py\npartis_view-0.1.0/src/view/edit/var_tree/__init__.py\npartis_view-0.1.0/src/view/edit/var_tree/var_tree.py\npartis_view-0.1.0/src/view/edit/var_tree/var_tree_item.py\npartis_view-0.1.0/src/view/edit/schema_editor.py\npartis_view-0.1.0/src/view/base/crumbs.py\npartis_view-0.1.0/src/view/base/__init__.py\npartis_view-0.1.0/src/view/base/base.py\npartis_view-0.1.0/src/view/base/widget_stack.py\npartis_view-0.1.0/src/view/manager.py\npartis_view-0.1.0/src/view/theme/__init__.py\npartis_view-0.1.0/src/view/theme/pygments_style.py\npartis_view-0.1.0/src/view/theme/images/icons/vsplit.svg\npartis_view-0.1.0/src/view/theme/images/icons/new.svg\npartis_view-0.1.0/src/view/theme/images/icons/vhsplit.svg\npartis_view-0.1.0/src/view/theme/images/icons/settings.svg\npartis_view-0.1.0/src/view/theme/images/icons/forward.svg\npartis_view-0.1.0/src/view/theme/images/icons/move_down.svg\npartis_view-0.1.0/src/view/theme/images/icons/hsplit.svg\npartis_view-0.1.0/src/view/theme/images/icons/move_up.svg\npartis_view-0.1.0/src/view/theme/images/icons/base.svg\npartis_view-0.1.0/src/view/theme/images/icons/down_arrow.svg\npartis_view-0.1.0/src/view/theme/images/icons/save.svg\npartis_view-0.1.0/src/view/theme/images/icons/load.svg\npartis_view-0.1.0/src/view/theme/images/icons/back.svg\npartis_view-0.1.0/src/view/theme/images/icons/script.svg\npartis_view-0.1.0/src/view/theme/images/icons/config.svg\npartis_view-0.1.0/src/view/theme/images/icons/left_arrow.svg\npartis_view-0.1.0/src/view/theme/images/icons/edit.svg\npartis_view-0.1.0/src/view/theme/images/icons/restore.svg\npartis_view-0.1.0/src/view/theme/images/icons/right_arrow.svg\npartis_view-0.1.0/src/view/theme/images/icons/up_arrow.svg\npartis_view-0.1.0/src/view/theme/images/icons/add.svg\npartis_view-0.1.0/src/view/theme/images/icons/app_icon.svg\npartis_view-0.1.0/src/view/theme/images/icons/pancake.svg\npartis_view-0.1.0/src/view/theme/images/icons/app_icon.png\npartis_view-0.1.0/src/view/theme/images/icons/disk.svg\npartis_view-0.1.0/src/view/theme/images/icons/remove.svg\npartis_view-0.1.0/src/view/theme/images/icons/connect.svg\npartis_view-0.1.0/src/view/theme/images/icons/saveAs.svg\npartis_view-0.1.0/src/view/theme/images/tree/branch-skip.svg\npartis_view-0.1.0/src/view/theme/images/tree/branch-end.svg\npartis_view-0.1.0/src/view/theme/images/tree/branch-more.svg\npartis_view-0.1.0/src/view/theme/images/tree/branch-closed.svg\npartis_view-0.1.0/src/view/theme/images/tree/branch-open.svg\npartis_view-0.1.0/src/view/theme/images/base/undock-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/right_arrow_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/radio_checked-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/down_arrow-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/radio_checked_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/transparent.svg\npartis_view-0.1.0/src/view/theme/images/base/up_arrow_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/branch_closed-on.svg\npartis_view-0.1.0/src/view/theme/images/base/down_arrow.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_checked_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/spinup_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/left_arrow_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/stylesheet-vline.svg\npartis_view-0.1.0/src/view/theme/images/base/stylesheet-branch-more.svg\npartis_view-0.1.0/src/view/theme/images/base/left_arrow.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_checked-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/branch_open-on.svg\npartis_view-0.1.0/src/view/theme/images/base/radio_unchecked_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/vsepartoolbars.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_unchecked_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/hmovetoolbar.svg\npartis_view-0.1.0/src/view/theme/images/base/stylesheet-branch-end-open.svg\npartis_view-0.1.0/src/view/theme/images/base/hsepartoolbar.svg\npartis_view-0.1.0/src/view/theme/images/base/stylesheet-branch-end.svg\npartis_view-0.1.0/src/view/theme/images/base/right_arrow.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_indeterminate_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/radio_unchecked-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/vmovetoolbar.svg\npartis_view-0.1.0/src/view/theme/images/base/up_arrow.svg\npartis_view-0.1.0/src/view/theme/images/base/close-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/stylesheet-branch-end-closed.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_unchecked-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/down_arrow_disabled.svg\npartis_view-0.1.0/src/view/theme/images/base/up_arrow-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/sizegrip.svg\npartis_view-0.1.0/src/view/theme/images/base/radio_checked.svg\npartis_view-0.1.0/src/view/theme/images/base/close-pressed.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_indeterminate-hover.svg\npartis_view-0.1.0/src/view/theme/images/base/close.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_indeterminate.svg\npartis_view-0.1.0/src/view/theme/images/base/branch_closed.svg\npartis_view-0.1.0/src/view/theme/images/base/branch_open.svg\npartis_view-0.1.0/src/view/theme/images/base/undock.svg\npartis_view-0.1.0/src/view/theme/images/base/checkbox_checked.svg\npartis_view-0.1.0/src/view/theme/utils.py\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Regular.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-LightItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Thin.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-BoldItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Italic.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-MediumItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-BoldItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-BlackItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-LightItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Medium.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Bold.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Italic.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-ThinItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/LICENSE.txt\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Thin.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Black.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Light.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-MediumItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Light.ttf\npartis_view-0.1.0/src/view/theme/fonts/RobotoMono-Regular.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Medium.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-ThinItalic.ttf\npartis_view-0.1.0/src/view/theme/fonts/Roboto-Bold.ttf\npartis_view-0.1.0/src/view/theme/styles/status.qss\npartis_view-0.1.0/src/view/theme/styles/scroll.qss\npartis_view-0.1.0/src/view/theme/styles/tree.qss\npartis_view-0.1.0/src/view/theme/styles/table.qss\npartis_view-0.1.0/src/view/theme/styles/edit.qss\npartis_view-0.1.0/src/view/theme/styles/button.qss\npartis_view-0.1.0/src/view/theme/styles/main.qss\npartis_view-0.1.0/src/view/theme/styles/base.qss\npartis_view-0.1.0/src/view/theme/styles/container.qss\npartis_view-0.1.0/src/view/theme/styles/menu.qss\npartis_view-0.1.0/src/view/theme/styles/_main.qss\npartis_view-0.1.0/src/view/settings.py\npartis_view-0.1.0/src/view/schema/tree_edit_deligate.py\npartis_view-0.1.0/src/view/schema/__init__.py\npartis_view-0.1.0/src/view/schema/tree_edit_w.py\npartis_view-0.1.0/src/view/schema/edit_w.py\npartis_view-0.1.0/src/view/schema/name_w.py\npartis_view-0.1.0/src/view/schema/int_w.py\npartis_view-0.1.0/src/view/schema/pass_w.py\npartis_view-0.1.0/src/view/schema/str_w.py\npartis_view-0.1.0/src/view/schema/hint_w.py\npartis_view-0.1.0/src/view/schema/union_w.py\npartis_view-0.1.0/src/view/schema/color_w.py\npartis_view-0.1.0/src/view/schema/map_w.py\npartis_view-0.1.0/src/view/schema/tree_node_map.py\npartis_view-0.1.0/src/view/schema/type_combo_w.py\npartis_view-0.1.0/src/view/schema/optional_w.py\npartis_view-0.1.0/src/view/schema/struct_w.py\npartis_view-0.1.0/src/view/schema/evaluated_w.py\npartis_view-0.1.0/src/view/schema/float_w.py\npartis_view-0.1.0/src/view/schema/bool_w.py\npartis_view-0.1.0/src/view/schema/tree_edit_node.py\npartis_view-0.1.0/src/view/schema/list_w.py\npartis_view-0.1.0/src/view/highlight/__init__.py\npartis_view-0.1.0/src/view/highlight/pygments.py\npartis_view-0.1.0/doc/conf.py\npartis_view-0.1.0/doc/__init__.py\npartis_view-0.1.0/doc/index.rst\npartis_view-0.1.0/doc/src/partis.view.__main__.rst\npartis_view-0.1.0/doc/__main__.py\npartis_view-0.1.0/test/conftest.py\npartis_view-0.1.0/test/900_view/conftest.py\npartis_view-0.1.0/test/900_view/__init__.py\npartis_view-0.1.0/test/900_view/test_901_app.py\npartis_view-0.1.0/pkgaux/build_qrc.py\npartis_view-0.1.0/pkgaux/__init__.py\npartis_view-0.1.0/pyproject.toml\npartis_view-0.1.0/LICENSE.txt\npartis_view-0.1.0/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b'[console_scripts]\npartis-view = partis.view.__main__:main\n\n'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
