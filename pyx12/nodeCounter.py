######################################################################
# Copyright (c) 2011-2012 Kalamazoo Community Mental Health Services,
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

class NodeCounter(object):
    """
    X12 Loop and Segment Node Counter
    """
    def __init__(self, counts={}):
# can default initial count state
# copy constructor
        self.stack = counts
# deque, Counter, OrderedDict
        #self.nodes = OrderedDict()

    def reset_to_node(self, xpath):
        """
        Pop to node, deleting all child counts
        """
        if xpath in self.stack:
            del self.stack[xpath]

    def increment(self, xpath):
        if xpath in self.stack:
            self.stack[xpath] += 1
        else:
            self.stack[xpath] = 1
    
    def get_count(self, xpath):
        if xpath not in self.stack:
            raise Exception, 'Unknown xpath in counter: %s' % (xpath)
        return self.stack[xpath]
