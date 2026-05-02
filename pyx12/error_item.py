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


class ErrorItem:
    """
    Wrap an X12 validation error
    """

    err_cde: str
    err_str: str

    def __init__(self, err_type: str, err_cde: str, err_str: str) -> None:
        """
        :param err_type: At what level did the error occur
        :type err_type: string
        :param err_cde: Segment level error code
        :type err_cde: string
        :param err_str: Description of the error
        :type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def getErrCde(self) -> str:
        return self.err_cde

    def getErrStr(self) -> str:
        return self.err_str


class ISAError(ErrorItem):
    def __init__(self, err_cde: str, err_str: str) -> None:
        ErrorItem.__init__(self, "isa", err_cde, err_str)
        if self.err_cde not in isa_errors:
            raise EngineError('Invalid ISA level error code "%s"' % (self.err_cde))


class SegError(ErrorItem):
    err_val: str | None

    def __init__(self, err_cde: str, err_str: str, err_val: str | None = None) -> None:
        ErrorItem.__init__(self, "seg", err_cde, err_str)
        self.err_val = err_val
        if self.err_cde not in seg_errors:
            raise EngineError('Invalid segment level error code "%s"' % (self.err_cde))

    def getErrVal(self) -> str | None:
        return self.err_val


class EleError(ErrorItem):
    err_val: str | None
    ele_idx: int | None
    subele_idx: int | None

    def __init__(
        self,
        err_cde: str,
        err_str: str,
        ele_idx: int | None,
        subele_idx: int | None = None,
        err_val: str | None = None,
    ) -> None:
        ErrorItem.__init__(self, "ele", err_cde, err_str)
        self.err_val = err_val
        self.ele_idx = ele_idx
        self.subele_idx = subele_idx
        if self.err_cde not in ele_errors:
            raise EngineError('Invalid element level error code "%s"' % (self.err_cde))

    def getErrVal(self) -> str | None:
        return self.err_val

    def getEleIdx(self) -> int | None:
        return self.ele_idx

    def getSubeleIdx(self) -> int | None:
        return self.subele_idx
