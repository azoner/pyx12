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
import pdb

# Intrapackage imports
from errors import *

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"

#class error_node:
#    def __init__(self)

logger = logging.getLogger('pyx12.error_handler')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class err_iter:
    def __init__(self, errh):
        self.errh = errh
        self.cur_node = errh
        #self.done = False
        self.visit_stack = []

    def first(self):
        self.cur_node = self.errh
    
    def next(self):
        #pdb.set_trace()
        #orig_node = self.cur_node

        #If at previosly visited branch, do not do children
        if self.cur_node in self.visit_stack:
            node = None
        else:
            node = self.cur_node.get_first_child()
        if node is not None:
            self.visit_stack.append(self.cur_node)
            self.cur_node = node
        else:
            node = self.cur_node.get_next_sibling()
            if node is not None:
                self.cur_node = node
            else:
                if not self.cur_node.is_closed():
                    raise IterOutOfBounds
                #pdb.set_trace()
                node = self.cur_node.get_parent()
                if node is None:
                    raise IterOutOfBounds
                #if node.get_cur_line() < self.src.cur_line:
                if not node.is_closed():
                    raise IterOutOfBounds
                if self.cur_node in self.visit_stack:
                    del self.visit_stack[-1]
                self.cur_node = node
                #logger.debug(node)
                if node.id == 'ROOT':
                    raise IterOutOfBounds
                #    raise IterDone

    def next_old(self):
        #pdb.set_trace()
        start_line = self.cur_node.get_cur_line()
        orig_node = self.cur_node
        if self.done:
            raise EngineError, 'Iterator was completed'
        try:
            self.cur_node = self.cur_node.get_first_child()
        except IterOutOfBounds:
            while not self.done:
                try:
                    self.cur_node = self.cur_node.get_next_sibling()
                    break
                except IterOutOfBounds:
                    self.cur_node = self.cur_node.get_parent()
                    break
                except IterDone:
                    self.done = True
        if self.cur_node.get_cur_line() < start_line:
            self.cur_node = orig_node
            self.done = False
            raise IterOutOfBounds

    def get_cur_node(self):
        return self.cur_node
        
#    def is_done(self):
#        return self.done

           

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
        self.seg_node_added = False
        self.cur_ele_node = None
        self.cur_line = 0

    def accept(self, visitor):
        """
        Class:      err_handler
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_root_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_root_post(self)

    def get_cur_line(self):
        """
        Class:      err_handler
        """
        return self.cur_line

    def get_id(self):
        """
        Class:      err_handler
        """
        return self.id

    def add_isa_loop(self, seg, src):
        """
        Class:      err_handler
        """
        #logger.debug('add_isa loop')
        self.children.append(err_isa(self, seg, src))
        self.cur_isa_node = self.children[-1]
        self.cur_seg_node = self.cur_isa_node
        self.seg_node_added = True
        
    def add_gs_loop(self, seg, src):
        """
        Class:      err_handler
        """
        #logger.debug('add_gs loop')
        parent = self.cur_isa_node
        parent.children.append(err_gs(parent, seg, src))
        self.cur_gs_node = parent.children[-1]
        self.cur_seg_node = self.cur_gs_node
        self.seg_node_added = True
        
    def add_st_loop(self, seg, src):
        """
        Class:      err_handler
        """
        #logger.debug('add_st loop')
        parent = self.cur_gs_node
        parent.children.append(err_st(parent, seg, src))
        self.cur_st_node = parent.children[-1]
        self.cur_seg_node = self.cur_st_node
        self.seg_node_added = True
        
    def add_seg(self, map_node, seg, seg_count, cur_line, ls_id):
        """
        Class:      err_handler
        """
        parent = self.cur_st_node
        self.cur_seg_node = err_seg(parent, map_node, seg, seg_count, cur_line, ls_id)
        self.seg_node_added = False
        #logger.debug('add_seg: %s' % map_node.name)
        #if len(parent.children) > 0:
        #    if parent.children[-1].err_count() == 0:
        #        del parent.children[-1]
        #        logger.debug('del seg: %s' % map_node.name)
        #parent.children.append(err_seg(parent, map_node, seg, src))
        
    def _add_cur_seg(self):
        """
        Class:      err_handler
        """
        #pdb.set_trace()
        if not self.seg_node_added:
            self.cur_st_node.children.append(self.cur_seg_node)
            self.seg_node_added = True
        
    def add_ele(self, map_node):
        """
        Class:      err_handler
        """
        if self.cur_seg_node.id == 'ISA':
            self.cur_ele_node = err_ele(self.cur_isa_node, map_node)
        elif self.cur_seg_node.id == 'GS':
            self.cur_ele_node = err_ele(self.cur_gs_node, map_node)
        elif self.cur_seg_node.id == 'ST':
            self.cur_ele_node = err_ele(self.cur_st_node, map_node)
        else:
            self.cur_ele_node = err_ele(self.cur_seg_node, map_node)
        self.ele_node_added = False
    
    def _add_cur_ele(self):
        """
        Class:      err_handler
        """
        self._add_cur_seg()
        if not self.ele_node_added:
            self.cur_seg_node.elements.append(self.cur_ele_node)
            self.ele_node_added = True
        #logger.debug('----  add_ele: %s' % self.cur_seg_node.elements[-1].name)
            
    def isa_error(self, err_cde, err_str):
        """
        Class:      err_handler
        """
        logger.error('isa_error: %s - %s' % (err_cde, err_str))
        self.cur_isa_node.add_error(err_cde, err_str)

    def gs_error(self, err_cde, err_str):
        """
        Class:      err_handler
        """
        logger.error('gs_error: %s - %s' % (err_cde, err_str))
        self.cur_gs_node.add_error(err_cde, err_str)
        
    def st_error(self, err_cde, err_str):
        """
        Class:      err_handler
        """
        logger.error('st_error: %s - %s' % (err_cde, err_str))
        self.cur_st_node.add_error(err_cde, err_str)
        
    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        Class:      err_handler
        """
        sout = ''
        if src_line is not None:
            sout += '#%s '
        sout += 'seg_error: %s - %s (%s)' % (err_cde, err_str, err_value)
        logger.error(sout)
        self._add_cur_seg()
        self.cur_seg_node.add_error(err_cde, err_str, err_value)
        
    def ele_error(self, err_cde, err_str, bad_value):
        """
        Class:      err_handler
        """
        logger.error('element_error: %s - %s (%s)' % (err_cde, err_str, bad_value))
        self._add_cur_ele()
        self.cur_ele_node.add_error(err_cde, err_str, bad_value) #, pos, data_ele)
        #print self.cur_ele_node.errors

    def close_isa_loop(self, node, seg, src):
        """
        Class:      err_handler
        """
        self.cur_isa_node.close(node, seg, src)
        self.cur_seg_node = self.cur_isa_node
        self.seg_node_added = True
        
    def close_gs_loop(self, node, seg, src):
        """
        Class:      err_handler
        """
        self.cur_gs_node.close(node, seg, src)
        self.cur_seg_node = self.cur_gs_node
        self.seg_node_added = True
        
    def close_st_loop(self, node, seg, src):
        """
        Class:      err_handler
        """
        self.cur_st_node.close(node, seg, src)
        self.cur_seg_node = self.cur_st_node
        self.seg_node_added = True
        
    def find_node(self, type):
        """
        Class:      err_handler
        Find the last node of a type
        """
        new_node = self.cur_node
        node_order = {'ROOT': 1, 'ISA': 2, 'GS': 3, 'ST': 4, 'SEG': 5, 'ELE': 6}
        while node_order[type] > new_node[new_node.get_id()]:
            new_node = new_node.get_parent()
        #walk error tree to find place to append
        #if type == 'ISA':
        #return node

#    def update_node(self, obj):
#        self.children[-1].update_node(obj)

    def _get_last_child(self):
        """
        Class:      err_handler
        """
        if len(self.children) != 0:
            return self.children[-1]
        else:
            return None
    
    def get_parent(self):
        return None

    def get_error_count(self):
        """
        Class:      err_handler
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count

    def get_first_child(self):
        """
        Class:      err_handler
        """
        if len(self.children) > 0:
            return self.children[0]
        else:
            return None
         
    def get_next_sibling(self):
        """
        Class:      err_handler
        """
        return None
        #raise IterDone

    def next(self):
        """
        Class:      err_handler
        Desc:       Return the next error node
        """
        for child in self.children:
            yield child

    def is_closed(self):
        return True
            
    def __repr__(self):
        """
        Class:      err_handler
        """
        return '%i: %s' % (-1, self.id)
         

class err_node:
    def __init__(self, parent): 
        """
        Class:      err_node
        """
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
        self.parent = parent
        self.id = None
        self.children = []
        self.cur_line = -1
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_node
        """
        pass
        
#    def update_node(self, obj):
#        pass

    def get_cur_line(self):
        """
        Class:      err_handler
        """
        return self.cur_line

    def get_id(self):
        """
        Class:      err_node
        """
        return self.id

    def get_parent(self):
        """
        Class:      err_node
        """
        return self.parent

    def _get_last_child(self):
        """
        Class:      err_node
        """
        if len(self.children) != 0:
            return self.children[-1]
        else:
            return None

    def get_next_sibling(self):
        """
        Class:      err_node
        """
        #if self.id == 'ROOT': raise EngineError
        bFound = False
        for sibling in self.parent.children:
            if bFound:
                return sibling
            if sibling is self:
                bFound = True
        return None
        #raise IterOutOfBounds

    def get_first_child(self):
        """
        Class:      err_node
        """
        if len(self.children) > 0:
            return self.children[0]
        else:
            return None
        
    def get_error_count(self):
        """
        Class:      err_node
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count

    def get_error_list(self, seg_id, pre=False):
        """
        Class:      err_node
        """
        return self.errors
    
    def is_closed(self):
        """
        Class:      err_node
        """
        return True

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
        self.seg = seg
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.isa_id = isa_id
        self.cur_line_isa = cur_line
        self.cur_line_iea = None
        
        self.isa_trn_set_id = self.isa_id
        self.id = 'ISA'

        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []

    def is_closed(self):
        if self.cur_line_iea:
            return True
        else:
            return False

    def accept(self, visitor):
        """
        Class:      err_isa
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_isa_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_isa_post(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_isa
        Name:       add_error
        Desc:    
        Params:     
        """
        self.errors.append((err_cde, err_str))
        
    def close(self, node, seg, src):
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.cur_line_iea = cur_line

    def get_cur_line(self):
        """
        Class:      err_isa
        """
        if self.cur_line_iea:
            return self.cur_line_iea
        else:
            return self.cur_line_isa

    def get_error_count(self):
        """
        Class:      err_isa
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count + len(self.errors)

    def get_error_list(self, seg_id, pre=False):
        """
        Class:      err_isa
        """
        if seg_id == 'ISA':
            return filter(lambda err: 'ISA' in err[0], self.errors)
        elif seg_id == 'IEA':
            return filter(lambda err: 'IEA' in err[0], self.errors)
        else:
            return []
        #err_list = []
        #for err in self.errors:
        #    if seg_id in err[0]:
        #        err_list.append(err)
        #return err_list
    
    def next(self):
        """
        Desc:       Return the next error node
        """
        for child in self.children:
            yield child
        self.parent.next()
            
    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)
            

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
        self.cur_line_gs = cur_line
        self.cur_line_ge = None
        
        self.gs_control_num = gs_id
        self.fic = self.seg[1]
        self.id = 'GS'
        
        self.st_loops = []

        # From GE loop
        self.ack_code = None # AK901
        self.st_count_orig = None # AK902
        self.st_count_recv = None # AK903
        #self.st_count_accept = None # AK904

        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []

    def accept(self, visitor):
        """
        Class:      err_gs
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_gs_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_gs_post(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_gs
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        self.errors.append((err_cde, err_str))

    def close(self, node, seg, src):
        """
        Class:      err_gs
        Name:       close
        Desc:    
        Params:     
        """
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        #self.cur_gs_id = gs_id
        # From GE loop
        self.cur_line_ge = cur_line

        if '1' in self.errors: self.ack_code = 'R'
        elif '2' in self.errors: self.ack_code = 'R'
        elif '3' in self.errors: self.ack_code = 'R'
        elif '4' in self.errors: self.ack_code = 'R'
        elif '5' in self.errors: self.ack_code = 'E'
        elif '6' in self.errors: self.ack_code = 'E'
        else: self.ack_code = 'A'


        if seg is None:
            self.st_count_orig = 0
        else:
            self.st_count_orig = int(seg[1]) # AK902
        self.st_count_recv = src.st_count # AK903
        #self.st_count_accept = self.st_count_recv - len(self.children) # AK904

    def count_failed_st(self):
        ct = 0
        for child in self.children:
            if child.ack_code not in ['A', 'E']:
                ct += 1
        return ct

    def get_cur_line(self):
        """
        Class:      err_gs
        """
        if self.cur_line_ge:
            return self.cur_line_ge
        else:
            return self.cur_line_gs

    def get_error_count(self):
        """
        Class:      err_gs
        """
        count = 0
        for child in self.children:
            count += child.get_error_count()
        return count + len(self.errors)

    def get_error_list(self, seg_id, pre=False):
        """
        Class:      err_gs
        """
        if seg_id == 'GS':
            return filter(lambda err: err[0] in ('6'), self.errors)
        elif seg_id == 'GE':
            return filter(lambda err: err[0] not in ('6'), self.errors)
        else:
            return []
   
    def is_closed(self):
        if self.cur_line_ge:
            return True
        else:
            return False

    def next(self):
        """
        Desc:       Return the next error node
        """
        for child in self.children:
            yield child
        self.parent.next()
            
    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)

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
        self.seg = seg
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.trn_set_control_num = st_id
        self.cur_line_st = cur_line
        self.cur_line_se = None
        self.trn_set_id = seg[1] # eg 837

        self.id = 'ST'
        
        self.ack_code = 'R'
        self.parent = parent
        self.children = []
        self.errors = []
        self.elements = []
        #self.rejected = None

    def accept(self, visitor):
        """
        Class:      err_st
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_st_pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.visit_st_post(self)

    def add_error(self, err_cde, err_str):
        """
        Class:      err_st
        Name:       add_error
        Desc:    
        Params:     
        """
        self.errors.append((err_cde, err_str))
 
    def close(self, node, seg, src):
        """
        Class:      err_st
        Name:       close
        Desc:    
        Params:     
        """
        (isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.cur_line_se = cur_line
        if self.err_count() > 0:
            self.ack_code = 'R'
        else:
            self.ack_code = 'A'
        
    def err_count(self):
        """
        Class:      err_st
        Name:       err_count
        Desc:    
        Returns:    count of errors
        """
        seg_err_ct = 0
        if self.child_err_count() > 0:
            seg_err_ct = 1
        return len(self.errors) + seg_err_ct

    def get_error_count(self):
        return self.err_count()
    
    def get_error_list(self, seg_id, pre=False):
        """
        Class:      err_st
        """
        if seg_id == 'ST':
            return filter(lambda err: err[0] in ('1', '6', '7', '23'), self.errors)
        elif seg_id == 'SE':
            return filter(lambda err: err[0] not in ('1', '6', '7', '23'), self.errors)
        else:
            return []
   
    def child_err_count(self):
        ct = 0
        for child in self.children:
            if child.err_count() > 0:
                ct += 1
        return ct
       
    def get_cur_line(self):
        """
        Class:      err_st
        """
        if self.cur_line_se:
            return self.cur_line_se
        else:
            return self.cur_line_st

    def is_closed(self):
        if self.cur_line_se:
            return True
        else:
            return False

    def next(self):
        """
        Class:      err_st
        Desc:       Return the next error node
        """
        for child in self.children:
            yield child
        return
        #self.parent.next()
            
    def __repr__(self):
        return '%i: %s' % (self.get_cur_line(), self.id)


class err_seg(err_node):
    """
    Name:    err_seg
    Desc:    Segment Errors
    """
    def __init__(self, parent, map_node, seg, seg_count, cur_line, ls_id):
        """
        Class:  err_seg
        Name:   __init__
        Desc:    
        Params: 
        Needs:
            seg_id_code
            seg_pos - pos in ST loop
            loop_id - LS loop id
            seg_count - in parent
        """
        self.parent = parent
        if map_node is None:
            self.name = 'Unknown'
            self.pos = -1
        else:
            self.name = map_node.name
            self.pos = map_node.pos
        self.seg_id = seg[0]
        #(isa_id, gs_id, st_id, ls_id, seg_count, cur_line) = src.get_id()
        self.seg_count = seg_count
        self.cur_line = cur_line
        self.ls_id = ls_id
        
        self.id = 'SEG'
        
        self.elements= []
        self.errors = []

    def accept(self, visitor):
        """
        Class:      err_seg
        Name:       accept
        Desc:    
        Params:     visitor - ref to visitor class
        """
        visitor.visit_seg(self)
        for elem in self.elements:
            elem.accept(visitor)

    def add_error(self, err_cde, err_str, err_value=None):
        """
        Class:      err_seg
        Name:       add_error
        Desc:    
        Params:     err - node error information
        """
        self.errors.append((err_cde, err_str, err_value))
        
    def err_count(self):
        """
        Class:      err_seg
        Name:       err_count
        Desc:    
        Returns:    count of errors
        """
        ele_err_ct = 0
        if self.child_err_count() > 0:
            ele_err_ct = 1
        return len(self.errors) + ele_err_ct
    
    def get_error_count(self):
        return self.err_count()
    
    def child_err_count(self):
        ct = 0
        for ele in self.elements:
            if ele.err_count() > 0:
                ct += 1
        return ct

    def next(self):
        """
        Desc:       Return the next error node
        """
        #for child in self.children:
        #    yield child
        #pdb.set_trace()
        return self
        #self.parent.next()
            
    def __repr__(self):
        return '%i: %s %s' % (self.get_cur_line(), self.id, self.seg_id)

    def get_first_child(self):
        return None
        #raise IterOutOfBounds
        
class err_ele(err_node):
    """
    Name:   err_ele
    Desc:   Element Errors - Holds and generates output for element and 
            composite/sub-element errors
            Each element with an error creates a new err_ele instance.  
    """
    def __init__(self, parent, map_node):
        """
        Class:      err_ele
        Name:       __init__
        Desc:    
        Params:     
        """
        #, self.id, self.name, self.seq, self.data_ele)
        self.ele_ref_num = map_node.data_ele
        self.name = map_node.name
        if map_node.parent.is_composite():
            self.ele_pos = map_node.parent.seq
            self.subele_pos = map_node.seq
        else:
            self.ele_pos = map_node.seq
            self.subele_pos = None
            
        #self.bad_val = bad_val
        self.id = 'ELE'

        self.parent = parent
        #self.children = []
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
        #logger.debug('err_ele.add_error: %s %s %s' % (err_cde, err_str, bad_value))
        self.errors.append((err_cde, err_str, bad_value))
        
    def err_count(self):
        return len(self.errors)

    def get_error_count(self):
        return len(self.errors)

class ErrorErrhNull(Exception):
    """Class for errh_null errors."""

class errh_null:
    """
    Name:   errh_null
    Desc:   
    """
    def __init__(self):
        """
        Name:       __init__
        Class:      errh_null
        Desc:    
        Params: 
        Note:      
        """

        self.id = 'ROOT'
        #self.children = []
        self.cur_node = self
        #self.cur_isa_node = None
        #self.cur_gs_node = None
        #self.cur_st_node = None
        #self.cur_seg_node = None
        #self.seg_node_added = False
        #self.cur_ele_node = None
        self.cur_line = 0
        self.err_cde = None
        self.err_str = None

    def get_cur_line(self):
        """
        Class:      errh_null
        """
        return self.cur_line

    def get_id(self):
        """
        Class:      errh_null
        """
        return self.id

    def add_isa_loop(self, seg, src):
        """
        Class:      errh_null
        """
        raise ErrorErrhNull, 'add_isa loop'
        
    def add_gs_loop(self, seg, src):
        """
        Class:      errh_null
        """
        pass
        
    def add_st_loop(self, seg, src):
        """
        Class:      errh_null
        """
        pass
        
    def add_seg(self, map_node, seg, seg_count, cur_line, ls_id):
        """
        Class:      errh_null
        """
        pass
        
    def add_ele(self, map_node):
        """
        Class:      errh_null
        """
        pass
   
    def isa_error(self, err_cde, err_str):
        """
        Class:      errh_null
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def gs_error(self, err_cde, err_str):
        """
        Class:      errh_null
        """
        self.err_cde = err_cde
        self.err_str = err_str
        
    def st_error(self, err_cde, err_str):
        """
        Class:      errh_null
        """
        self.err_cde = err_cde
        self.err_str = err_str
        
    def seg_error(self, err_cde, err_str, err_value=None):
        """
        Class:      errh_null
        """
        self.err_cde = err_cde
        self.err_str = err_str
        
    def ele_error(self, err_cde, err_str, bad_value):
        """
        Class:      errh_null
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def close_isa_loop(self, node, seg, src):
        """
        Class:      errh_null
        """
        pass
        
    def close_gs_loop(self, node, seg, src):
        """
        Class:      errh_null
        """
        pass
        
    def close_st_loop(self, node, seg, src):
        """
        Class:      errh_null
        """
        pass
        
    def find_node(self, type):
        """
        Class:      errh_null
        Find the last node of a type
        """
        pass

    def get_parent(self):
        return None

#    def get_first_child(self):
#        """
#        Class:      errh_null
#        """
#        if len(self.children) > 0:
#            return self.children[0]
#        else:
#            return None
         
    def get_next_sibling(self):
        """
        Class:      errh_null
        """
        return None

    def get_error_count(self):
        """
        Class:      errh_null
        """
        if self.err_cde is not None:
            return 1
        else:
            return 0

    def is_closed(self):
        """
        Class:      errh_null
        """
        return True
            
    def __repr__(self):
        """
        Class:      errh_null
        """
        return '%i: %s' % (-1, self.id)
 
