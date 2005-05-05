######################################################################
# Copyright (c) 2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Parses an x12 path

An x12 path is comprised of a sequence of loop identifiers, a segment
identifier, and element position, and a composite position.

/LOOP_1/LOOP_2
/LOOP_1/LOOP_2/SEG
/LOOP_1/LOOP_2/SEG02
/LOOP_1/LOOP_2/SEG02-1
SEG02-1
02-1
02

"""

import string

from pyx12.errors import *

class path:
    """
    Interface to an x12 path
    """

    def __init__(self, path_str):
        """
        @param path_str: 
        @type path_str: string
        
        """
        loop_list = path_str.split('/')
        if len(loop_list) == 0:
            return None
        
    def __len__(self):
        """
        @rtype: int
        """
        return 1

    def __repr__(self):
        """
        @rtype: string
        """
        return string.join(loop_list,'/')

    def format(self):
        """
        @rtype: string
        """
        return self.__repr__()

    def get_value(self):
        """
        @rtype: string
        """
        return self.value

    def getnodebypath(self, path):
        """
        """
        return None

