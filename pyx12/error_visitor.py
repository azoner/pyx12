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


def ascii_only(value: str) -> str:
    """Replace non-ASCII codepoints with `?` (0x3F).

    The X12 997/999 acknowledgement output is ASCII-by-spec, but the input
    file may contain non-ASCII bytes that bubble through validation as
    `bad_value` payloads on element-level errors. The visitor must
    sanitize before writing them into IK404/AK4-04, otherwise the ack
    itself would carry the bad bytes (and the X12Writer's ASCII encode
    would crash on file output).

    `?` is in the X12 basic charset, so the substitute is always valid
    in any IK404/AK4-04 context."""
    return value.encode("ascii", errors="replace").decode("ascii")


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
