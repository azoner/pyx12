######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Implements an interface to a x12 segment.

A segment is comprised of a segment identifier and a sequence of elements.
An element can be a simple element or a composite.  A simple element is 
treated as a composite element with one sub-element.

All indexing is zero based.
"""

import string

from pyx12.errors import *

class element:
    """
    Holds a simple element, which is just a simple string.
    """

    def __init__(self, ele_str):
        """
        @param ele_str: 1::2
        @type ele_str: string
        
        """
        self.value = ele_str
        
    def __len__(self):
        """
        @rtype: int
        """
        return 1

    def __repr__(self):
        """
        @rtype: string
        """
        return self.value

    def format(self):
        """
        @rtype: string
        """
        return self.value

    def get_value(self):
        """
        @rtype: string
        """
        return self.value

    def set_value(self, elem_str):
        self.value = elem_str

    def is_composite(self):
        """
        @rtype: boolean
        """
        return False
 
    def is_element(self):
        """
        @rtype: boolean
        """
        return True

    def is_empty(self):
        """
        @rtype: boolean
        """
        if self.value and self.value.strip() != '':
            return False
        else:
            return True

class composite:
    """
    Can be a simple element or a composite.
    A simple element is treated as a composite element with one sub-element.
    """
    # Attributes:
    
    # Operations
    def __init__(self, ele_str, subele_term=None):
        """
        @type ele_str: string
        """
        self.subele_term = subele_term
        self.subele_term_orig = subele_term
        members = ele_str.split(self.subele_term)
        self.elements = []
        for elem in members:
            self.elements.append(element(elem))
        
    def __getitem__(self, idx):
        """
        returns element instance for idx
        """
        return self.elements[idx]

    def __setitem__(self, idx, val):
        """
        1 based index
        [0] throws exception
        sets element value for idx
        """
        self.elements[idx] = val

    def __len__(self):
        """
        @rtype: int
        """
        return len(self.elements)

    def __repr__(self):
        """
        @rtype: string
        """
        return self.format(self.subele_term)

    def format(self, subele_term=None):
        if subele_term is None:
            subele_term = self.subele_term
        return '%s' % (string.join(map(element.__repr__, self.elements), subele_term))

    def get_value(self):
        if len(self.elements) == 1:
            return self.elements[0].get_value()
        else:
            raise IndexError, 'value of composite is undefined'

    def set_subele_term(self, subele_term):
        self.subele_term = subele_term
  
    def is_composite(self):
        """
        @rtype: boolean
        """
        if len(self.elements) > 1:
            return True
        else:
            return False
 
    def is_element(self):
        """
        @rtype: boolean
        """
        if len(self.elements) == 1:
            return True
        else:
            return False

    def is_empty(self):
        """
        @rtype: boolean
        """
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True


class segment:
    """
    Encapsulates a X12 segment.  Contains composites.
    """
    # Attributes:
    
    # Operations
    def __init__(self, seg_str, seg_term, ele_term, subele_term):
        """
        """
        self.seg_term = seg_term
        self.seg_term_orig = seg_term
        self.ele_term = ele_term
        self.ele_term_orig = ele_term
        self.subele_term = subele_term
        self.subele_term_orig = subele_term
        self.seg_id = None
        if seg_str and seg_str[-1] == seg_term:
            elems = string.split(seg_str[:-1], self.ele_term)
        else:
            elems = string.split(seg_str, self.ele_term)
        self.elements = []
        if elems:
            self.seg_id = elems[0]
        for ele in elems[1:]:
            if self.seg_id == 'ISA':
                #Special handling for ISA segment
                #guarantee subele_term will not be matched
                self.elements.append(composite(ele, ele_term))
            else:
                self.elements.append(composite(ele, subele_term))
    
    def __repr__(self):
        """
        @rtype: string
        """
        return self.format(self.seg_term, self.ele_term, self.subele_term)
    
    def __getitem__(self, idx):
        """
        returns element instance
        """
        return self.elements[idx]

    def __setitem__(self, idx, val):
        """
        """
        self.elements[idx] = composite(val, self.subele_term)

    def append(self, val):
        self.elements.append(composite(val, self.subele_term))

    def __len__(self):
        return len(self.elements)
    
    def get_seg_id(self):
        """
        @rtype: string
        """
        return self.seg_id

    def get_value_by_ref_des(self, ref_des):
        """
        """
        if ref_des[:len(self.seg_id)] != self.seg_id:
            raise EngineError, 'Invalid ref_des: %s, seg_id: %s' % (ref_des, self.seg_id)
        rest = ref_des[len(self.seg_id):]
        dash = rest.find('-')
        if dash == -1:
            ele_idx = int(rest) - 1
            #comp_idx = 0
            return self.elements[ele_idx].format()
        else:
            ele_idx = int(rest[:dash]) - 1
            comp_idx = int(rest[dash+1:]) - 1
            return self.elements[ele_idx][comp_idx].get_value()
    
    def set_seg_term(self, seg_term):
        self.seg_term = seg_term

    def set_ele_term(self, ele_term):
        self.ele_term = ele_term

    def set_subele_term(self, subele_term):
        self.subele_term = subele_term

#    def set_eol(self, eol):
#        self.eol = eol

    def format(self, seg_term=None, ele_term=None, subele_term=None):
        """
        @rtype: string
        """
        if seg_term is None:
            seg_term = self.seg_term
        if ele_term is None:
            ele_term = self.ele_term
        if subele_term is None:
            subele_term = self.subele_term
        str_elems = []
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))
        return '%s%s%s%s' % (self.seg_id, ele_term, \
            string.join(str_elems, ele_term), \
            seg_term)

    def format_ele_list(self, str_elems, subele_term=None):
        if subele_term is None:
            subele_term = self.subele_term
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))

    def is_empty(self):
        """
        @rtype: boolean
        """
        if len(self.elements) == 0:
            return True
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True
        
    def is_seg_id_valid(self):
        """
        Is the Segment identifier the correct length
        @rtype: boolean
        """
        if not self.seg_id or len(self.seg_id) < 2 or len(self.seg_id) > 3:
            return False
        else:
            return True
