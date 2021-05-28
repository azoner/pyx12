######################################################################
# Copyright (c)
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""pyx12 package exception classes.
"""

class XML_Reader_Error(Exception):
    """Class for XML Reader errors."""


class X12Error(Exception):
    """Base class for X12N format errors."""


class GSError(X12Error):
    """Errors in the GS or GE segements."""


class EngineError(Exception):
    """Base class for translation engine errors."""


class IterOutOfBounds(Exception):
    """Iterator is out of bounds"""


class IterDone(Exception):
    """Iterator is Complete"""


class IsValidError(Exception):
    """
    Exception for invalid X12 type errors
    """
    pass


class X12PathError(Exception):
    """
    Exception for invalid X12 path errors
    """
    pass
