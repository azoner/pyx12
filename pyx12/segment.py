#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without
#        modification, are permitted provided that the following conditions are
#        met:
#
#        1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#        2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#        3. The name of the author may not be used to endorse or promote
#        products derived from this software without specific prior written
#        permission.
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#        IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#        DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#        STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#        IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#        POSSIBILITY OF SUCH DAMAGE.

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
    """Class element
    """

    def __init__(self, ele_str):
        """function element
        
        ele_str: string
        """
        self.value = ele_str
        
    def __len__(self):
        return 1

    def __repr__(self):
        """function __repr__
        
        returns string
        """
        return self.value

    def format(self):
        return self.value

    def get_value(self):
        return self.value

    def set_value(self, elem_str):
        self.value = elem_str

    def is_composite(self):
        return False
 
    def is_element(self):
        return True

    def is_empty(self):
        if self.value and self.value.strip() != '':
            return False
        else:
            return True

class composite:
    """Class element

       Can be a simple element or a composite
       A simple element is treated as a composite element with one sub-element.
    """
    # Attributes:
    
    # Operations
    def __init__(self, ele_str, subele_term=None):
        """function element
        
        ele_str: string
        
        returns void
        """
        self.subele_term = subele_term
        self.subele_term_orig = subele_term
        members = ele_str.split(self.subele_term)
        self.elements = []
        for elem in members:
            self.elements.append(element(elem))
        
    def __getitem__(self, idx):
        """function operator[]
        returns element instance for idx
        """
        return self.elements[idx]

    def __setitem__(self, idx, val):
        """function operator[]=
        1 based index
        [0] throws exception
        sets element value for idx
        """
        self.elements[idx] = val

    def __len__(self):
        """function length
        
        returns int
        """
        return len(self.elements)

    def __repr__(self):
        """function __repr__
        
        returns string
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
        if len(self.elements) > 1:
            return True
        else:
            return False
 
    def is_element(self):
        if len(self.elements) == 1:
            return True
        else:
            return False

    def is_empty(self):
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True


class segment:
    """Class segment

    """
    # Attributes:
    
    # Operations
    def __init__(self, seg_str, seg_term, ele_term, subele_term):
        """function segment
        
        returns void
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
        """function __repr__
        """
        return self.format(self.seg_term, self.ele_term, self.subele_term, '')
    
    def __getitem__(self, idx):
        """function operator[]
        returns element instance
        """
        return self.elements[idx]

    def __setitem__(self, idx, val):
        """function operator[]
        """
        self.elements[idx] = composite(val, self.subele_term)

    def __len__(self):
        return len(self.elements)
    
    def get_seg_id(self):
        """function get_seg_id
        
        returns string
        """
        return self.seg_id

    def get_value_by_ref_des(self, ref_des):
        if ref_des[:len(self.seg_id)] != self.seg_id:
            raise EngineError, 'Invalid ref_des: %s, seg_id: %s' % (ref_des, self.seg_id)
        rest = ref_des[len(self.seg_id):]
        dash = rest.find('-')
        if dash == -1:
            ele_idx = int(rest) - 1
            comp_idx = 0
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

    def set_eol(self, eol):
        self.eol = eol

    def format(self, seg_term=None, ele_term=None, subele_term=None, eol='\n'):
        if seg_term is None:
            seg_term = self.seg_term
        if ele_term is None:
            ele_term = self.ele_term
        if subele_term is None:
            subele_term = self.subele_term
        str_elems = []
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))
        return '%s%s%s%s%s' % (self.seg_id, ele_term, \
            string.join(str_elems, ele_term), \
            seg_term, eol)

    def format_ele_list(self, str_elems, subele_term=':'):
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))

    def is_empty(self):
        for ele in self.elements:
            if not ele.is_empty():
                return False
        return True
