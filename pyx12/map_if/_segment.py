######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Segment interface - per-segment validator and matcher.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from typing import Any
from xml.etree.ElementTree import Element

import pyx12.segment

from ..error_item import EleError
from ..errors import EngineError
from ..path import X12Path
from ..syntax import is_syntax_valid
from ._base import MAXINT, _required_attr, x12_node
from ._composite import composite_if
from ._element import element_if


def apply_segment_errors(node: segment_if, seg_data: pyx12.segment.Segment, errh: Any) -> bool:
    """Drive a segment validation: run is_valid_errors and forward errors
    with cursor maintenance. Seg-level errors (too many elements, syntax)
    leave map_node=None so they attach to the prior cursor; per-element
    errors carry map_node from the leaf and trigger add_ele(map_node)
    when the cursor changes."""
    ok, errors = node.is_valid_errors(seg_data)
    prev_cursor = None
    for e in errors:
        if e.map_node is not None and e.map_node is not prev_cursor:
            errh.add_ele(e.map_node)
            prev_cursor = e.map_node
        errh.ele_error(e.err_cde, e.err_str, e.err_val, e.refdes)
    return ok


class segment_if(x12_node):
    """
    Segment Interface
    """

    root: Any
    base_name: str
    _cur_count: int
    syntax: list[list[Any]]
    type: str | None
    usage: str | None
    pos: int
    max_use: str | None
    repeat: str | None
    end_tag: str | None

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        :param parent: parent node
        """

        x12_node.__init__(self)
        self.root = root
        self.parent = parent
        self.children = []
        self.base_name = "segment"
        self._cur_count = 0
        self.syntax = []

        self.id = elem.get("xid")
        self.path = self.id or ""
        self.type = elem.get("type")

        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.pos = int(_required_attr(elem, "pos"))
        self.max_use = elem.get("max_use") if elem.get("max_use") else elem.findtext("max_use")
        self.repeat = elem.get("repeat") if elem.get("repeat") else elem.findtext("repeat")

        self.end_tag = elem.get("end_tag") if elem.get("end_tag") else elem.findtext("end_tag")

        for s in elem.findall("syntax"):
            syn_list = self._split_syntax(s.text)
            if syn_list is not None:
                self.syntax.append(syn_list)

        children_map: dict[int, Element] = {}
        for e in elem.findall("element"):
            seq = int(_required_attr(e, "seq"))
            children_map[seq] = e

        for e in elem.findall("composite"):
            seq = int(_required_attr(e, "seq"))
            children_map[seq] = e

        for seq in sorted(children_map.keys()):
            if children_map[seq].tag == "element":
                self.children.append(element_if(self.root, self, children_map[seq]))
            elif children_map[seq].tag == "composite":
                self.children.append(composite_if(self.root, self, children_map[seq]))

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        out = '%s "%s"' % (self.id, self.name)
        if self.usage:
            out += "  usage: %s" % (self.usage)
        if self.pos:
            out += "  pos: %i" % (self.pos)
        if self.max_use:
            out += "  max_use: %s" % (self.max_use)
        out += "\n"
        return out

    def get_child_node_by_idx(self, idx: int) -> Any:
        """
        :param idx: zero based
        """
        if idx >= len(self.children):
            return None
        else:
            m = [c for c in self.children if c.seq == idx + 1]
            if len(m) == 1:
                return m[0]
            else:
                raise EngineError("idx %i not found in %s" % (idx, self.id))

    def get_child_node_by_ordinal(self, ord: int) -> Any:
        """
        Get a child element or composite by the X12 ordinal
        :param ord: one based element/composite index.  Corresponds to the map <seq> element
        :type ord: int
        """
        return self.get_child_node_by_idx(ord - 1)

    def getnodebypath2(self, path_str: str) -> Any:
        """
        Try x12 path

        :param path_str: remaining path to match
        :type path_str: string
        :return: matching node, or None is no match
        """
        x12path = X12Path(path_str)
        if x12path.empty():
            return None
        if x12path.ele_idx is None:
            return self  # matched segment only
        ele = self.get_child_node_by_ordinal(x12path.ele_idx)
        if x12path.subele_idx is None:
            return ele
        return ele.get_child_node_by_ordinal(x12path.subele_idx)

    def get_max_repeat(self) -> int:
        if self.max_use is None or self.max_use == ">1":
            return MAXINT
        return int(self.max_use)

    def get_parent(self) -> Any:
        """
        :return: ref to parent class instance
        :rtype: pyx12.x12_node
        """
        return self.parent

    def is_first_seg_in_loop(self) -> bool:
        """
        :rtype: boolean
        """
        if self is self.get_parent().get_first_seg():
            return True
        else:
            return False

    def is_match(self, seg: pyx12.segment.Segment) -> bool:
        """
        Is data segment given a match to this segment node?
        :param seg: data segment instance
        :return: boolean
        :rtype: boolean
        """
        if seg.get_seg_id() != self.id:
            return False
        key = self._resolve_unique_key_field(seg.get_seg_id(), with_qual=False)
        if key is None:
            return True
        child, ele_idx, subele_idx = key
        path = f"{ele_idx:02d}-{subele_idx}" if subele_idx else f"{ele_idx:02d}"
        return seg.get_value(path) in child._valid_codes_set

    def is_match_qual(
        self,
        seg_data: pyx12.segment.Segment,
        seg_id: str | None,
        qual_code: str | None,
    ) -> tuple[bool, str | None, int | None, int | None]:
        """
        Is segment id and qualifier a match to this segment node and to this particular segment data?
        :param seg_data: data segment instance
        :type seg_data: L{segment<segment.Segment>}
        :param seg_id: data segment ID
        :param qual_code: an ID qualifier code
        :return: (True if a match, qual_code, element_index, subelement_index)
        :rtype: tuple(boolean, string, int, int)
        """
        if seg_id != self.id:
            return (False, None, None, None)
        if qual_code is None:
            return (True, None, None, None)
        key = self._resolve_unique_key_field(seg_id, with_qual=True)
        if key is None:
            return (True, None, None, None)
        child, ele_idx, subele_idx = key
        path = f"{ele_idx:02d}-{subele_idx}" if subele_idx else f"{ele_idx:02d}"
        if qual_code in child._valid_codes_set and seg_data.get_value(path) == qual_code:
            return (True, qual_code, ele_idx, subele_idx)
        return (False, None, None, None)

    def _resolve_unique_key_field(
        self, seg_id: str | None, *, with_qual: bool
    ) -> tuple[Any, int, int | None] | None:
        """
        Locate the child node carrying this segment's qualifier (if any).

        Returns ``(validating_child, ele_idx, subele_idx_or_None)`` describing
        where to read the qualifier value from a data segment, or ``None`` if
        the segment has no recognizable qualifier field.

        ``with_qual=False`` (used by ``is_match``) accepts the AN-typed CTX
        composite as a valid qualifier carrier; ``with_qual=True`` (used by
        ``is_match_qual``) only honors ID-typed qualifier fields.
        """
        # Element at position 01 ??? the common case
        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and self.children[0].usage == "R"
            and len(self.children[0].valid_codes) > 0
        ):
            return (self.children[0], 1, None)
        # ENT-segment carries its qualifier at element 02 (820 special case)
        if (
            seg_id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
        ):
            return (self.children[1], 2, None)
        # CTX-segment can have an AN-typed composite at 01-1 (999 special case);
        # is_match_qual ignores this branch.
        if (
            not with_qual
            and seg_id == "CTX"
            and self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "AN"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return (self.children[0].children[0], 1, 1)
        # General ID-typed composite at 01-1
        if (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return (self.children[0].children[0], 1, 1)
        # HL-segment carries its qualifier at element 03
        if (
            seg_id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
        ):
            return (self.children[2], 3, None)
        return None

    def guess_unique_key_id_element(self) -> Any:
        """
        Some segments, like REF, DTP, and DTP are duplicated.  They are matched using the value of an ID element.
        Which element to use varies.  This function tries to find a good candidate.
        """
        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and len(self.children[0].valid_codes) > 0
        ):
            return self.children[0]
        # Special Case for 820
        elif (
            self.id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
        ):
            return self.children[1]
        elif (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
        ):
            return self.children[0].children[0]
        elif (
            self.id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
        ):
            return self.children[2]
        return None

    def get_unique_key_id_element(self, id_val: str) -> Any:
        """
        Some segments, like REF, DTP, and DTP are duplicated.  They are matched using the value of an ID element.
        Which element to use varies.  This function tries to find a good candidate, using a key value
        """

        if (
            self.children[0].is_element()
            and self.children[0].get_data_type() == "ID"
            and len(self.children[0].valid_codes) > 0
            and id_val in self.children[0]._valid_codes_set
        ):
            return self.children[0]
        # Special Case for 820
        elif (
            self.id == "ENT"
            and self.children[1].is_element()
            and self.children[1].get_data_type() == "ID"
            and len(self.children[1].valid_codes) > 0
            and id_val in self.children[1]._valid_codes_set
        ):
            return self.children[1]
        elif (
            self.children[0].is_composite()
            and self.children[0].children[0].get_data_type() == "ID"
            and len(self.children[0].children[0].valid_codes) > 0
            and id_val in self.children[0].children[0]._valid_codes_set
        ):
            return self.children[0].children[0]
        elif (
            self.id == "HL"
            and self.children[2].is_element()
            and len(self.children[2].valid_codes) > 0
            and id_val in self.children[2]._valid_codes_set
        ):
            return self.children[2]
        return None

    def is_segment(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def is_valid_errors(self, seg_data: pyx12.segment.Segment) -> tuple[bool, list[EleError]]:
        """
        Pure validator parallel to is_valid: returns (ok, errors) without
        touching an error handler. Seg-level errors (too many elements,
        too many sub-elements, syntax) leave map_node unset (=None);
        per-element errors carry map_node from the element validator so
        a cursor-tracking wrapper can replay add_ele/ele_error in the
        original order.
        """
        valid = True
        errors: list[EleError] = []
        child_count = self.get_child_count()

        if len(seg_data) > child_count:
            err_str = 'Too many elements in segment "%s" (%s). Has %i, should have %i' % (
                self.name,
                seg_data.get_seg_id(),
                len(seg_data),
                child_count,
            )
            ref_des = "%02i" % (child_count + 1)
            err_value = seg_data.get_value(ref_des)
            errors.append(EleError(err_cde="3", err_str=err_str, err_val=err_value, refdes=ref_des))
            valid = False

        dtype: list[str | None] = []
        type_list: list[str | None] = []
        for i in range(min(len(seg_data), child_count)):
            child_node = self.get_child_node_by_idx(i)
            if child_node.is_composite():
                ref_des = "%02i" % (i + 1)
                comp_data = seg_data.get(ref_des)
                subele_count = child_node.get_child_count()
                if seg_data.ele_len(ref_des) > subele_count and child_node.usage != "N":
                    subele_node = child_node.get_child_node_by_idx(subele_count + 1)
                    err_str = 'Too many sub-elements in composite "%s" (%s)' % (
                        subele_node.name,
                        subele_node.refdes,
                    )
                    err_value = seg_data.get_value(ref_des)
                    errors.append(
                        EleError(
                            err_cde="3",
                            err_str=err_str,
                            err_val=err_value,
                            refdes=ref_des,
                        )
                    )
                ok, comp_errors = child_node.is_valid_errors(comp_data)
                valid &= ok
                errors += comp_errors
            elif child_node.is_element():
                if (
                    i == 1
                    and seg_data.get_seg_id() == "DTP"
                    and seg_data.get_value("02") in ("RD8", "D8", "D6", "DT", "TM")
                ):
                    dtype = [seg_data.get_value("02")]
                if child_node.data_ele == "1250":
                    type_list.extend(child_node.valid_codes)
                ele_data = seg_data.get("%02i" % (i + 1))
                if i == 2 and seg_data.get_seg_id() == "DTP":
                    ok, ele_errors = child_node.is_valid_errors(ele_data, dtype)
                elif child_node.data_ele == "1251" and len(type_list) > 0:
                    ok, ele_errors = child_node.is_valid_errors(ele_data, type_list)
                else:
                    ok, ele_errors = child_node.is_valid_errors(ele_data)
                valid &= ok
                errors += ele_errors

        for i in range(min(len(seg_data), child_count), child_count):
            child_node = self.get_child_node_by_idx(i)
            ok, child_errors = child_node.is_valid_errors(None)
            valid &= ok
            errors += child_errors

        for syn in self.syntax:
            bResult, syn_err = is_syntax_valid(seg_data, syn)
            if not bResult:
                # When is_syntax_valid returns False, syn_err is the message string.
                assert syn_err is not None
                code = "10" if syn[0] == "E" else "2"
                errors.append(EleError(err_cde=code, err_str=syn_err, refdes=syn[1]))
                valid = False

        return valid, errors

    def _split_syntax(self, syntax: str | None) -> list[Any] | None:
        """
        Split a Syntax string into a list
        """
        if syntax is None or syntax[0] not in ["P", "R", "C", "L", "E"]:
            return None
        syn: list[Any] = [syntax[0]]
        for i in range(len(syntax[1:]) // 2):
            syn.append(int(syntax[i * 2 + 1 : i * 2 + 3]))
        return syn

    def get_cur_count(self) -> int:
        """
        :return: current count
        :rtype: int
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def incr_cur_count(self) -> None:
        raise DeprecationWarning("Moved to nodeCounter")

    def reset_cur_count(self) -> None:
        """
        Set cur_count of node to zero
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def set_cur_count(self, ct: int) -> None:
        raise DeprecationWarning("Moved to nodeCounter")

    def get_counts_list(self, ct_list: list[tuple[str, int]]) -> bool:
        """
        Build a list of (path, ct) of the current node and parents
        Gets the node counts to apply to another map
        :param ct_list: List to append to
        :type ct_list: list[(string, int)]
        """
        raise DeprecationWarning("Moved to nodeCounter")

    def loop_segment_iterator(self) -> Iterator[Any]:
        yield self
