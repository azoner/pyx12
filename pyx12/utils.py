######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Common functions
"""

import string
from types import *
import pdb

# Intrapackage imports
import errors


def seg_str(seg, seg_term, ele_term, subele_term, eol=''):
    """
    Join a list of elements
    @param seg: List of elements
    @type seg: list[string|list[string]]
    @param seg_term: Segment terminator character
    @type seg_term: string
    @param ele_term: Element terminator character
    @type ele_term: string
    @param subele_term: Sub-element terminator character
    @type subele_term: string
    @param eol: End of line character
    @type eol: string
    @return: formatted segment
    @rtype: string
    """
    #if None in seg:
    #    logger.debug(seg)
    tmp = []
    for a in seg:
        if type(a) is ListType:
            tmp.append(string.join(a, subele_term))
        else:
            tmp.append(a)
    return '%s%s%s' % (string.join(tmp, ele_term), seg_term, eol)

def escape_html_chars(str_val):
    """
    Escape special HTML characters (& <>)
    @type str_val: string
    @return: formatted string
    @rtype: string
    """
    if str_val is None: 
        return None
    output = str_val
    output = output.replace('&', '&amp;')
    output = output.replace(' ', '&nbsp;')
    output = output.replace('>', '&gt;')
    output = output.replace('<', '&lt;')
    return output
