######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Composite interface - sub-element container.
"""

from __future__ import annotations

import sys
from typing import Any
from xml.etree.ElementTree import Element

from ..error_item import EleError
from ._base import _required_attr, x12_node
from ._element import element_if


def apply_composite_errors(child_node: composite_if, comp_data: Any, errh: Any) -> bool:
    """Drive a composite validation: run is_valid_errors, forward errors with
    cursor maintenance. Composite-level errors leave the cursor untouched
    (matches the historical behavior of attaching to the prior cursor);
    sub-element errors switch the cursor via add_ele(map_node) before
    forwarding."""
    ok, errors = child_node.is_valid_errors(comp_data)
    prev_cursor = None
    for e in errors:
        if e.map_node is not None and e.map_node is not prev_cursor:
            errh.add_ele(e.map_node)
            prev_cursor = e.map_node
        errh.ele_error(e.err_cde, e.err_str, e.err_val, e.refdes)
    return ok


############################################################
# Composite Interface
############################################################
class composite_if(x12_node):
    """
    Composite Node Interface
    """

    root: Any
    base_name: str
    refdes: str | None
    data_ele: str | None
    usage: str | None
    seq: int
    repeat: int

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        Get the values for this composite
        :param parent: parent node
        """
        x12_node.__init__(self)

        self.children = []
        self.root = root
        self.parent = parent
        self.path = ""
        self.base_name = "composite"

        self.id = elem.get("xid")
        self.refdes = elem.findtext("refdes") if elem.findtext("refdes") else self.id
        self.data_ele = elem.get("data_ele") if elem.get("data_ele") else elem.findtext("data_ele")
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.seq = int(_required_attr(elem, "seq"))
        if (r := elem.get("repeat")) is not None:
            self.repeat = int(r)
        elif (r := elem.findtext("repeat")) is not None:
            self.repeat = int(r)
        else:
            self.repeat = 1
        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")

        for e in elem.findall("element"):
            self.children.append(element_if(self.root, self, e))

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
            out += "  usage %s" % (self.usage)
        if self.seq:
            out += "  seq %i" % (self.seq)
        if self.refdes:
            out += "  refdes %s" % (self.refdes)
        out += "\n"
        return out

    def xml(self) -> None:
        """
        Sends an xml representation of the composite to stdout
        """
        sys.stdout.write("<composite>\n")
        for sub_elem in self.children:
            sub_elem.xml()
        sys.stdout.write("</composite>\n")

    def is_valid_errors(self, comp_data: Any) -> tuple[bool, list[EleError]]:
        """
        Pure validator: returns (ok, errors) without touching an error
        handler. Composite-level errors leave map_node unset (=None) so a
        wrapper iterating with cursor tracking attaches them to whatever
        cursor was last set — matches the historical behavior of the
        per-composite errh.ele_error calls.
        """
        valid = True
        errors: list[EleError] = []

        if (comp_data is None or comp_data.is_empty()) and self.usage in ("N", "S"):
            return True, []

        if self.usage == "R":
            good_flag = False
            if comp_data is not None:
                for sub_ele in comp_data:
                    if sub_ele is not None and len(sub_ele.get_value()) > 0:
                        good_flag = True
                        break
            if not good_flag:
                err_str = 'At least one component of composite "%s" (%s) is required' % (
                    self.name,
                    self.refdes,
                )
                return False, [EleError(err_cde="2", err_str=err_str, refdes=self.refdes)]

        if self.usage == "N" and not comp_data.is_empty():
            err_str = 'Composite "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            return False, [EleError(err_cde="5", err_str=err_str, refdes=self.refdes)]

        if len(comp_data) > self.get_child_count():
            err_str = 'Too many sub-elements in composite "%s" (%s)' % (self.name, self.refdes)
            errors.append(EleError(err_cde="3", err_str=err_str, refdes=self.refdes))
            valid = False
        for i in range(min(len(comp_data), self.get_child_count())):
            ok, sub_errors = self.get_child_node_by_idx(i).is_valid_errors(comp_data[i])
            valid &= ok
            errors += sub_errors
        for i in range(min(len(comp_data), self.get_child_count()), self.get_child_count()):
            if i < self.get_child_count():
                ok, sub_errors = self.get_child_node_by_idx(i).is_valid_errors(None)
                valid &= ok
                errors += sub_errors
        return valid, errors

    def is_composite(self) -> bool:
        """
        :rtype: boolean
        """
        return True
