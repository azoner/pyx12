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
import string
from types import *

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"


class err_root:
    """
    Name:   err_root
    Desc:   
    """
    def __init__(self, x12_src, st_control_num):
        """
        Name:   __init__
        Desc:    
        Params: x12_src - instance of x12file
        """
        self.x12_src = x12_src
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()

        self.gs_loops = []
        self.gs_loop_count = 0
        self.eol = '\n'

        
    def __repr__(self):
        x12src = self.x12_src
        eol = self.eol
        str = ''
        for gs_loop in self.gs_loops:
            str += gs_loop.__repr__()
        self.gs_loop_count += 1
        return str

    def add_seg_error(self, seg_id_code, seg_error_code):
        self.errors.append(err_seg(seg_id_code, seg_error_code, self))
        
    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
            ele_err_code, bad_val=None):
        try:    
            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
                self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
        except:
            self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
        self.errors[-1].append(err_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       
    def set_st_id(self, st_id, trn_set_id):
        self.cur_st_id = st_id
        self.cur_trn_set_id = trn_set_id

#    def __iter__(self):
#        return self

#    def next(self):
#        return None

class err_gs:
    """
    Name:    err_gs
    Desc:    Holds source GS loop information
    """

    def __init__(self, fic, root):
        """
        Class:  err_gs
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
        """
        
        self.fic = fic
        self.root = root
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = root.x12_src.get_id()
        self.cur_gs_id = gs_id
        self.st_loops = []
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        self.st_count_accept = None # AK904
        self.err_cde = [] # AK905-9

#    def add_seg_error(self, seg_id_code, seg_error_code):
#        self.errors.append(err_seg_err(seg_id_code, seg_error_code, self.x12_src))
#        
#    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
#            ele_err_code, bad_val=None):
#        try:    
#            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
#                self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
#        except:
#            self.errors.append(err_seg_err(seg_id_code, 8, self.x12_src))
#        self.errors[-1].append(err_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
        
class err_st:
    """
    Name:    err_st
    Desc:    ST loops
    """

    def __init__(self, trn_set_id_code, root):
        """
        Class:  err_st
        Name:   __init__
        Desc:    
        Params: trn_set_id_code - Type of original transaction (837, 278, 835)
                root - root 997 node
        """
        
        self.trn_set_id_code = trn_set_id_code
        self.root = root
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.root.x12_src.get_id()
        self.cur_st_id = st_id

        # Must be set before repr
        self.ack_code = None # AK501
        self.err_cde = [] # AK502-6

        self.seg_errors = [] # err_seg instances

        
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
    def __init__(self, seg_id_code, root, seg_error_code=None):

        self.root = root
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.root.x12_src.get_id()
        self.seg_id_code = seg_id_code
        self.seg_pos = seg_count
        self.loop_id = ls_id
        self.seg_error_code = seg_error_code
        
        self.elems = []
        
#    def add_ele_error(self, ele_pos, subele_pos=None, ele_ref_num=None, \
#        ele_err_code, bad_val=None): 
#        self.elems.append(err_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))

class err_ele:
    """
    Name:   err_ele
    Desc:   Element Errors - Holds and generates output for element and 
            composite/sub-element errors
    """
    def __init__(self, root, ele_pos, ele_err_code, subele_pos=None, \
        ele_ref_num=None, bad_val=None):

        self.root = root
        self.ele_pos = ele_pos
        self.subele_pos = subele_pos
        self.ele_ref_num = ele_ref_num
        self.ele_err_code = ele_err_code
        self.bad_val = bad_val
        
