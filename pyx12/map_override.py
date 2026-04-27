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
Apply local overrides to the current map.
Overrides defined in a xml document.

NOT IMPLEMENTED
"""
from __future__ import annotations
from typing import Any


class map_override:
    """
    Apply local overrides to the current map. Overrides defined in a xml document.
    """

    def __init__(
        self,
        map_root: Any,
        override_file: str,
        icvn: str | None,
        vriic: str | None,
        fic: str | None,
    ) -> None:
        pass

    def _set_value(self, map_root: Any, path: str, variable: str, value: Any) -> None:
        pass

    def _append_value(self, map_root: Any, path: str, variable: str, value: Any) -> None:
        pass

    def _reset_list(self, map_root: Any, path: str, variable: str, value: Any) -> None:
        pass
