######################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

""" """

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import EngineError

isa_errors = (
    "000",
    "001",
    "002",
    "003",
    "004",
    "005",
    "006",
    "007",
    "008",
    "009",
    "010",
    "011",
    "012",
    "013",
    "014",
    "015",
    "016",
    "017",
    "018",
    "019",
    "020",
    "021",
    "022",
    "023",
    "024",
    "025",
    "026",
    "027",
    "028",
    "029",
    "030",
    "031",
)
seg_errors = ("1", "2", "3", "4", "5", "6", "7", "8")
ele_errors = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")


@dataclass(slots=True, frozen=True)
class ErrorItem:
    err_cde: str
    err_str: str


@dataclass(slots=True, frozen=True)
class ISAError(ErrorItem):
    def __post_init__(self) -> None:
        if self.err_cde not in isa_errors:
            raise EngineError('Invalid ISA level error code "%s"' % (self.err_cde))


@dataclass(slots=True, frozen=True)
class SegError(ErrorItem):
    err_val: str | None = None
    src_line: int | None = None

    def __post_init__(self) -> None:
        if self.err_cde not in seg_errors:
            raise EngineError('Invalid segment level error code "%s"' % (self.err_cde))


@dataclass(slots=True, frozen=True)
class EleError(ErrorItem):
    err_val: str | None = None
    refdes: str | None = None
    # map_node carries the element node ref for cursor materialization in the
    # err_handler tree. None means the wrapper should leave the cursor where
    # it was (used for composite-/seg-level errors that historically attach
    # to the prior cursor).
    map_node: Any = None

    def __post_init__(self) -> None:
        if self.err_cde not in ele_errors:
            raise EngineError('Invalid element level error code "%s"' % (self.err_cde))
