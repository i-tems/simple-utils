"""
simple-utils: A collection of simple Python utilities.
"""

from . import datetime_utils
from . import string_utils
from . import file_utils
from . import decorators

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0"

__all__ = ["datetime_utils", "string_utils", "file_utils", "decorators"]
