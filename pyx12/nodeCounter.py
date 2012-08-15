######################################################################
# Copyright Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id: map_if.py 1487 2011-10-22 04:52:02Z johnholland $

"""
Loop and segment counter
"""
#import collections
import pyx12.path


class NodeCounter(object):
    """
    X12 Loop and Segment Node Counter
    """
    def __init__(self, initialCounts={}):
        self._dict = {}
# copy constructor
        for k, v in initialCounts.items():
            if isinstance(k, pyx12.path.X12Path):
                self._dict[k] = v
            else:
                self._dict[pyx12.path.X12Path(k)] = v
# deque, Counter, OrderedDict
        #self.nodes = OrderedDict()

    def reset_to_node(self, xpath):
        """
        Pop to node, deleting all child counts
        """
        if xpath in self._dict:
            del self._dict[xpath]

    def increment(self, xpath):
        """
        Increment path count
        """
        if xpath in self._dict:
            self._dict[xpath] += 1
        else:
            self._dict[xpath] = 1

    def setCount(self, xpath, ct):
        """
        Set path count
        """
        self._dict[xpath] = ct

    def get_count(self, xpath):
        """
        Get path count
        """
        if xpath not in self._dict:
            return 0
            #raise Exception, 'Unknown xpath in counter: %s' % (xpath)
        return self._dict[xpath]
