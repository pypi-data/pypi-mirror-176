# isort: skip_file

# Has the side effect of applying patches
from . import _zipfile  # noqa: F401

from zipfile import (
    BadZipFile,
    BadZipfile,
    error,
    ZIP_STORED,
    ZIP_DEFLATED,
    ZIP_BZIP2,
    ZIP_LZMA,
    is_zipfile,
    ZipInfo,
    ZipFile,
    PyZipFile,
    LargeZipFile,
    Path,
)

from zipfile import ZIP_DEFLATED64  # type: ignore[attr-defined]  # noqa: F401

from zipfile_inflate64.version import __version__

__copyright__ = 'Copyright (C) 2022 Hiroshi Miura'

__all__ = [
    'BadZipFile',
    'BadZipfile',
    'error',
    'ZIP_STORED',
    'ZIP_DEFLATED',
    'ZIP_BZIP2',
    'ZIP_LZMA',
    'ZIP_DEFLATED64',
    'is_zipfile',
    'ZipInfo',
    'ZipFile',
    'PyZipFile',
    'LargeZipFile',
    'Path',
    '__version__',
    '__copyright__',
]
