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
External Codes interface
"""

from __future__ import annotations

import logging
import os.path
from importlib.resources import files as _res_files
from typing import IO, Any, TypedDict

import defusedxml.ElementTree as et

from pyx12.errors import EngineError


class CodesError(Exception):
    """Class for code modules errors."""


class _CodeSet(TypedDict):
    name: str | None
    dataele: str | None
    codes: frozenset[str | None]


class ExternalCodes:
    """
    Validates an ID against an external list of codes
    """

    codes: dict[str | None, _CodeSet]
    exclude_list: list[str]

    def __init__(self, base_path: str | None = None, exclude: str | None = None) -> None:
        """
        Initialize the external list of codes

        :param base_path: Override directory containing codes.xml.
            If None, uses package resource folder.
        :param exclude: comma-separated string of external code names to ignore.

        ``self.codes`` maps codeset_id to ``{'name', 'dataele', 'codes'}``.
        """
        logger = logging.getLogger("pyx12")
        self.codes = {}
        codes_file = "codes.xml"
        # ElementTree.parse accepts either text- or binary-mode streams; the
        # file source differs between override path and bundled package resource.
        code_fd: IO[Any]
        if base_path is not None:
            logger.debug(f"Looking for codes file '{codes_file}' in map_path '{base_path}'")
            code_fd = open(os.path.join(base_path, codes_file), encoding="utf-8")
        else:
            logger.debug(f"Looking for codes file '{codes_file}' in package resources")
            code_fd = _res_files("pyx12").joinpath("map", codes_file).open("rb")

        self.exclude_list = exclude.split(",") if exclude is not None else []
        with code_fd:
            parser = et.XMLParser(encoding="utf-8")
            for cElem in et.parse(code_fd, parser=parser).iter("codeset"):
                codeset_id = cElem.findtext("id")
                self.codes[codeset_id] = {
                    "name": cElem.findtext("name"),
                    "dataele": cElem.findtext("data_ele"),
                    "codes": frozenset(c.text for c in cElem.iterfind("version/code")),
                }

    def isValid(self, key: str | None, code: str | None, check_dte: str | None = None) -> bool:
        """
        Return True if code is in the codeset identified by key.
        """
        if not key:
            raise EngineError(f"bad key {key!r}")
        if key in self.exclude_list:
            return True
        if key not in self.codes:
            raise EngineError(f'External Code "{key}" is not defined')
        return code in self.codes[key]["codes"]

    def debug_print(self, count: int = 10) -> None:
        """Debug print first <count> codes for each codeset (alphabetical)."""
        for key in self.codes:
            print(sorted(self.codes[key]["codes"], key=lambda c: c or "")[:count])
