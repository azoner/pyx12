#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without modification,
#        are permitted provided that the following conditions are met:
#
#        1. Redistributions of source code must retain the above copyright notice, this list
#           of conditions and the following disclaimer.
#
#        2. Redistributions in binary form must reproduce the above copyright notice, this
#           list of conditions and the following disclaimer in the documentation and/or other
#           materials provided with the distribution.
#
#        3. The name of the author may not be used to endorse or promote products derived
#           from this software without specific prior written permission.
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#        MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#        EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
#        OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#        THE POSSIBILITY OF SUCH DAMAGE.


import string

class base_element:
    """Abstract class base_element
    """
    def __init__(self):
        """function base_element
        
        ele_str: string
        
        returns void
        """
        raise NotImplementedError()
    
    def __len__(self):
        """function length
        
        returns int
        """
        raise NotImplementedError()
    
    def __repr__(self):
        """function __repr__
        
        returns 
        """
        raise NotImplementedError()
    

class composite(base_element):
    """Class composite
    """
    def __init__(self, ele_str, subele_term):
        """function composite
        
        ele_str: string
        subele_term: char
        
        returns void
        """

        self.subele_term = subele_term
        self.elements = ele_str.split(self.subele_term)
    
    def __len__(self):
        """function length
        
        returns int
        """
        return len(self.elements)
    
    def __repr__(self):
        """function __repr__
        
        returns 
        """
        return '%s' % (string.join(self.elements, self.subele_term))
    

class element(base_element):
    """Class element
    """
    # Attributes:
    
    # Operations
    def __init__(self, ele_str):
        """function element
        
        ele_str: string
        
        returns void
        """
        self.ele_val = ele_str
    
    def __len__(self):
        """function length
        
        returns int
        """
        return 1
    
    def __repr__(self):
        """function __repr__
        
        returns 
        """
        return self.ele_val


class segment:
    """Class segment
    """
    # Attributes:
    
    # Operations
    def __init__(self, seg_str, seg_term, ele_term, subele_term, eol='\n'):
        """function segment
        
        returns void
        """
        self.seg_term = seg_term
        self.ele_term = ele_term
        self.eol = eol
        elems = string.split(seg_str, self.ele_term)
        self.elements = []
        self.seg_id = elems[0]
        for ele in elems[1:]:
            if ele.find(subele_term) != -1: # Split composite
                self.elements.append(composite(ele, subele_term))
            else:
                self.elements.append(element(ele))
    
    def __repr__(self):
        """function __repr__
        """
        str_elems = []
        for ele in self.elements:
            str_elems.append(ele.__repr__())
        return '%s%s%s%s%s' % (self.seg_id, self.ele_term, \
            string.join(str_elems, self.ele_term), \
            self.seg_term, self.eol)
    
    def __getitem__(self, idx):
        """function operator[]
        1 based index
        [0] throws exception
        returns element
        """
        if idx == 0:
            raise IndexError, 'list index out of range'
        return self.elements[idx-1]

    def __len__(self):
        return len(self.elements)
    
    def get_seg_id(self):
        """function get_seg_id
        
        returns string
        """
        return self.seg_id
    

