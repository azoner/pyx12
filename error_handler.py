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

    def add_node(self, obj):
        if obj['id'] == 'ISA':
            self.isa_loops.append(err_isa(obj))
        else:
            self.isa_loops[-1].add_node(obj)
        
    def add_error(self, err):
        self.isa_loops[-1].add_error(err)
            

class err_isa:
    """
    Name:    err_isa
    Desc:    Holds source ISA loop errors
    """

    def __init__(self, obj):
        """
        Name:   __init__
        Desc:    
        Params: x12_src - instance of x12file
        """
        if obj['id'] != 'ISA':
            raise EngineError, 'err_isa.__init__', obj

        #self.x12_src = x12_src
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()

        self.gs_loops = []
        #self.gs_loop_count = 0
        #self.eol = '\n'

    def add_node(self, obj):
        if obj['id'] == 'GS':
            self.gs_loops.append(err_gs(obj))
        else:
            self.gs_loops[-1].add_node(obj)

    def add_error(self, err):
        if err['id'] == 'ISA':
            pass
            #add error info
        else:
            self.gs_loops[-1].add_error(err)
            
#    def set_st_id(self, st_id, trn_set_id):
#        self.cur_st_id = st_id
#        self.cur_trn_set_id = trn_set_id


class err_gs:
    """
    Name:    err_gs
    Desc:    Holds source GS loop information
    """

    def __init__(self, obj): #fic, root):
        """
        Class:  err_gs
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
        """
        if obj['id'] != 'GS':
            raise EngineError, 'err_gs.__init__', obj
        
        #self.fic = fic
        #self.root = root
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = root.x12_src.get_id()
        #self.cur_gs_id = gs_id
        self.st_loops = []
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        self.st_count_accept = None # AK904
        self.err_cde = [] # AK905-9

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
            self.err_cde.append([err_cde, err_str])
        else:
            self.st_loops[-1].add_error(err)
 
       
class err_st:
    """
    Name:    err_st
    Desc:    ST loops
    """

    def __init__(self, obj): #trn_set_id_code, root):
        """
        Class:  err_st
        Name:   __init__
        Desc:    
        Params: trn_set_id_code - Type of original transaction (837, 278, 835)
                root - root 997 node
        """
        if obj['id'] != 'ST':
            raise EngineError, 'err_st.__init__', obj
        
        #self.trn_set_id_code = trn_set_id_code
        #self.root = root
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.root.x12_src.get_id()
        #self.cur_st_id = st_id

        # Must be set before repr
        self.ack_code = None # AK501
        self.err_cde = [] # AK502-6

        self.segments = [] # err_seg instances

    def add_node(self, obj):
        """
        Class:      err_st
        Name:       add_node
        Desc:    
        Params:     obj - node object information
        """
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
 
        
#    def add_seg_error(self, seg_id_code, seg_error_code):
#        self.errors.append(err_seg_err(seg_id_code, seg_error_code, self.x12_src))
        
#    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
#            ele_err_code, bad_val=None):
#        try:    
#            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
#                self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
#        except:
#            self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
#        self.errors[-1].append(err_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       
      

class err_seg:
    """
    Name:    err_seg
    Desc:    Segment Errors
    """
    def __init__(self, obj): #seg_id_code, root, seg_error_code=None):

        if obj['id'] != 'SEG':
            raise EngineError, 'err_seg.__init__', obj
        #self.root = root
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.root.x12_src.get_id()
        #self.seg_id_code = seg_id_code
        #self.seg_pos = seg_count
        #self.loop_id = ls_id
        #self.seg_error_code = seg_error_code
        self.elems = []

    def add_node(self, obj):
        """
        Class:      err_seg
        Name:       add_node
        Desc:    
        Params:     obj - node object information
        """
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
            pass
            #add error info
        else:
            self.elems[-1].add_error(err)
        
#    def add_ele_error(self, ele_pos, subele_pos=None, ele_ref_num=None, \
#        ele_err_code, bad_val=None): 
#        self.elems.append(err_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))

class err_ele:
    """
    Name:   err_ele
    Desc:   Element Errors - Holds and generates output for element and 
            composite/sub-element errors
    """
    def __init__(self, obj): 
        #root, ele_pos, ele_err_code, subele_pos=None,ele_ref_num=None, bad_val=None):
        if obj['id'] != 'ELE':
            raise EngineError, 'err_ele.__init__', obj

        #self.root = root
        #self.ele_pos = ele_pos
        #self.subele_pos = subele_pos
        #self.ele_ref_num = ele_ref_num
        #self.ele_err_code = ele_err_code
        #self.bad_val = bad_val

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
        if err['id'] == 'ELE':
            pass
            #add error info
        else:
            raise EngineError, 'add_error - unhandled error', err
        
