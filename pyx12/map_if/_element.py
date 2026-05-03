######################################################################
# Copyright (c)
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Element interface - leaf node validator.
"""

from __future__ import annotations

import re
import sys
from typing import Any, cast
from xml.etree.ElementTree import Element

from .. import validation
from ..dataele import _DataEle
from ..errors import EngineError
from ._base import _required_attr, x12_node


############################################################
# Element Interface
############################################################
class element_if(x12_node):
    """
    Element Interface
    """

    root: Any
    base_name: str
    valid_codes: list[str | None]
    _valid_codes_set: frozenset[str | None]
    external_codes: str | None
    rec: re.Pattern[str] | None
    refdes: str | None
    data_ele: str | None
    _data_ele: _DataEle | None
    usage: str | None
    seq: int
    max_use: str | None
    res: str | None

    def __init__(self, root: Any, parent: Any, elem: Element) -> None:
        """
        :param parent: parent node
        """
        x12_node.__init__(self)
        self.children = []
        self.root = root
        self.parent = parent
        self.base_name = "element"
        self.valid_codes = []
        self.external_codes = None
        self.rec = None

        self.id = elem.get("xid")
        self.refdes = self.id
        self.data_ele = elem.get("data_ele") if elem.get("data_ele") else elem.findtext("data_ele")
        # Eagerly cache the data element definition; a map that references an
        # undefined data_ele fails at validation time, matching legacy behavior.
        try:
            self._data_ele = (
                self.root.data_elements.get_by_elem_num(self.data_ele) if self.data_ele else None
            )
        except EngineError:
            self._data_ele = None
        self.usage = elem.get("usage") if elem.get("usage") else elem.findtext("usage")
        self.name = elem.get("name") if elem.get("name") else elem.findtext("name")
        self.seq = int(_required_attr(elem, "seq"))
        self.path = elem.get("seq") if elem.get("seq") else (elem.findtext("seq") or "")  # type: ignore[assignment]
        self.max_use = elem.get("max_use") if elem.get("max_use") else elem.findtext("max_use")
        self.res = elem.findtext("regex")
        try:
            if self.res is not None and self.res != "":
                self.rec = re.compile(self.res, re.S)
        except Exception:
            raise EngineError('Element regex "%s" failed to compile' % (self.res)) from None

        v = elem.find("valid_codes")
        if v is not None:
            self.external_codes = v.get("external")
            for c in v.findall("code"):
                self.valid_codes.append(c.text)
        # Parallel frozenset for O(1) membership checks. The list is kept
        # because callers (loop_if path disambiguation, map_if._get_icvn)
        # rely on a stable indexed order from the XML.
        self._valid_codes_set = frozenset(self.valid_codes)

    def debug_print(self) -> None:
        sys.stdout.write(self.__repr__())
        for node in self.children:
            node.debug_print()

    def __repr__(self) -> str:
        """
        :rtype: string
        """
        data_ele = self._resolve_data_ele()
        out = '%s "%s"' % (self.refdes, self.name)
        if self.data_ele:
            out += "  data_ele: %s" % (self.data_ele)
        if self.usage:
            out += "  usage: %s" % (self.usage)
        if self.seq:
            out += "  seq: %i" % (self.seq)
        out += "  %s(%i, %i)" % (data_ele["data_type"], data_ele["min_len"], data_ele["max_len"])
        if self.external_codes:
            out += "   external codes: %s" % (self.external_codes)
        out += "\n"
        return out

    def _resolve_data_ele(self) -> _DataEle:
        if self._data_ele is not None:
            return self._data_ele
        return cast(_DataEle, self.root.data_elements.get_by_elem_num(self.data_ele))

    def _error(self, errh: Any, err_str: str, err_cde: str, elem_val: str | None) -> None:
        """
        Forward the error to an error_handler
        """
        errh.ele_error(err_cde, err_str, elem_val, self.refdes)

    def _valid_code(self, code: str | None) -> bool:
        """
        Verify the x12 element value is in the given list of valid codes
        :return: True if found, else False
        :rtype: boolean
        """
        return code in self._valid_codes_set

    def get_parent(self) -> Any:
        """
        :return: ref to parent class instance
        """
        return self.parent

    def is_match(self) -> bool:
        """
        :return:
        :rtype: boolean
        """
        # match also by ID
        raise NotImplementedError("Override in sub-class")

    def is_valid(self, elem: Any, errh: Any, type_list: list[str | None] | None = None) -> bool:
        """
        Is this a valid element?

        :param elem: element instance
        :type elem: L{element<segment.Element>}
        :param errh: instance of error_handler
        :param type_list: Optional data/time type list
        :type type_list: list[string]
        :return: True if valid
        :rtype: boolean
        """
        if type_list is None:
            type_list = []
        errh.add_ele(self)

        if elem and elem.is_composite():
            err_str = 'Data element "%s" (%s) is an invalid composite' % (self.name, self.refdes)
            self._error(errh, err_str, "6", elem.__repr__())
            return False
        if elem is None or elem.get_value() == "":
            return self._validate_when_empty(errh)
        if self.usage == "N" and elem.get_value() != "":
            err_str = 'Data element "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            self._error(errh, err_str, "10", None)
            return False

        elem_val = elem.get_value()
        valid = self._validate_length(elem_val, errh)
        if not self._validate_control_chars(elem_val, errh):
            return False  # control char errors trump later checks
        valid &= self._validate_trailing_spaces(elem_val, errh)
        valid &= self._is_valid_code(elem_val, errh)
        valid &= self._validate_data_type(elem_val, errh)
        if type_list:
            valid &= self._validate_type_list(elem_val, type_list, errh)
        valid &= self._validate_regex(elem_val, errh)
        return bool(valid)

    def _validate_when_empty(self, errh: Any) -> bool:
        if self.usage in ("N", "S"):
            return True
        if self.usage == "R" and (
            self.seq != 1 or not self.parent.is_composite() or self.parent.usage == "R"
        ):
            err_str = 'Mandatory data element "%s" (%s) is missing' % (self.name, self.refdes)
            self._error(errh, err_str, "1", None)
            return False
        return True

    def _validate_length(self, elem_val: str, errh: Any) -> bool:
        data_ele = self._resolve_data_ele()
        data_type = data_ele["data_type"]
        min_len = data_ele["min_len"]
        max_len = data_ele["max_len"]
        # Numeric types ignore "-" and "." for length purposes.
        if data_type is not None and (data_type == "R" or data_type[0] == "N"):
            measured = elem_val.replace("-", "").replace(".", "")
        else:
            measured = elem_val
        elem_len = len(measured)
        valid = True
        if elem_len < min_len:
            err_str = 'Data element "%s" (%s) is too short: len("%s") = %i < %i (min_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                min_len,
            )
            self._error(errh, err_str, "4", elem_val)
            valid = False
        if elem_len > max_len:
            err_str = 'Data element "%s" (%s) is too long: len("%s") = %i > %i (max_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                max_len,
            )
            self._error(errh, err_str, "5", elem_val)
            valid = False
        return valid

    def _validate_control_chars(self, elem_val: str, errh: Any) -> bool:
        res, bad_string = validation.contains_control_character(elem_val)
        if not res:
            return True
        err_str = 'Data element "%s" (%s), contains an invalid control character(%s)' % (
            self.name,
            self.refdes,
            bad_string,
        )
        self._error(errh, err_str, "6", bad_string)
        return False

    def _validate_trailing_spaces(self, elem_val: str, errh: Any) -> bool:
        data_ele = self._resolve_data_ele()
        if data_ele["data_type"] not in ("AN", "ID") or elem_val[-1] != " ":
            return True
        if len(elem_val.rstrip()) < data_ele["min_len"]:
            return True
        err_str = 'Data element "%s" (%s) has unnecessary trailing spaces. (%s)' % (
            self.name,
            self.refdes,
            elem_val,
        )
        self._error(errh, err_str, "6", elem_val)
        return False

    def _validate_data_type(self, elem_val: str, errh: Any) -> bool:
        data_type = self._resolve_data_ele()["data_type"]
        if validation.IsValidDataType(
            elem_val, cast(str, data_type), self.root.param.get("charset"), self.root.icvn
        ):
            return True
        if data_type in ("RD8", "DT", "D8", "D6"):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "8", elem_val)
        elif data_type == "TM":
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "9", elem_val)
        else:
            err_str = 'Data element "%s" (%s) is type %s, contains an invalid character(%s)' % (
                self.name,
                self.refdes,
                data_type,
                elem_val,
            )
            self._error(errh, err_str, "6", elem_val)
        return False

    def _validate_type_list(self, elem_val: str, type_list: list[str | None], errh: Any) -> bool:
        valid_type = False
        for dtype in type_list:
            if dtype is not None:
                valid_type |= validation.IsValidDataType(
                    elem_val, dtype, self.root.param.get("charset")
                )
        if valid_type:
            return True
        if "TM" in type_list:
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "9", elem_val)
        elif any(t in type_list for t in ("RD8", "DT", "D8", "D6")):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            self._error(errh, err_str, "8", elem_val)
        return False

    def _validate_regex(self, elem_val: str, errh: Any) -> bool:
        if self.rec is None or self.rec.search(elem_val):
            return True
        err_str = 'Data element "%s" with a value of (%s)' % (self.name, elem_val)
        err_str += ' failed to match the regular expression "%s"' % (self.res)
        self._error(errh, err_str, "7", elem_val)
        return False

    def _is_valid_code(self, elem_val: str, errh: Any) -> bool:
        """
        :rtype: boolean
        """
        bValidCode = False
        if not self._valid_codes_set and self.external_codes is None:
            bValidCode = True
        if elem_val in self._valid_codes_set:
            bValidCode = True
        if self.external_codes is not None and self.root.ext_codes.isValid(
            self.external_codes, elem_val
        ):
            bValidCode = True
        if not bValidCode:
            err_str = "(%s) is not a valid code for %s (%s)" % (elem_val, self.name, self.refdes)
            self._error(errh, err_str, "7", elem_val)
            return False
        return True

    def get_data_type(self) -> str | None:
        return self._resolve_data_ele()["data_type"]

    @property
    def data_type(self) -> str | None:
        return self._resolve_data_ele()["data_type"]

    @property
    def min_len(self) -> int:
        return self._resolve_data_ele()["min_len"]

    @property
    def max_len(self) -> int:
        return self._resolve_data_ele()["max_len"]

    @property
    def data_element_name(self) -> str | None:
        return self._resolve_data_ele()["name"]

    def get_seg_count(self) -> None:
        """ """
        pass

    def is_element(self) -> bool:
        """
        :rtype: boolean
        """
        return True

    def get_path(self) -> str:
        """
        :return: path - XPath style
        :rtype: string
        """
        if self._fullpath:
            return self._fullpath
        # get enclosing loop
        parent_path = self.get_parent_segment().parent.get_path()
        # add the segment, element, and sub-element path
        self._fullpath = parent_path + "/" + (self.id or "")
        return self._fullpath

    def get_parent_segment(self) -> Any:
        # pop to enclosing loop
        p = self.parent
        while not p.is_segment():
            p = p.parent
        return p
