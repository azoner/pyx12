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


"""
Interface to X12 Errors
"""

import logging
#import os
#import sys
#import string
from types import *

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"

#class error_node:
#    def __init__(self)

logger = logging.getLogger('pyx12')

class err_handler:
    """
    Name:   err_handler
    Desc:   
    """
    def __init__(self):
        """
        Name:   __init__
        Desc:    
        Params: 
        Note:      
        """
        #self.x12_src = x12_src
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()

        self.id = 'ROOT'
        #self.isa_loop_count = 0
        self.children = []
        self.cur_node = self
        self.cur_isa_node = None
        self.cur_gs_node = None
        self.cur_st_node = None
        self.cur_seg_node = None
        self.cur_ele_node = None

    def accept(self, visitor):
        """
        Class:      err_root
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_root(self)

    def get_id(self):
        return self.id

    def add_isa_loop(self, seg, src):
        self.children.append(err_isa(self, seg, src))
        self.cur_isa_node = self.children[-1]
        
    def add_gs_loop(self, seg, src):
        parent = self.cur_isa_node
        parent.children.append(err_gs(parent, seg, src))
        self.cur_gs_node = parent.children[-1]
        
    def add_st_loop(self, seg, src):
        parent = self.cur_gs_node
        parent.children.append(err_st(parent, seg, src))
        self.cur_st_node = parent.children[-1]
        
    def add_seg(self, seg, src):
        parent = self.cur_st_node
        if parent.children[-1].err_count() == 0:
            del parent.children[-1]
        parent.children.append(err_seg(parent, seg, src))
        self.cur_seg_node = parent.children[-1]
        
    def add_ele(self, ele_pos, ele_ref_num, subele_pos=None):
        parent = self.cur_seg_node
        if parent.children[-1].err_count() == 0:
            del parent.children[-1]
        parent.children.append(err_ele(parent, ele_pos, ele_ref_num, subele_pos))
        self.cur_ele_node = parent.children[-1]
        
    def isa_error(self, err_cde, err_str):
        self.cur_isa_node.add_error(err_cde, err_str)

    def gs_error(self, err_cde, err_str):
        self.cur_gs_node.add_error(err_cde, err_str)
        
    def st_error(self, err_cde, err_str):
        self.cur_st_node.add_error(err_cde, err_str)
        
    def seg_error(self, err_cde, err_str):
        self.cur_seg_node.add_error(err_cde, err_str)
        
    def ele_error(self, err_cde, err_str, bad_value, pos, data_ele):
        self.cur_ele_node.add_error(err_cde, err_str, bad_value, pos, data_ele)

    def close_isa_loop(self, seg, sec, gs_count):
        self.cur_isa_node.close(seg, sec, gs_count)
        
    def find_node(self, type):
        """
        Find the last node of a type
        """
        new_node = self.cur_node
        node_order = {'ROOT': 1, 'ISA': 2, 'GS': 3, 'ST': 4, 'SEG': 5, 'ELE': 6}
        while node_order[type] > new_node[new_node.get_id()]:
            new_node = new_node.get_parent()
        #walk error tree to find place to append
        #if type == 'ISA':
        #return node

    def update_node(self, obj):
        self.children[-1].update_node(obj)

    def _get_last_child(self):
        if len(self.children) != 0:
            #logger.debug(obj)
            return self.children[-1]
        else:
            return None
    
         

class err_node:
    def __init__(self, parent): 
        #obj = {'id': '', 'seg': seg, 'src_id': src.get_id()}
#        self.seg = obj['seg']
#        self.src_id =  obj['src_id']
#        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.src_id
#        self.cur_line = cur_line
#        self.isa_id = isa_id
#        self.gs_id = gs_id
#        self.st_id = st_id
#        self.ls_id = ls_id
#        self.seg_count = seg_count
        self.id = None

    def accept(self, visitor):
        pass
        
    def add_error(self, err):
        pass
        
    def update_node(self, obj):
        pass

    def get_id(self):
        return self.id

    def get_parent(self):
        return self.parent

    def _get_last_child(self):
        if len(self.children) != 0:
            #logger.debug(obj)
            return self.children[-1]
        else:
            return None
   

class err_isa(err_node):
    """
    Name:    err_isa
    Desc:    Holds source ISA loop errors
    """

    def __init__(self, parent, seg, src):
        """
        Class:      err_isa
        Name:       __init__
        Desc:    
        Params:     x12_src - instance of x12file
        """
        #err_node.__init__(self, obj)

        self.seg = seg
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.isa_id = isa_id
        self.cur_line = cur_line
        
        self.isa_trn_set_id = self.isa_id
        self.id = 'ISA'

        self.parent = parent
        self.children = []
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_isa
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_isa(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_isa
        Name:       add_error
        Desc:    
        Params:     
        """
        self.errors.append((err_cde, err_str))
        
    def close(self, seg, sec, gs_count):
        pass
            
#    def update_node(self, obj):
#        """
#        Class:      err_isa
#        Name:       update_node
#        Desc:    
#        Params:     obj - map of passed variables
#        """
#        if obj['id'] == 'IEA':
#            pass # Handle variables
#        else:
#            self.children[-1].update_node(obj)

#    def set_st_id(self, st_id, trn_set_id):
#        self.cur_st_id = st_id
#        self.cur_trn_set_id = trn_set_id


class err_gs(err_node):
    """
    Name:    err_gs
    Desc:    Holds source GS loop information
    """

    def __init__(self, parent, seg, src):
        """
        Class:  err_gs
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
        """
        self.seg = seg
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.isa_id = isa_id
        self.cur_line = cur_line
        
        self.gs_control_num = gs_id
        self.fic = self.seg[1]
        self.id = 'GS'
        
        self.st_loops = []

        # From GE loop
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        self.st_count_accept = None # AK904

        self.parent = parent
        self.children = []
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_gs
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_gs(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_gs
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        self.errors.append((err_cde, err_str))

    def update_node(self, obj):
        """
        Class:      err_gs
        Name:       update_node
        Desc:    
        Params:     obj - map of passed variables
        """
        if obj['id'] == 'GE':
            #obj = {'id': 'ISA', 'seg': seg, 'src_id': src.get_id()}
            self.seg = obj['seg']
            self.src_id =  obj['src_id']
            (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.src_id
            #self.cur_gs_id = gs_id
            # From GE loop
            self.ge_cur_line = cur_line
            
            # AK901
            if '1' in self.errors: self.ack_code = 'R'
            elif '2' in self.errors: self.ack_code = 'R'
            elif '3' in self.errors: self.ack_code = 'R'
            elif '4' in self.errors: self.ack_code = 'R'
            elif '5' in self.errors: self.ack_code = 'E'
            elif '6' in self.errors: self.ack_code = 'E'
            else: self.ack_code = 'A'
            #if st rejected, set A = P

            self.st_count_orig = None # AK902
            self.st_count_recv = None # AK903
            self.st_count_accept = None # AK904
        else:
            self.st_loops[-1].update_node(obj)


class err_st(err_node):
    """
    Name:    err_st
    Desc:    ST loops

    Needs:
        Transaction set id code (837, 834)
        Transaction set control number

        trn set error codes
        
    At SE:
        Determine final ack code
        
    """

    def __init__(self, parent, seg, src):
        """
        Class:  err_st
        Name:   __init__
        Desc:    
        Params: 
        """
        self.trn_set_control_num = self.st_id
        self.id = 'ST'

        # Must be set before repr
        self.ack_code = None 
        self.parent = parent
        self.children = []
        self.errors = []


    def accept(self, visitor):
        """
        Class:      err_st
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_st(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_st
        Name:       add_error
        Desc:    
        Params:     
        """
        self.errors.append((err_cde, err_str))
 
    def update_node(self, obj):
        """
        Class:      err_st
        Name:       update_node
        Desc:    
        Params:     obj - map of passed variables
        """
        if obj['id'] == 'SE':
            pass # Handle variables
        else:
            raise EngineError, 'err_st.update_node - Unhandled obj', obj
        

class err_seg(err_node):
    """
    Name:    err_seg
    Desc:    Segment Errors
    """
    def __init__(self, parent, seg, src):
        """
        Class:  err_seg
        Name:   __init__
        Desc:    
        Params: 
        Needs:
            seg_id_code
            seg_pos - pos in ST loop
            loop_id - LS loop id
            name?
            seg_count - in parent

            errors:
                
        """
        self.seg_id_code = self.seg[0]
        self.seg_pos = self.seg_count
        self.loop_id = self.ls_id
        self.id = 'SEG'
        #self.seg_error_code = seg_error_code
        
        self.parent = parent
        self.children = []
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_seg
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_seg(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_seg
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        self.errors.append((err_cde, err_str))
        
    def err_count(self):
        """
        Class:      err_seg
        Name:       err_count
        Desc:    
        Returns:    count of errors
        """
        ele_err_ct = 0
        for ele in self.children:
            if ele.err_count() > 0:
                ele_err_ct = 1
                break
        return len(self.errors) + ele_err_ct

class err_ele(err_node):
    """
    Name:   err_ele
    Desc:   Element Errors - Holds and generates output for element and 
            composite/sub-element errors
            Each element with an error creates a new err_ele instance.  
    Needs:
            pos in element
            pos in composite
            element reference number
            element name?
            
            self.errors:
                error code
                error string
                bad value - if available
            
    """
    def __init__(self, parent, ele_pos, ele_ref_num, subele_pos=None):
        """
        Class:      err_ele
        Name:       __init__
        Desc:    
        Params:     
        """
        self.ele_pos = obj['ele_pos']
        self.subele_pos = obj['subele_pos']
        self.ele_ref_num = obj['ele_ref_num']
        #self.bad_val = bad_val
        self.id = 'ELE'

        self.parent = parent
        self.children = []
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_ele
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_ele(self)

    def add_error(self, err_cde, err_str, bad_value):
        """
        Class:      err_ele
        Name:       add_error
        Desc:    
        Params:     
        """
        self.errors.append((err_cde, err_str, bad_value))
        
    def err_count(self):
        return len(self.errors)
