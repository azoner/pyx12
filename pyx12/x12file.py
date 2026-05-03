######################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Interface to an X12 data stream.
 - Efficiently handles large files.
 - Tracks end of explicit loops.
 - Tracks segment/line/loop counts.
 - Tracks some transaction specific counters:
   837 2400/LX
   837 HL tree
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from types import TracebackType
from typing import Literal, TextIO

# Intrapackage imports
import pyx12.errors
import pyx12.segment
from pyx12.rawx12file import RawX12File

# (kind, code, message, value, src_line)
_ErrTuple = tuple[str, str, str, str | None, int | None]
# (loop_type, control_number)
_LoopTuple = tuple[str, str | None]


class X12Base:
    """
    Base class of X12 Reader and X12 Writer
    Common X12 validation
    """

    err_list: list[_ErrTuple]
    loops: list[_LoopTuple]
    hl_stack: list[int]
    gs_count: int
    st_count: int
    hl_count: int
    seg_count: int
    cur_line: int
    isa_ids: list[str | None]
    gs_ids: list[str | None]
    st_ids: list[str | None]
    lx_count: int
    check_837_lx: bool
    isa_usage: str | None
    seg_term: str | None
    ele_term: str | None
    subele_term: str | None
    repetition_term: str | None

    def __init__(self) -> None:
        """
        Initialize the X12 file
        """
        self.err_list = []
        self.loops = []
        self.hl_stack = []
        self.gs_count = 0
        self.st_count = 0
        self.hl_count = 0
        self.seg_count = 0
        self.cur_line = 0
        self.isa_ids = []
        self.gs_ids = []
        self.st_ids = []
        self.lx_count = 0
        self.check_837_lx = False
        self.isa_usage = None
        self.seg_term = None
        self.ele_term = None
        self.subele_term = None
        self.repetition_term = None

    def Close(self) -> None:
        """
        Complete any outstanding tasks
        """
        pass

    def _parse_segment(self, seg_data: pyx12.segment.Segment) -> None:
        """
        Catch segment issues common to both readers and writers

        :param seg_data: Segment data instance
        :type seg_data: L{segment<segment.Segment>}
        """
        if seg_data.is_empty():
            err_str = f'Segment "{seg_data}" is empty'
            self._seg_error("8", err_str, None, src_line=self.cur_line + 1)
        if not seg_data.is_seg_id_valid():
            err_str = f'Segment identifier "{seg_data.get_seg_id()}" is invalid'
            self._seg_error("1", err_str, None, src_line=self.cur_line + 1)
        seg_id = seg_data.get_seg_id()
        if seg_id == "ISA":
            if len(seg_data) != 16:
                err_str = f"The ISA segment must have 16 elements ({seg_data})"
                raise pyx12.errors.X12Error(err_str)
            interchange_control_number = seg_data.get_value("ISA13")
            if interchange_control_number in self.isa_ids:
                err_str = "ISA Interchange Control Number "
                err_str += f"{interchange_control_number} not unique within file"
                self._isa_error("025", err_str)
            self.loops.append(("ISA", interchange_control_number))
            self.isa_ids.append(interchange_control_number)
            self.gs_count = 0
            self.gs_ids = []
            self.isa_usage = seg_data.get_value("ISA15")
        elif seg_id == "GS":
            group_control_number = seg_data.get_value("GS06")
            if group_control_number in self.gs_ids:
                err_str = "GS Interchange Control Number "
                err_str += f"{group_control_number} not unique within file"
                self._gs_error("6", err_str)
            self.gs_count += 1
            self.gs_ids.append(group_control_number)
            self.loops.append(("GS", group_control_number))
            self.st_count = 0
            self.st_ids = []
        elif seg_id == "ST":
            self.hl_stack = []
            self.hl_count = 0
            transaction_control_number = seg_data.get_value("ST02")
            if transaction_control_number in self.st_ids:
                err_str = "ST Interchange Control Number "
                err_str += f"{transaction_control_number} not unique within file"
                self._st_error("23", err_str)
            self.st_count += 1
            self.st_ids.append(transaction_control_number)
            self.loops.append(("ST", transaction_control_number))
            self.seg_count = 1
            self.hl_count = 0
        # elif seg_id == 'LS':
        #    self.seg_count += 1
        #    self.loops.append(('LS', seg_data.get_value('LS06')))
        # elif seg_id == 'LE':
        #    self.seg_count += 1
        #    del self.loops[-1]
        elif seg_id == "HL":
            self.hl_count += 1
            hl_count = seg_data.get_value("HL01")
            if self.hl_count != self._int(hl_count):
                # raise pyx12.errors.X12Error, \
                #   'My HL count %i does not match your HL count %s' \
                #    % (self.hl_count, seg[1])
                err_str = f"My HL count {self.hl_count:d} does not match your HL count {hl_count}"
                self._seg_error("HL1", err_str)
            if seg_data.get_value("HL02") != "":
                hl_parent = self._int(seg_data.get_value("HL02"))
                if hl_parent not in self.hl_stack:
                    err_str = f"HL parent ({hl_parent}) is not a valid parent"
                    self._seg_error("HL2", err_str)
                while self.hl_stack and hl_parent != self.hl_stack[-1]:
                    del self.hl_stack[-1]
            else:
                if len(self.hl_stack) != 0:
                    pass
                    # err_str = 'HL parent is blank, but stack not empty'
                    # self._seg_error('HL2', err_str)
            self.hl_stack.append(self.hl_count)
        elif self.check_837_lx and seg_id == "CLM":
            self.lx_count = 0
        elif self.check_837_lx and seg_id == "LX":
            self.lx_count += 1
            if seg_data.get_value("LX01") != f"{self.lx_count:d}":
                err_str = (
                    "Your 2400/LX01 Service Line Number {} does not match my count of {:d}".format(
                        seg_data.get_value("LX01"), self.lx_count
                    )
                )
                self._seg_error("LX", err_str)
        # count all regular segments
        if seg_id not in ("ISA", "IEA", "GS", "GE", "ST", "SE"):
            self.seg_count += 1
        self.cur_line += 1

    def pop_errors(self) -> list[_ErrTuple]:
        """
        Pop error list
        :return: List of errors
        """
        tmp = self.err_list
        self.err_list = []
        return tmp

    def _isa_error(self, err_cde: str, err_str: str) -> None:
        """
        :param err_cde: ISA level error code
        :type err_cde: string
        :param err_str: Description of the error
        :type err_str: string
        """
        self.err_list.append(("isa", err_cde, err_str, None, None))

    def _gs_error(self, err_cde: str, err_str: str) -> None:
        """
        :param err_cde: GS level error code
        :type err_cde: string
        :param err_str: Description of the error
        :type err_str: string
        """
        self.err_list.append(("gs", err_cde, err_str, None, None))

    def _st_error(self, err_cde: str, err_str: str) -> None:
        """
        :param err_cde: Segment level error code
        :type err_cde: string
        :param err_str: Description of the error
        :type err_str: string
        """
        self.err_list.append(("st", err_cde, err_str, None, None))

    def _seg_error(
        self,
        err_cde: str,
        err_str: str,
        err_value: str | None = None,
        src_line: int | None = None,
    ) -> None:
        """
        :param err_cde: Segment level error code
        :type err_cde: string
        :param err_str: Description of the error
        :type err_str: string
        """
        self.err_list.append(("seg", err_cde, err_str, err_value, src_line))

    def _int(self, str_val: str | None) -> int | None:
        """
        Converts a string to an integer
        :type str_val: string
        :return: Int value if successful, None if not
        :rtype: int
        """
        try:
            return int(str_val)  # type: ignore[arg-type]
        except (ValueError, TypeError):
            return None

    def get_isa_id(self) -> str | None:
        """
        Get the current ISA identifier

        :rtype: string
        """
        for loop in self.loops:
            if loop[0] == "ISA":
                return loop[1]
        return None

    def get_gs_id(self) -> str | None:
        """
        Get the current GS identifier

        :rtype: string
        """
        for loop in self.loops:
            if loop[0] == "GS":
                return loop[1]
        return None

    def get_st_id(self) -> str | None:
        """
        Get the current ST identifier

        :rtype: string
        """
        for loop in self.loops:
            if loop[0] == "ST":
                return loop[1]
        return None

    def get_ls_id(self) -> str | None:
        """
        Get the current LS identifier

        :rtype: string
        """
        for loop in self.loops:
            if loop[0] == "LS":
                return loop[1]
        return None

    def get_seg_count(self) -> int:
        """
        Get the current segment count

        :rtype: int
        """
        return self.seg_count

    def get_cur_line(self) -> int:
        """
        Get the current line

        :rtype: int
        """
        return self.cur_line

    def get_term(self) -> tuple[str | None, str | None, str | None, str, str | None]:
        """
        Get the original terminators

        :rtype: tuple(string, string, string, string)
        """
        return (self.seg_term, self.ele_term, self.subele_term, "\n", self.repetition_term)


class X12Reader(X12Base):
    """
    Read an X12 data file

    Errors found when reading the segment such as loop counting or ID
    errors can be retrieved using the pop_errors function
    """

    fd_in: TextIO
    need_to_close: bool
    raw: RawX12File
    icvn: str

    def __init__(self, src_file_obj: str | TextIO) -> None:
        """
        Initialize the file X12 file reader

        :param src_file_obj: absolute path of source file or an open,
            readable file object
        :type src_file_obj: string or open file object
        """
        self.need_to_close = False
        try:
            _ = src_file_obj.closed  # type: ignore[union-attr]
            self.fd_in = src_file_obj  # type: ignore[assignment]
        except AttributeError:
            if src_file_obj == "-":
                self.fd_in = sys.stdin
            else:
                self.fd_in = open(src_file_obj, encoding="ascii")  # type: ignore[arg-type]
                self.need_to_close = True
        X12Base.__init__(self)
        try:
            self.raw = RawX12File(self.fd_in)
        except pyx12.errors.X12Error:
            raise
        (seg_term, ele_term, subele_term, eol, repetition_term) = self.raw.get_term()
        self.seg_term = seg_term
        self.ele_term = ele_term
        self.subele_term = subele_term
        self.repetition_term = repetition_term
        self.icvn = self.raw.icvn

    def close(self) -> None:
        """
        Close the underlying file if X12Reader opened it itself.
        Idempotent.
        """
        if self.need_to_close and self.fd_in is not None:
            self.fd_in.close()
            self.need_to_close = False

    def __enter__(self) -> X12Reader:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    def _parse_segment(self, seg_data: pyx12.segment.Segment) -> None:
        """
        Catch segment issues

        :param seg_data: Segment data instance
        :type seg_data: L{segment<segment.Segment>}
        """
        X12Base._parse_segment(self, seg_data)
        seg_id = seg_data.get_seg_id()
        if seg_id == "IEA":
            if self.loops[-1][0] != "ISA":
                # Unterminated GS loop
                err_str = f"Unterminated Loop {self.loops[-1][0]}"
                self._isa_error("024", err_str)
                del self.loops[-1]
            if self.loops[-1][1] != seg_data.get_value("IEA02"):
                err_str = "IEA id={} does not match ISA id={}".format(
                    seg_data.get_value("IEA02"), self.loops[-1][1]
                )
                self._isa_error("001", err_str)
            if self._int(seg_data.get_value("IEA01")) != self.gs_count:
                err_str = "IEA count for IEA02={} is wrong".format(seg_data.get_value("IEA02"))
                self._isa_error("021", err_str)
            del self.loops[-1]
        elif seg_id == "GE":
            if self.loops[-1][0] != "GS":
                err_str = f"Unterminated segment {self.loops[-1][1]}"
                self._gs_error("3", err_str)
                del self.loops[-1]
            if self.loops[-1][1] != seg_data.get_value("GE02"):
                err_str = "GE id={} does not match GS id={}".format(
                    seg_data.get_value("GE02"), self.loops[-1][1]
                )
                self._gs_error("4", err_str)
            if self._int(seg_data.get_value("GE01")) != self.st_count:
                err_str = "GE count of {} for GE02={} is wrong. I count {}".format(
                    seg_data.get_value("GE01"), seg_data.get_value("GE02"), self.st_count
                )
                self._gs_error("5", err_str)
            del self.loops[-1]
        elif seg_id == "SE":
            se_trn_control_num = seg_data.get_value("SE02")
            if self.loops[-1][0] != "ST" or self.loops[-1][1] != se_trn_control_num:
                err_str = f"SE id={se_trn_control_num} does not match ST id={self.loops[-1][1]}"
                self._st_error("3", err_str)
            if self._int(seg_data.get_value("SE01")) != self.seg_count + 1:
                err_str = "SE count of {} for SE02={} is wrong. I count {}".format(
                    seg_data.get_value("SE01"), se_trn_control_num, self.seg_count + 1
                )
                self._st_error("4", err_str)
            del self.loops[-1]

    def __iter__(self) -> Iterator[pyx12.segment.Segment]:
        """
        Iterate over input segments
        """
        self.err_list = []
        for line in self.raw:
            # We have not yet incremented cur_line
            if line.startswith(" "):
                err_str = "Segment contains a leading space"
                self._seg_error("1", err_str, None, src_line=self.cur_line + 1)
                line = line.lstrip()
            if line[-1] == self.ele_term:
                err_str = "Segment contains trailing element terminators"
                self._seg_error("SEG1", err_str, None, src_line=self.cur_line + 1)
            seg_data = pyx12.segment.Segment(line, self.seg_term, self.ele_term, self.subele_term)  # type: ignore[arg-type]
            self._parse_segment(seg_data)
            yield seg_data
        # yield(None)

    def cleanup(self) -> None:
        """
        At EOF, check for missing loop trailers
        """
        if self.loops:
            for seg, id1 in self.loops:
                if seg == "ST":
                    err_str = 'Mandatory segment "Transaction Set Trailer" '
                    err_str += f"(SE={id1}) missing"
                    self._st_error("2", err_str)
                elif seg == "GS":
                    err_str = 'Mandatory segment "Functional Group Trailer" '
                    err_str += f"(GE={id1}) missing"
                    self._gs_error("3", err_str)
                elif seg == "ISA":
                    err_str = 'Mandatory segment "Interchange Control Trailer" '
                    err_str += f"(IEA={id1}) missing"
                    self._isa_error("023", err_str)
                # elif self.loops[-1][0] == 'LS':
                #    err_str = 'LS id=%s was not closed with a LE' % \
                #    (id1, self.loops[-1][1])


# Backward compatible name
X12file = X12Reader


class X12Writer(X12Base):
    """
    X12 file and stream writer
    """

    fd_out: TextIO
    need_to_close: bool
    eol: str

    def __init__(
        self,
        src_file_obj: str | TextIO,
        seg_term: str = "~",
        ele_term: str = "*",
        subele_term: str = "\\",
        eol: str = "\n",
        repetition_term: str = "^",
    ) -> None:
        """
        Initialize the file X12 file writer

        :param src_file_obj: absolute path of source file or an open,
            readable file object
        :type src_file_obj: string or open file object
        """
        self.need_to_close = False
        try:
            _ = src_file_obj.write  # type: ignore[union-attr]
            # isinstance(f, file)
            self.fd_out = src_file_obj  # type: ignore[assignment]
        except AttributeError:
            if src_file_obj == "-":
                self.fd_out = sys.stdout
            else:
                self.fd_out = open(src_file_obj, mode="w", encoding="ascii")  # type: ignore[arg-type, assignment]
                self.need_to_close = True
        X12Base.__init__(self)
        self.seg_term = seg_term
        self.ele_term = ele_term
        self.subele_term = subele_term
        self.repetition_term = repetition_term
        self.eol = eol

    def close(self) -> None:
        """
        Flush trailing loops and close the underlying file if X12Writer
        opened it itself. Idempotent.
        """
        self._popToLoop("ISA")
        X12Base.Close(self)
        if self.need_to_close and self.fd_out is not None:
            self.fd_out.close()
            self.need_to_close = False

    def Close(self) -> None:
        """Backwards-compatible alias for close()."""
        self.close()

    def __enter__(self) -> X12Writer:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    def Write(self, seg_data: pyx12.segment.Segment) -> None:
        """
        Write the segment to the stream given current separators

        :param seg_data: Segment data instance
        :type seg_data: L{segment<segment.Segment>}
        """
        self._parse_segment(seg_data)
        # If we have hit a loop closing segment, generate any missing, containing, closing segments
        # then generate this segment
        seg_id = seg_data.get_seg_id()
        if seg_id == "IEA":
            self._popToLoop("ISA")
        elif seg_id == "GE":
            self._popToLoop("GS")
        elif seg_id == "SE":
            self._popToLoop("ST")
        elif self.check_837_lx and seg_id == "LX":
            # Write our own LX counter
            seg_data.set("01", f"{self.lx_count:d}")
            self._write_segment(seg_data)
        elif seg_id == "ISA":
            # Replace terminators
            self._write_isa_segment(seg_data)
        else:
            self._write_segment(seg_data)

    def _close_loop(self, loop_type: str, loop_id: str | None) -> None:
        if loop_type == "ISA":
            self._close_iea(loop_id)
        elif loop_type == "GS":
            self._close_ge(loop_id)
        elif loop_type == "ST":
            self._close_se(loop_id)

    def _popToLoop(self, loop_type: str) -> None:
        """
        Move up the loop open loops, up to and including the given loop

        :param loop_type: The current ending loop
        :type loop_type: string
        """
        while len(self.loops) > 0 and self.loops[-1][0] != loop_type:
            loop = self.loops.pop()
            self._close_loop(loop[0], loop[1])
        if len(self.loops) > 0:
            loop = self.loops.pop()
            self._close_loop(loop[0], loop[1])

    def _close_iea(self, id: str | None) -> None:
        """
        Close a ISA/IEA loop, reset GS counter

        :param id: ISA loop ID
        :type id: string
        """
        seg_temp = self._get_trailer_segment("IEA", self.gs_count, id)
        self._write_segment(seg_temp)
        self.gs_count = 0

    def _close_ge(self, id: str | None) -> None:
        """
        Close a GS/GE loop, reset ST counter

        :param id: GS loop ID
        :type id: string
        """
        seg_temp = self._get_trailer_segment("GE", self.st_count, id)
        self._write_segment(seg_temp)
        self.st_count = 0

    def _close_se(self, id: str | None) -> None:
        """
        Close a ST/SE loop, reset segment counter

        :param id: ST loop ID
        :type id: string
        """
        seg_temp = self._get_trailer_segment("SE", self.seg_count + 1, id)
        self._write_segment(seg_temp)
        self.seg_count = 0

    def _write_segment(self, seg_data: pyx12.segment.Segment) -> None:
        """
        Write the given segment, using the current delimiters and end of line

        :param seg_data: segment to write
        :type seg_data: L{segment<segment.Segment>}
        """
        out = seg_data.format(self.seg_term, self.ele_term, self.subele_term) + self.eol
        # self.fd_out.write(out.decode('ascii'))
        self.fd_out.write(out)

    def _write_isa_segment(self, seg_data: pyx12.segment.Segment) -> None:
        """
        Write the ISA segment, using the current delimiters and end of line

        ISA*03*SENDER    *01*          *ZZ*SENDER         *ZZ*RECEIVER       *040608*1333*U*00401*000000288*0*P*:~
        ISA*03*SENDER    *01*          *ZZ*SENDER         *ZZ*RECEIVER       *040611*1333*^*00501*000000125*0*P*\\~

        :param seg_data: ISA segment to write
        :type seg_data: L{segment<segment.Segment>}
        """
        icvn = seg_data.get_value("ISA12")
        if icvn == "00501":
            seg_data.set("ISA11", self.repetition_term)  # type: ignore[arg-type]
        seg_data.set("ISA16", self.subele_term)  # type: ignore[arg-type]
        out = seg_data.format(self.seg_term, self.ele_term, self.subele_term) + self.eol
        # self.fd_out.write(out.decode('ascii'))
        self.fd_out.write(out)

    def _get_trailer_segment(
        self,
        seg_id: str,
        count: int,
        id: str | None,
    ) -> pyx12.segment.Segment:
        """
        Create a loop trailer segment, using the matching loop start and current count

        :param seg_id: end loop segment id
        :type seg_id: string
        :param count: count of loop members
        :type count: non-negative int
        :param id: loop id, should come from loop header
        :type id: string
        """
        ele_term = self.ele_term
        seg_str = f"{seg_id}{ele_term}{count:d}{ele_term}{id}"
        return pyx12.segment.Segment(
            seg_str,
            self.seg_term,  # type: ignore[arg-type]
            self.ele_term,  # type: ignore[arg-type]
            self.subele_term,  # type: ignore[arg-type]
        )
