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
#import sys
import string
from types import *

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"


class if_997:
    """
    Name:   if_997
    Desc:   Interface to an X12 997 Response
            Everytime we hit a GS loop in the source, create a new instance of
            this class.
            Holds instances of source GS loops
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

#    def add_seg_error(self, seg_id_code, seg_error_code):
#        self.errors.append(seg_997(seg_id_code, seg_error_code, self))
        
#    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
#            ele_err_code, bad_val=None):
#        try:    
#            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
#                self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        except:
#            self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        self.errors[-1].append(ele_997_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       
#    def set_st_id(self, st_id, trn_set_id):
#        self.cur_st_id = st_id
#        self.cur_trn_set_id = trn_set_id

#    def __iter__(self):
#        return self

#    def next(self):
#        return None

class gs_997:
    """
    Name:    gs_997
    Desc:    Holds source GS loop information
    """

    def __init__(self, fic, root):
        """
        Class:  gs_997
        Name:   __init__
        Desc:    
        Params: fic - Functional Identifier Code (GS01)
                root - root 997 node
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

        
    def __repr__(self):
        """
        Class:  gs_997
        Name:   __repr__
        Desc:   Creates 997 data
        Params: 
        Note:   Must set variables before print
        """
        x12src = self.root.x12_src
        eol = self.root.eol
        if not (self.ack_code and self.st_count_orig and self.st_count_recv \
            and self.st_count_accept):
            raise EngineError, 'gs_997 variables not set'
        #ST
        seg = ['ST', '997', '%i'%st_control_num]
        str = x12src.seg_str(seg, eol)

        #AK1
        str += x12src.seg_str(['AK1', self.fic, self.cur_gs_id], eol)
        
        #Loop AK2
        for st_loop in self.st_loops:
            str += st_loop.__repr__()
        
        #AK9
        seg = ['AK9', self.ack_code, '%i'%self.st_count_orig, \
            '%i'%self.st_count_recv, '%i'%self.st_count_accept]
        for code in self.err_cde:
            seg.append('%s' % code)
        str += x12src.seg_str(seg, eol)
        
        #SE
        seg_count = str.count(x12src.seg_term+self.eol) + 1
        seg = ['SE', '%i'%seg_count, '%i'%st_control_num]
        str = x12src.seg_str(seg, eol)
        return str

#    def add_seg_error(self, seg_id_code, seg_error_code):
#        self.errors.append(seg_997_err(seg_id_code, seg_error_code, self.x12_src))
#        
#    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
#            ele_err_code, bad_val=None):
#        try:    
#            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
#                self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        except:
#            self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        self.errors[-1].append(ele_997_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
        
class st_997:
    """
    Name:    st_997
    Desc:    ST loops
    """

    def __init__(self, trn_set_id_code, root):
        """
        Class:  st_997
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

        self.seg_errors = [] # seg_997 instances

        
    def __repr__(self):
        """
        Class:  st_997
        Name:   __repr__
        Desc:   Creates 997 data
        Params: 
        Note:   Must set variables before print
        """
        x12src = self.root.x12_src
        eol = self.root.eol
        str = x12src.seg_str(['AK2', self.trn_set_id_code, self.cur_st_id], eol) 
        for seg_err in self.seg_errors:
            str += seg_err.__repr__()
        seg = ['AK5']
        if len(self.seg_errors) > 0:
            seg.append('R')
        else:
            seg.append('A')
        str += x12src.seg_str(seg, eol) 
        return str

#    def add_seg_error(self, seg_id_code, seg_error_code):
#        self.errors.append(seg_997_err(seg_id_code, seg_error_code, self.x12_src))
        
#    def add_ele_error(self, seg_id_code, ele_pos, subele_pos=None, ele_ref_num=None, \
#            ele_err_code, bad_val=None):
#        try:    
#            if not self.errors[-1].is_match(seg_id_code, 8, self.x12_src):
#                self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        except:
#            self.errors.append(seg_997_err(seg_id_code, 8, self.x12_src))
#        self.errors[-1].append(ele_997_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))
       
      

class seg_997:
    """
    Name:    seg_997
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
        
    def __repr__(self):
        x12src = self.root.x12_src
        eol = self.root.eol
        seg = ['AK3', self.seg_id_code, '%i'%self.seg_pos]
        if self.loop_id:
            seg.append(self.loop_id)
        else:
            seg.append('')
        if self.seg_error_code:
            seg.append(self.seg_error_code)
        str = x12src.seg_str(seg, eol) 
        for ele in self.elems:
            str += ele.__repr__()
        return str

#    def add_ele_error(self, ele_pos, subele_pos=None, ele_ref_num=None, \
#        ele_err_code, bad_val=None): 
#        self.elems.append(ele_997_err(ele_pos, subele_pos, ele_ref_num, ele_err_code, bad_val))

    def is_match(self, seg_id_code, seg_error_code):
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = self.root.x12_src.get_id()
        if seg_id_code == self.seg_id_code and seg_error_code == self.seg_error_code \
            and seg_count == self.seg_pos and ls_id == self.loop_id:
            return True
        return False

class ele_997:
    """
    Name:    ele_997
    Desc:    Element Errors
    """
    def __init__(self, root, ele_pos, ele_err_code, subele_pos=None, \
        ele_ref_num=None, bad_val=None):

        self.root = root
        self.ele_pos = ele_pos
        self.subele_pos = subele_pos
        self.ele_ref_num = ele_ref_num
        self.ele_err_code = ele_err_code
        self.bad_val = bad_val
        
    def __repr__(self):
        x12src = self.root.x12_src
        eol = self.root.eol
        seg = ['AK4']
        if self.subele_pos: 
            seg.append(['%i' % (self.ele_pos), '%i' % self.subele_pos])
        else:
            seg.append('%i' % (self.ele_pos))
        if self.ele_ref_num:
            seg.append(self.ele_ref_num)
        else:
            seg.append('')
        seg.append(self.ele_err_code)
        if self.bad_val:
            seg.append(self.bad_val)
        return x12src.seg_str(seg, eol)
