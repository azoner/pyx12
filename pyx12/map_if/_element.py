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
from ..error_item import EleError
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

    def _ele_error(self, err_cde: str, err_str: str, err_val: str | None) -> EleError:
        return EleError(err_cde=err_cde, err_str=err_str, err_val=err_val, refdes=self.refdes)

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
        Backwards-compatible wrapper: drives the pure is_valid_errors and
        forwards the produced errors into the legacy err_handler API.
        """
        errh.add_ele(self)
        ok, errors = self.is_valid_errors(elem, type_list)
        for e in errors:
            errh.ele_error(e.err_cde, e.err_str, e.err_val, e.refdes)
        return ok

    def is_valid_errors(
        self, elem: Any, type_list: list[str | None] | None = None
    ) -> tuple[bool, list[EleError]]:
        """
        Pure validator: returns (ok, errors) without touching an error handler.
        """
        if type_list is None:
            type_list = []
        errors: list[EleError] = []

        if elem and elem.is_composite():
            err_str = 'Data element "%s" (%s) is an invalid composite' % (self.name, self.refdes)
            errors.append(self._ele_error("6", err_str, elem.__repr__()))
            return False, errors
        if elem is None or elem.get_value() == "":
            empty_errors = self._validate_when_empty()
            return (not empty_errors, empty_errors)
        if self.usage == "N" and elem.get_value() != "":
            err_str = 'Data element "%s" (%s) is marked as Not Used' % (self.name, self.refdes)
            errors.append(self._ele_error("10", err_str, None))
            return False, errors

        elem_val = elem.get_value()
        errors += self._validate_length(elem_val)
        ctrl_errors = self._validate_control_chars(elem_val)
        errors += ctrl_errors
        if ctrl_errors:
            # control char errors trump later checks
            return False, errors
        errors += self._validate_trailing_spaces(elem_val)
        errors += self._is_valid_code(elem_val)
        errors += self._validate_data_type(elem_val)
        if type_list:
            errors += self._validate_type_list(elem_val, type_list)
        errors += self._validate_regex(elem_val)
        return (not errors, errors)

    def _validate_when_empty(self) -> list[EleError]:
        if self.usage in ("N", "S"):
            return []
        if self.usage == "R" and (
            self.seq != 1 or not self.parent.is_composite() or self.parent.usage == "R"
        ):
            err_str = 'Mandatory data element "%s" (%s) is missing' % (self.name, self.refdes)
            return [self._ele_error("1", err_str, None)]
        return []

    def _validate_length(self, elem_val: str) -> list[EleError]:
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
        out: list[EleError] = []
        if elem_len < min_len:
            err_str = 'Data element "%s" (%s) is too short: len("%s") = %i < %i (min_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                min_len,
            )
            out.append(self._ele_error("4", err_str, elem_val))
        if elem_len > max_len:
            err_str = 'Data element "%s" (%s) is too long: len("%s") = %i > %i (max_len)' % (
                self.name,
                self.refdes,
                elem_val,
                elem_len,
                max_len,
            )
            out.append(self._ele_error("5", err_str, elem_val))
        return out

    def _validate_control_chars(self, elem_val: str) -> list[EleError]:
        res, bad_string = validation.contains_control_character(elem_val)
        if not res:
            return []
        err_str = 'Data element "%s" (%s), contains an invalid control character(%s)' % (
            self.name,
            self.refdes,
            bad_string,
        )
        return [self._ele_error("6", err_str, bad_string)]

    def _validate_trailing_spaces(self, elem_val: str) -> list[EleError]:
        data_ele = self._resolve_data_ele()
        if data_ele["data_type"] not in ("AN", "ID") or elem_val[-1] != " ":
            return []
        if len(elem_val.rstrip()) < data_ele["min_len"]:
            return []
        err_str = 'Data element "%s" (%s) has unnecessary trailing spaces. (%s)' % (
            self.name,
            self.refdes,
            elem_val,
        )
        return [self._ele_error("6", err_str, elem_val)]

    def _validate_data_type(self, elem_val: str) -> list[EleError]:
        data_type = self._resolve_data_ele()["data_type"]
        if validation.IsValidDataType(
            elem_val, cast(str, data_type), self.root.param.get("charset"), self.root.icvn
        ):
            return []
        if data_type in ("RD8", "DT", "D8", "D6"):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            return [self._ele_error("8", err_str, elem_val)]
        if data_type == "TM":
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            return [self._ele_error("9", err_str, elem_val)]
        err_str = 'Data element "%s" (%s) is type %s, contains an invalid character(%s)' % (
            self.name,
            self.refdes,
            data_type,
            elem_val,
        )
        return [self._ele_error("6", err_str, elem_val)]

    def _validate_type_list(
        self, elem_val: str, type_list: list[str | None]
    ) -> list[EleError]:
        valid_type = False
        for dtype in type_list:
            if dtype is not None:
                valid_type |= validation.IsValidDataType(
                    elem_val, dtype, self.root.param.get("charset")
                )
        if valid_type:
            return []
        if "TM" in type_list:
            err_str = 'Data element "%s" (%s) contains an invalid time (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            return [self._ele_error("9", err_str, elem_val)]
        if any(t in type_list for t in ("RD8", "DT", "D8", "D6")):
            err_str = 'Data element "%s" (%s) contains an invalid date (%s)' % (
                self.name,
                self.refdes,
                elem_val,
            )
            return [self._ele_error("8", err_str, elem_val)]
        return []

    def _validate_regex(self, elem_val: str) -> list[EleError]:
        if self.rec is None or self.rec.search(elem_val):
            return []
        err_str = 'Data element "%s" with a value of (%s)' % (self.name, elem_val)
        err_str += ' failed to match the regular expression "%s"' % (self.res)
        return [self._ele_error("7", err_str, elem_val)]

    def _is_valid_code(self, elem_val: str) -> list[EleError]:
        if not self._valid_codes_set and self.external_codes is None:
            return []
        if elem_val in self._valid_codes_set:
            return []
        if self.external_codes is not None and self.root.ext_codes.isValid(
            self.external_codes, elem_val
        ):
            return []
        err_str = "(%s) is not a valid code for %s (%s)" % (elem_val, self.name, self.refdes)
        return [self._ele_error("7", err_str, elem_val)]

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
