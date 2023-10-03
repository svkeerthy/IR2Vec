# Copyright (c) 2023, The Contributors of IR2Vec.
#
# Part of the IR2Vec project. This software is available under the BSD 4-Clause
# License. Please see LICENSE file in the top-level directory for more details.
#

### we have to find package before importing it else export LD_Lib path and LIB_path will not work.
from . import preparation
from IR2Vec.core import *

import pathlib as pl
import os, io

# version_regex = re.compile(r"^project\(ir2vec VERSION (?P<version>[^)]+)\)$")
VERSION = ""
with io.open("version.txt", encoding="utf-8") as f:
    VERSION = f.read().strip()

__version__ = VERSION
__copyright__ = "Copyright The Contributors of IR2Vec"
__license__ = "BSD 4-Clause License"

print("__version__: ", __version__)

setSeedEmbdPath(preparation.install_loc_pkg)
