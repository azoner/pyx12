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

#import os
#import sys
#import string
from types import *

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"

#class error_node:
#    def __init__(self)

class err_node:
    def __init__(self, obj): 
        #obj = {'id': '', 'seg': seg, 'src_id': src.get_id()}
        self.seg = obj['seg']
        self.src_id =  obj['src_id']
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.src_id
        self.cur_line = cur_line
        self.isa_id = isa_id
        self.gs_id = gs_id
        self.st_id = st_id
        self.ls_id = ls_id
        self.seg_count = seg_count

    def accept(self, visitor):
        pass
        
    def add_node(self, obj):
        pass
        
    def add_error(self, err):
        pass
        
    def update_node(self, obj):
        pass


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

        self.isa_loops = []
        #self.isa_loop_count = 0

    def accept(self, visitor):
        """
        Class:      err_root
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_root(self)

    def add_node(self, obj):
        if obj['id'] == 'ISA':
            self.isa_loops.append(err_isa(obj))
        else:
            self.isa_loops[-1].add_node(obj)
        
    def add_error(self, err):
        self.isa_loops[-1].add_error(err)

    def update_node(self, obj):
        self.isa_loops[-1].update_node(obj)
            

class err_isa(err_node):
    """
    Name:    err_isa
    Desc:    Holds source ISA loop errors
    """

    def __init__(self, obj):
        """
        Class:      err_isa
        Name:       __init__
        Desc:    
        Params:     x12_src - instance of x12file
        """
        err_node.__init__(self, obj)

        if obj['id'] != 'ISA':
            raise EngineError, 'err_isa.__init__', obj
        
        self.isa_trn_set_id = self.isa_id

        self.gs_loops = []
        self.err_cde = []

    def accept(self, visitor):
        """
        Class:      err_isa
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_isa(self)

    def add_node(self, obj):
        """
        Class:      err_isa
        Name:       add_node
        Desc:    
        Params:     obj - map of passed variables
        """
        if obj['id'] == 'GS':
            self.gs_loops.append(err_gs(obj))
        else:
            self.gs_loops[-1].add_node(obj)

    def add_error(self, err):
        """
        Class:      err_isa
        Name:       add_error
        Desc:    
        Params:     obj - map of passed variables
        """
        if err['id'] == 'ISA':
            err_cde = err['code']
            err_str = err['str']
            self.err_cde.append([err_cde, err_str])
        else:
            self.gs_loops[-1].add_error(err)
            
    def update_node(self, obj):
        """
        Class:      err_isa
        Name:       update_node
        Desc:    
        Params:     obj - map of passed variables
        """
        if obj['id'] == 'IEA':
            pass # Handle variables
        else:
            self.gs_loops[-1].update_node(obj)

#    def set_st_id(self, st_id, trn_set_id):
#        self.cur_st_id = st_id
#        self.cur_trn_set_id = trn_set_id


class err_gs(err_node):
    """
    Name:    err_gs
    Desc:    Holds source GS loop information
    """

    def __init__(self, obj):
        """
        Class:  err_gs
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
        """
        err_node.__init__(self, obj)

        if obj['id'] != 'GS':
            raise EngineError, 'err_gs.__init__', obj
        
        self.gs_control_num = self.gs_id
        self.fic = self.seg[1]
        
        self.st_loops = []

        # From GE loop
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        self.st_count_accept = None # AK904

        self.gs_errors = [] # AK905-9

    def accept(self, visitor):
        """
        Class:      err_gs
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_gs(self)

    def add_node(self, obj):
        """
        Class:      err_gs
        Name:       add_node
        Desc:    
        Params:     obj - node object information
        """
        if obj['id'] == 'ST':
            self.st_loops.append(err_st(obj))
        else:
            self.st_loops[-1].add_node(obj)

    def add_error(self, err):
        """
        Class:      err_gs
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        if err['id'] == 'GS':
            err_cde = err['code']
            err_str = err['str']
            self.gs_errors.append([err_cde, err_str])
        else:
            self.st_loops[-1].add_error(err)

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
            if '1' in self.gs_errors: self.ack_code = 'R'
            elif '2' in self.gs_errors: self.ack_code = 'R'
            elif '3' in self.gs_errors: self.ack_code = 'R'
            elif '4' in self.gs_errors: self.ack_code = 'R'
            elif '5' in self.gs_errors: self.ack_code = 'E'
            elif '6' in self.gs_errors: self.ack_code = 'E'
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

    def __init__(self, obj):
        """
        Class:  err_st
        Name:   __init__
        Desc:    
        Params: 
        """
        err_node.__init__(self, obj)

        if obj['id'] != 'ST':
            raise EngineError, 'err_st.__init__', obj
        
        self.trn_set_control_num = self.st_id

        # Must be set before repr
        self.ack_code = None # AK501
        self.err_cde = [] # AK502-6

        self.segments = [] # err_seg instances

    def accept(self, visitor):
        """
        Class:      err_st
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_st(self)

    def add_node(self, obj):
        """
        Class:      err_st
        Name:       add_node
        Desc:    
        Params:     obj - node object information
        """
        if self.segments:
            if self.segments[-1].err_count() == 0:
                del self.segments[-1]
        if obj['id'] == 'SEG':
            self.segments.append(err_seg(obj))
        else:
            self.segments[-1].add_node(obj)

    def add_error(self, err):
        """
        Class:      err_st
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        if err['id'] == 'ST':
            pass
            #add error info
        else:
            self.segments[-1].add_error(err)
 
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
    def __init__(self, obj):
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

            st_errors:
                
        """
        err_node.__init__(self, obj)

        if obj['id'] != 'SEG':
            raise EngineError, 'err_seg.__init__', obj
        self.seg_id_code = self.seg[0]
        self.seg_pos = self.seg_count
        self.loop_id = self.ls_id
        #self.seg_error_code = seg_error_code
        
        self.st_errors = []
        self.elems = []

    def accept(self, visitor):
        """
        Class:      err_seg
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_seg(self)

    def add_node(self, obj):
        """
        Class:      err_seg
        Name:       add_node
        Desc:    
        Params:     obj - node object information
        """
        # If last element added does not have any errors by now, delete
        if self.elems:
            if self.elems[-1].err_count() == 0:
                del self.elems[-1]
        if obj['id'] == 'ELE':
            self.elems.append(err_ele(obj))
        else:
            #self.elems[-1].add_node(obj)
            raise EngineError, 'add_node - unhandled add', obj

    def add_error(self, err):
        """
        Class:      err_seg
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        if err['id'] == 'SEG':
            self.st_errors.append((err['code'], err['value'], err['seq'], \
                err['data_ele'], err['str']))
        else:
            self.elems[-1].add_error(err)
        
    def err_count(self):
        """
        Class:      err_seg
        Name:       err_count
        Desc:    
        Returns:    count of errors
        """
        ele_err_ct = 0
        for ele in self.ele_errors:
            if ele.err_count() > 0:
                ele_err_ct = 1
                break
        return len(self.st_errors) + ele_err_ct

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
            
            self.ele_errors:
                error code
                error string
                bad value - if available
            
    """
    def __init__(self, obj): 
        """
        Class:      err_ele
        Name:       __init__
        Desc:    
        Params:     obj
        """
        err_node.__init__(self, obj)

        if obj['id'] != 'ELE':
            raise EngineError, 'err_ele.__init__', obj

        self.ele_pos = ele_pos
        self.subele_pos = subele_pos
        self.ele_ref_num = ele_ref_num
        #self.bad_val = bad_val

        self.ele_errors = []

    def accept(self, visitor):
        """
        Class:      err_ele
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_ele(self)

#    def add_node(self, obj):
#        """
#        Class:      err_ele
#        Name:       add_node
#        Desc:    
#        Params:     obj - node object information
#        """
#        pass
#        raise EngineError, 'add_node - unhandled add', obj
        
    def add_error(self, err):
        """
        Class:      err_ele
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        #self.ele_err_code = ele_err_code
        if err['id'] == 'ELE':
            self.ele_errors.append((err['code'], err['value'], err['str']))            
        else:
            raise EngineError, 'add_error - unhandled error', err
        
    def err_count(self):
        return len(self.ele_errors)
