"""
Generic JSON table interface class
"""

from __future__ import annotations

import collections
import logging
from typing import Any


class JsonInterface:
    """
    Abstract the formatting of json objects
    Correctly format the @param = value pairs
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.fields: collections.OrderedDict[str, dict[str, Any]] = collections.OrderedDict()
        self.seg_count: int | None = None
        self.line_number: int | None = None
        self.parent_line_number: int | None = None

    def add_fields(self, fields: dict[str, dict[str, Any]]) -> None:
        for k, v in fields.items():
            self.fields[k] = v

    def add_date_range(self, paramname1: str, paramname2: str, value: str | None) -> None:
        (date1, date2) = JsonInterface._parse_rd8(value)
        self.add_string(paramname1, date1)
        self.add_string(paramname2, date2)

    def add_date(self, paramname: str, value: str | None) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is None:
            d: dict[str, Any] = {"name": paramname, "type": "datetime", "value": None}
        else:
            d = {
                "name": paramname,
                "type": "datetime",
                "value": JsonInterface._format_date_str(value),
            }
        self.fields[paramname] = d

    def add_time(self, paramname: str, value: str | None) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is None:
            d: dict[str, Any] = {"name": paramname, "type": "time", "value": None}
        else:
            d = {"name": paramname, "type": "time", "value": JsonInterface._format_time_str(value)}
        self.fields[paramname] = d

    def add_datetime(self, paramname: str, datevalue: str | None, timevalue: str | None) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if datevalue is None:
            d: dict[str, Any] = {"name": paramname, "type": "datetime", "value": None}
        else:
            if timevalue is None:
                self.add_date(paramname, datevalue)
                return
            else:
                datestr = JsonInterface._format_iso_date_str(datevalue)
                timestr = JsonInterface._format_time_str(timevalue)
                d = {"name": paramname, "type": "datetime", "value": f"{datestr}T{timestr}"}
        self.fields[paramname] = d

    def add_string(self, paramname: str, value: str | None) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is None:
            d: dict[str, Any] = {"name": paramname, "type": "string", "value": ""}
        else:
            d = {"name": paramname, "type": "string", "value": value}
        self.fields[paramname] = d

    def add_number(self, paramname: str, value: Any) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is not None and value != "":
            d = {"name": paramname, "type": "number", "value": float(value)}
            self.fields[paramname] = d

    def add_int(self, paramname: str, value: Any) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is not None and value != "":
            d = {"name": paramname, "type": "number", "value": int(value)}
            self.fields[paramname] = d

    def add_float(self, paramname: str, value: Any) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is not None and value != "":
            d = {"name": paramname, "type": "number", "value": float(value)}
            self.fields[paramname] = d

    def add_bool(self, paramname: str, value: bool | None) -> None:
        if paramname in self.fields:
            raise Exception(f"Param {paramname} exists")
        if value is not None and value in (True, False):
            d = {"name": paramname, "type": "bool", "value": bool(value)}
            self.fields[paramname] = d

    def _asdict(self) -> collections.OrderedDict[str, Any]:
        """
        Get an ordered dict from the fields and data
        """
        ret: collections.OrderedDict[str, Any] = collections.OrderedDict()
        for k, v in self.fields.items():
            if v["value"] is not None and v["value"] != "":
                ret[k] = v["value"]
        return ret

    def _escape_sql_string(self, val: str) -> str:
        return val.replace("'", "''")

    @staticmethod
    def _parse_rd8(date_str: str | None) -> tuple[str | None, str | None]:
        if date_str is None or len(date_str) != 17:
            return (None, None)
        return (
            JsonInterface._format_date_str(date_str[:8]),
            JsonInterface._format_date_str(date_str[9:]),
        )

    @staticmethod
    def _format_date_str(date_str: str | None) -> str | None:
        """
        Turn an X12 style date YYYYMMDD into an SQL style date YYYY-MM-DD HH:MM
        """
        if date_str is None or len(date_str) not in (8, 12):
            return None
        datestr = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        if len(date_str) == 12:
            datestr += f" {date_str[8:10]}:{date_str[10:12]}"
        return datestr

    @staticmethod
    def _format_iso_date_str(date_str: str | None) -> str | None:
        """
        Turn an X12 style date YYYYMMDD into an ISO style date YYYY-MM-DDTHH:MM
        """
        if date_str is None or len(date_str) not in (8, 12):
            return None
        datestr = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        if len(date_str) == 12:
            datestr += f"T{date_str[8:10]}:{date_str[10:12]}"
        return datestr

    @staticmethod
    def _format_time_str(val: str | None) -> str | None:
        """
        Turn an X12 style time HHMMSS into an SQL style time HH:MM:SS
        """
        if val is None:
            return None
        if len(val) == 4:
            return f"{val[:2]}:{val[2:4]}:00"
        if len(val) == 6:
            return f"{val[:2]}:{val[2:4]}:{val[4:]}"
        if len(val) == 8:
            return f"{val[:2]}:{val[2:4]}:{val[4:6]}.{val[6:]}"
        return None
