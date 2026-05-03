######################################################################
# Copyright (c) 2001-2011
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
X12 syntax validation functions
"""

from __future__ import annotations

from typing import Any

import pyx12.segment


def is_syntax_valid(
    seg_data: pyx12.segment.Segment,
    syn: list[Any],
) -> tuple[bool, str | None]:
    """
    Verifies the segment against the syntax
    :param seg_data: data segment instance
    :type seg_data: L{segment<segment.Segment>}
    :param syn: list containing the syntax type, and the indices of elements
    :type syn: list[string]
    :rtype: tuple(boolean, error string)
    """
    # handle intra-segment dependancies
    if len(syn) < 3:
        err_str = f"Syntax string must have at least two comparators {syntax_str(syn)}"
        return (False, err_str)

    syn_code = syn[0]
    syn_idx = [int(s) for s in syn[1:]]

    if syn_code == "P":
        count = 0
        for s in syn_idx:
            _val = seg_data.get_value(f"{s:02d}")
            if len(seg_data) >= s and _val != "":
                count += 1
        if count != 0 and count != len(syn_idx):
            err_str = f"Syntax Error ({syntax_str(syn)}): If any of {syntax_ele_id_str(seg_data.get_seg_id(), syn_idx)} is present, then all are required"
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == "R":
        count = 0
        for s in syn_idx:
            _val = seg_data.get_value(f"{s:02d}")
            if len(seg_data) >= s and _val != "":
                count += 1
        if count == 0:
            err_str = f"Syntax Error ({syntax_str(syn)}): At least one element is required"
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == "E":
        count = 0
        for s in syn_idx:
            _val = seg_data.get_value(f"{s:02d}")
            if len(seg_data) >= s and _val != "":
                count += 1
        if count > 1:
            err_str = "Syntax Error (%s): At most one of %s may be present" % (
                syntax_str(syn),
                syntax_ele_id_str(seg_data.get_seg_id(), syn_idx),
            )
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == "C":
        # If the first is present, then all others are required
        if len(seg_data) >= syn_idx[0] and seg_data.get_value("%02i" % (syn_idx[0])) != "":
            count = 0
            for s in syn_idx[1:]:
                _val = seg_data.get_value(f"{s:02d}")
                if len(seg_data) >= s and _val != "":
                    count += 1
            if count != len(syn_idx) - 1:
                if len(syn_idx[1:]) > 1:
                    verb = "are"
                else:
                    verb = "is"
                err_str = "Syntax Error (%s): If %s%02i is present, then %s %s required" % (
                    syntax_str(syn),
                    seg_data.get_seg_id(),
                    syn_idx[0],
                    syntax_ele_id_str(seg_data.get_seg_id(), syn_idx[1:]),
                    verb,
                )
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    elif syn_code == "L":
        if len(seg_data) > syn_idx[0] - 1 and seg_data.get_value("%02i" % (syn_idx[0])) != "":
            count = 0
            for s in syn_idx[1:]:
                _val = seg_data.get_value(f"{s:02d}")
                if len(seg_data) >= s and _val != "":
                    count += 1
            if count == 0:
                err_str = "Syntax Error (%s): If %s%02i is present, then at least one of " % (
                    syntax_str(syn),
                    seg_data.get_seg_id(),
                    syn_idx[0],
                )
                err_str += syntax_ele_id_str(seg_data.get_seg_id(), syn_idx[1:])
                err_str += " is required"
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    # raise EngineError
    return (False, "Syntax Type %s Not Found" % (syntax_str(syn)))


def syntax_str(syntax: list[Any]) -> str:
    """
    :rtype: string
    """
    output: str = str(syntax[0])
    for i in syntax[1:]:
        output += f"{int(i):02d}"
    return output


def syntax_ele_id_str(seg_id: str | None, ele_pos_list: list[int]) -> str:
    """
    :rtype: string
    """
    output = ""
    output += f"{seg_id}{ele_pos_list[0]:02d}"
    for i in range(len(ele_pos_list) - 1):
        if i == len(ele_pos_list) - 2:
            output += f" or {seg_id}{ele_pos_list[i + 1]:02d}"
        else:
            output += f", {seg_id}{ele_pos_list[i + 1]:02d}"
    return output
