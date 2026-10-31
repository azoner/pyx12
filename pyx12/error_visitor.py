######################################################################
# Copyright (c)
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Visitor - Visits an error_handler composite
"""

from __future__ import annotations

from typing import Any

_ACK_DELIMITERS = frozenset("~*:^")

# Ack elements that legitimately hold a delimiter or a composite:
# ISA11 / ISA16 are the repetition and sub-element separators themselves,
# IK4-01 / AK4-01 are the C030 position composite built from integers.
_ACK_PASSTHROUGH = frozenset({("ISA", 11), ("ISA", 16), ("IK4", 1), ("AK4", 1)})


def ack_safe(value: str) -> str:
    """Substitute `?` for anything that could forge ack structure.

    The ack writer is hardwired to `~ * : ^` regardless of the input file's
    delimiters, so any input value copied into the ack can carry them."""
    return "".join(
        "?" if ch in _ACK_DELIMITERS or not (0x20 <= ord(ch) < 0x7F) else ch for ch in value
    )


def sanitize_ack_segment(seg_data: Any) -> None:
    """Apply ack_safe to every element of an ack segment in place."""
    seg_id = seg_data.get_seg_id()
    for pos in range(1, len(seg_data) + 1):
        if (seg_id, pos) in _ACK_PASSTHROUGH:
            continue
        ref_des = f"{seg_id}{pos:02d}"
        value = seg_data.get_value(ref_des)
        if value:
            safe = ack_safe(value)
            if safe != value:
                seg_data.set(ref_des, safe)


class error_visitor:
    """ """

    def __init__(self, fd: Any) -> None:
        """
        Params:     fd - target file
        """
        pass

    def visit_root_pre(self, errh: Any) -> None:
        """
        :param errh: Error handler
        :type errh: L{error_handler.err_handler}
        """
        pass

    def visit_root_post(self, errh: Any) -> None:
        """
        :param errh: Error handler
        :type errh: L{error_handler.err_handler}
        """
        pass

    def visit_isa_pre(self, err_isa: Any) -> None:
        pass

    def visit_isa_post(self, err_isa: Any) -> None:
        """
        Params:     err_isa - error_isa instance
        """
        pass

    def visit_gs_pre(self, err_gs: Any) -> None:
        pass

    def visit_gs_post(self, err_gs: Any) -> None:
        """
        Params:     err_gs - error_gs instance
        """
        pass

    def visit_st_pre(self, err_st: Any) -> None:
        pass

    def visit_st_post(self, err_st: Any) -> None:
        """
        Params:     err_st - error_st instance
        """
        pass

    def visit_seg(self, err_seg: Any) -> None:
        """
        Params:     err_seg - error_seg instance
        """
        pass

    def visit_ele(self, err_ele: Any) -> None:
        """
        Params:     err_ele - error_ele instance
        """
        pass
