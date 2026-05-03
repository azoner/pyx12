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
Loop and segment counter
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Mapping

import pyx12.path


class NodeCounter:
    """
    X12 Loop and Segment Node Counter
    """

    _dict: OrderedDict[pyx12.path.X12Path, int]

    def __init__(
        self,
        initialCounts: Mapping[str | pyx12.path.X12Path, int] | None = None,
    ) -> None:
        if initialCounts is None:
            initialCounts = {}
        self._dict = OrderedDict()
        # copy constructor
        for k, v in initialCounts.items():
            self._dict[NodeCounter.makeX12Path(k)] = v

    # @dump_args
    def reset_to_node(self, xpath: str | pyx12.path.X12Path) -> None:
        """
        Pop to node, deleting all child counts
        Keep count of xpath node
        """
        parent = NodeCounter.makeX12Path(xpath)
        child_keys = [x for x in self._dict.keys() if parent.is_child_path(x.format())]
        for k in child_keys:
            del self._dict[k]

    # @dump_args
    def increment(self, xpath: str | pyx12.path.X12Path) -> None:
        """
        Increment path count
        """
        k = NodeCounter.makeX12Path(xpath)
        if k in self._dict:
            self._dict[k] += 1
        else:
            self._dict[k] = 1

    # @dump_args
    def setCount(self, xpath: str | pyx12.path.X12Path, ct: int) -> None:
        """
        Set path count
        """
        k = NodeCounter.makeX12Path(xpath)
        self._dict[k] = ct

    def get_count(self, xpath: str | pyx12.path.X12Path) -> int:
        """
        Get path count
        """
        k = NodeCounter.makeX12Path(xpath)
        if k not in self._dict:
            return 0
        return self._dict[k]

    def getState(self) -> OrderedDict[pyx12.path.X12Path, int]:
        return self._dict

    @staticmethod
    def makeX12Path(xpath: str | pyx12.path.X12Path) -> pyx12.path.X12Path:
        if isinstance(xpath, pyx12.path.X12Path):
            return xpath
        else:
            return pyx12.path.X12Path(xpath)
