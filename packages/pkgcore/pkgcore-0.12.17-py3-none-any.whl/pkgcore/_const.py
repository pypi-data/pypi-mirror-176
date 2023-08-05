from os.path import join, abspath
import sys

from snakeoil import process

INSTALL_PREFIX = abspath(sys.prefix)
DATA_PATH = join(INSTALL_PREFIX, 'share/pkgcore')
CONFIG_PATH = join(DATA_PATH, 'config')
LIBDIR_PATH = join(INSTALL_PREFIX, 'lib/pkgcore')
EBD_PATH = join(LIBDIR_PATH, 'ebd')
INJECTED_BIN_PATH = ()
