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
Interface to an X12 997 Response
"""

#import os
import sys
import string
from types import *

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"


class 997_if:
    """
    Name:    997_if
    Desc:    Interface to an X12 997 Response
    """

    def __init__(self, fic, trn_set_id_code, x12_src):
        """
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
                x12_src - instance of x12file
        """
        
        self.fic = fic
        self.trn_set_id_code = trn_set_id_code
        self.x12_src = x12_src
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()
        self.cur_gs_id = gs_id
        self.cur_st_id = st_id

        self.errors = []

        
    def __repr__(self):
        str = 'AK1*%s*%s~\n' % (self.fic, self.cur_gs_id)
        str += 'AK2*%s*%s~\n' % (self.trn_set_id_code, self.cur_st_id)
        for seg_err in self.errors:
            str += seg_err.__repr__()
        if len(self.errors) > 0:
            err_cde = 'R'
        else:
            err_cde = 'A'
        str += 'AK5*%s*%s~\n' % (err_cde, 
        return str

    def add_seg_error(self, seg_id_code, seg_error_code):
        self.errors.append(997_seg_err(seg_id_code, seg_error_code, self.x12_src))
        
    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
            ele_err_code, bad_val=None):
        try:    
            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
                self.errors.append(997_seg_err(seg_id_code, 8, self.x12_src))
        except:
            self.errors.append(997_seg_err(seg_id_code, 8, self.x12_src))
        self.errors[-1].append(997_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       
#    def set_st_id(self, st_id, trn_set_id):
#        self.cur_st_id = st_id
#        self.cur_trn_set_id = trn_set_id

#    def __iter__(self):
#        return self

#    def next(self):
#        return None

class 997_gs:
    """
    Name:    997_gs
    Desc:    Holds source GS loop information
    """

    def __init__(self, fic, x12_src):
        """
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
                x12_src - instance of x12file
        """
        
        self.fic = fic
        self.x12_src = x12_src
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()
        self.cur_gs_id = gs_id
        self.st_loops = []
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        self.st_count_accept = None # AK904
        self.err_cde = [] # AK905-9

        
    def __repr__(self):
        if not (self.ack_code and self.st_count_orig and self.st_count_recv \
            and self.st_count_accept):
            raise EngineError, '997_gs variables not set'
        str = 'AK1*%s*%s~\n' % (self.fic, self.cur_gs_id)
        for seg_err in self.errors:
            str += seg_err.__repr__()
        str += 'AK9*%s*%i*%i*%i' % (self.ack_code, self.st_count_orig, \
            self.st_count_recv, self.st_count_accept)
        for code in err_cde:
            str += '*%s' % code
        str += '~\n'
        return str

    def add_seg_error(self, seg_id_code, seg_error_code):
        self.errors.append(997_seg_err(seg_id_code, seg_error_code, self.x12_src))
        
    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
            ele_err_code, bad_val=None):
        try:    
            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
                self.errors.append(997_seg_err(seg_id_code, 8, self.x12_src))
        except:
            self.errors.append(997_seg_err(seg_id_code, 8, self.x12_src))
        self.errors[-1].append(997_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       

class 997_seg_err:

    def __init__(self, seg_id_code, seg_error_code=None, x12_src):

        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()
        self.seg_id_code = seg_id_code
        self.seg_pos = seg_count
        self.loop_id = ls_id
        self.seg_error_code = seg_error_code
        
        self.elems = []
        
    def __repr__(self):
        str = 'AK3*%s*%i' % (self.seg_id_code, self.seg_pos)
        if self.loop_id:
            str += '*%s' % self.loop_id
        if self.seg_error_code:
            str += '*%s' % self.seg_error_code
        str += '~\n'
        for ele in self.elems:
            str += ele.__repr__()
        return str

#    def add_ele_error(self, ele_pos, subele_pos=None, ele_ref_num=None, \
#        ele_err_code, bad_val=None): 
#        self.elems.append(997_ele_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))

    def is_match(self, seg_id_code, seg_error_code, x12_src):
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = x12_src.get_id()
        if seg_id_code == self.seg_id_code and seg_error_code == self.seg_error_code \
            and seg_count == self.seg_pos and ls_id == self.loop_id:
            return True
        return False

class 997_ele_err:

    def __init__(self, ele_pos, subele_pos=None, ele_ref_num=None, \
        ele_err_code, bad_val=None):

        self.ele_pos = ele_pos
        self.subele_pos = subele_pos
        self.ele_ref_num = ele_ref_num
        self.ele_err_code = ele_err_code
        self.bad_val = bad_val
        
    def __repr__(self):
        str = 'AK4*%i' % (self.ele_pos)
        if self.subele_pos: str += ':%i' % self.subele_pos
        if self.ele_ref_num: str += '*%s' % self.ele_ref_num
        else str += '*'
        str += '*%s' % self.ele_err_code
        if self.bad_val: str += '*%s' % self.bad_val
        str += '~\n'
        return str
