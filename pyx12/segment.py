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

import string

class element:
    """Class element

       Can be a simple element or a composite
       INDEXING IS 1 BASED
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
        self.elements = ele_str.split(self.subele_term)
        
    def __getitem__(self, idx):
        """function operator[]
        1 based index
        [0] throws exception
        returns element value for idx
        """
        if idx == 0:
            raise IndexError, 'element index out of range'
        elif idx < 0:
            return self.elements[idx]
        else:
            return self.elements[idx-1]

    def __setitem__(self, idx, val):
        """function operator[]=
        1 based index
        [0] throws exception
        sets element value for idx
        """
        if idx == 0:
            raise IndexError, 'list index out of range'
        elif idx < 0:
            i = idx
        else:
            i = idx - 1
        self.elements[i] = val

    def __len__(self):
        """function length
        
        returns int
        """
        return len(self.elements)

    def __repr__(self):
        """function __repr__
        
        returns string
        """
        return '%s' % (string.join(self.elements, self.subele_term))

    def format(self, subele_term=':'):
        return '%s' % (string.join(self.elements, subele_term))

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

class segment:
    """Class segment

        INDEXING IS 1 BASED
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
            self.elements.append(element(ele, subele_term))
    
    def __repr__(self):
        """function __repr__
        """
        str_elems = []
        for ele in self.elements:
            str_elems.append(ele.__repr__())
        return '%s%s%s%s' % (self.seg_id, self.ele_term, \
            string.join(str_elems, self.ele_term), \
            self.seg_term)
    
    def __getitem__(self, idx):
        """function operator[]
        1 based index
        [0] throws exception
        returns base element instance
        """
        if idx == 0:
            raise IndexError, 'list index out of range'
        elif idx < 0:
            return self.elements[idx]
        else:
            return self.elements[idx-1]

    def __setitem__(self, idx, val):
        """function operator[]
        1 based index
        [0] throws exception
        """
        if idx == 0:
            raise IndexError, 'list index out of range'
        elif idx < 0:
            i = idx
        else:
            i = idx - 1
        self.elements[i] = element(val, self.subele_term)

    def __len__(self):
        return len(self.elements)
    
    def get_seg_id(self):
        """function get_seg_id
        
        returns string
        """
        return self.seg_id
    
    def set_seg_term(self, seg_term):
        self.seg_term = seg_term

    def set_ele_term(self, ele_term):
        self.ele_term = ele_term

    def set_subele_term(self, subele_term):
        self.subele_term = subele_term

    def set_eol(self, eol):
        self.eol = eol

    def format(self, seg_term, ele_term, subele_term, eol='\n'):
        str_elems = []
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))
        return '%s%s%s%s%s' % (self.seg_id, ele_term, \
            string.join(str_elems, ele_term), \
            seg_term, eol)

    def format_ele_list(self, str_elems, subele_term=':'):
        for ele in self.elements:
            str_elems.append(ele.format(subele_term))
