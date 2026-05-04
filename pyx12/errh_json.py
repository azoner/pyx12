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
Generates a JSON document of validation errors.
Visitor - Visits an error_handler composite (issue #50).
"""

from __future__ import annotations

import json
from typing import Any, TextIO

import pyx12.error_visitor


class errh_json_visitor(pyx12.error_visitor.error_visitor):
    """
    Visit an error_handler composite. Accumulate a nested dict mirroring
    the ISA / GS / ST / segment / element hierarchy and dump it once as
    JSON in visit_root_post.

    Streaming JSON during the walk would require closing arrays mid-walk;
    the err_handler tree always fits in memory for any X12 document, so
    accumulate-then-dump is the right shape.
    """

    fd: TextIO
    indent: int | None
    doc: dict[str, Any]
    _stack: list[dict[str, Any]]
    _cur_seg: dict[str, Any] | None

    def __init__(self, fd: TextIO, indent: int | None = 2) -> None:
        """
        :param fd: target file
        :type fd: file descriptor
        :param indent: json.dump indent argument; pass None for compact output
        :type indent: int | None
        """
        self.fd = fd
        self.indent = indent
        self.doc = {"interchanges": []}
        self._stack = []
        self._cur_seg = None

    def visit_root_post(self, errh: Any) -> None:
        """
        :param errh: Error handler
        :type errh: L{error_handler.err_handler}
        """
        json.dump(self.doc, self.fd, indent=self.indent, default=str)

    def visit_isa_pre(self, err_isa: Any) -> None:
        """
        :param err_isa: ISA error node
        :type err_isa: L{error_handler.err_isa}
        """
        isa_dict: dict[str, Any] = {
            "isa_trn_set_id": err_isa.isa_trn_set_id,
            "ta1_req": err_isa.ta1_req,
            "orig_date": err_isa.orig_date,
            "orig_time": err_isa.orig_time,
            "cur_line": err_isa.get_cur_line(),
            "errors": [],
            "groups": [],
        }
        self.doc["interchanges"].append(isa_dict)
        self._stack.append(isa_dict)

    def visit_isa_post(self, err_isa: Any) -> None:
        isa_dict = self._stack[-1]
        isa_dict["errors"] = [
            {"err_cde": cde, "err_str": err_str} for (cde, err_str) in err_isa.errors
        ]
        self._stack.pop()

    def visit_gs_pre(self, err_gs: Any) -> None:
        gs_dict: dict[str, Any] = {
            "gs_control_num": err_gs.gs_control_num,
            "fic": err_gs.fic,
            "vriic": err_gs.vriic,
            "ack_code": err_gs.ack_code,
            "st_count_orig": err_gs.st_count_orig,
            "st_count_recv": err_gs.st_count_recv,
            "cur_line": err_gs.get_cur_line(),
            "errors": [],
            "transactions": [],
        }
        self._stack[-1]["groups"].append(gs_dict)
        self._stack.append(gs_dict)

    def visit_gs_post(self, err_gs: Any) -> None:
        gs_dict = self._stack[-1]
        gs_dict["errors"] = [
            {"err_cde": cde, "err_str": err_str} for (cde, err_str) in err_gs.errors
        ]
        self._stack.pop()

    def visit_st_pre(self, err_st: Any) -> None:
        st_dict: dict[str, Any] = {
            "trn_set_id": err_st.trn_set_id,
            "trn_set_control_num": err_st.trn_set_control_num,
            "vriic": err_st.vriic,
            "ack_code": err_st.ack_code,
            "cur_line": err_st.get_cur_line(),
            "errors": [],
            "segments": [],
        }
        self._stack[-1]["transactions"].append(st_dict)
        self._stack.append(st_dict)

    def visit_st_post(self, err_st: Any) -> None:
        st_dict = self._stack[-1]
        st_dict["errors"] = [
            {"err_cde": cde, "err_str": err_str} for (cde, err_str) in err_st.errors
        ]
        self._stack.pop()

    def visit_seg(self, err_seg: Any) -> None:
        seg_dict: dict[str, Any] = {
            "seg_id": err_seg.seg_id,
            "seg_count": err_seg.seg_count,
            "pos": err_seg.pos,
            "name": err_seg.name,
            "ls_id": err_seg.ls_id,
            "cur_line": err_seg.get_cur_line(),
            "errors": [
                {"err_cde": cde, "err_str": err_str, "err_val": err_val}
                for (cde, err_str, err_val) in err_seg.errors
            ],
            "elements": [],
        }
        self._stack[-1]["segments"].append(seg_dict)
        self._cur_seg = seg_dict

    def visit_ele(self, err_ele: Any) -> None:
        # err_ele.accept is only invoked from err_seg.accept (ISA / GS / ST
        # accept methods do not walk their .elements list), so a non-None
        # _cur_seg is guaranteed at this point.
        if self._cur_seg is None:
            return
        ele_dict: dict[str, Any] = {
            "ele_pos": err_ele.ele_pos,
            "subele_pos": err_ele.subele_pos,
            "repeat_pos": err_ele.repeat_pos,
            "ele_ref_num": err_ele.ele_ref_num,
            "name": err_ele.name,
            "errors": [
                {"err_cde": cde, "err_str": err_str, "err_val": err_val}
                for (cde, err_str, err_val) in err_ele.errors
            ],
        }
        self._cur_seg["elements"].append(ele_dict)
