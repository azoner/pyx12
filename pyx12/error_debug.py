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
Generates error debug output
Visitor - Visits an error_handler composite
"""

#import os
import sys
import string
from types import *
#import time
import pdb

# Intrapackage imports
from errors import *
from utils import seg_str
from error_visitor import error_visitor

class error_debug_visitor(error_visitor):
    """
    
    """
    def __init__(self, fd):
        """
        @param fd: target file
        @type fd: file descriptor
        """
        self.fd = fd
        self.seg_count = 0
        self.st_control_num = 0

    def visit_root_pre(self, errh):
        """
        @param errh: Error_handler instance
        @type errh: L{error_handler.err_handler}
        """
        self.fd.write('%s\n' % errh.id)
        
    def visit_root_post(self, errh):
        """
        @param errh: Error_handler instance
        @type errh: L{error_handler.err_handler}
        """
        pass
        
    def visit_isa_pre(self, err_isa):
        """
        @param err_isa: ISA Loop error handler
        @type err_isa: L{error_handler.err_isa}
        """
        self.fd.write('%s\n' % err_isa.id)
        self.fd.write('-- ISA errors --\n')
        for err in err_isa.errors:
            self.fd.write('  %s %s\n' % err)
        for ele in err_isa.elements:
            self.fd.write('  %s %s\n' % (ele.id, ele.name))
            

    def visit_isa_post(self, err_isa):
        """
        @param err_isa: ISA Loop error handler
        @type err_isa: L{error_handler.err_isa}
        """
        pass

    def visit_gs_pre(self, err_gs): 
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        self.fd.write('%s\n' % err_gs.id)
        self.fd.write('-- GS errors --\n')
        for err in err_gs.errors:
            self.fd.write('  %s %s\n' % err)
        for ele in err_gs.elements:
            self.fd.write('  %s %s\n' % (ele.id, ele.name))

    def visit_gs_post(self, err_gs): 
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """

        self.fd.write('%s POST\n' % err_gs.id)
        #AK9
        #seg = ['AK9', err_gs.ack_code, '%i' % err_gs.st_count_orig, \
        #    '%i' % err_gs.st_count_recv, '%i' % (err_gs.st_count_recv - err_gs.count_failed_st())]
        self.fd.write(' GS Ack Code%s\n' % err_gs.ack_code)
        self.fd.write(' GS st_count_orig%i\n' % err_gs.st_count_orig)
        self.fd.write(' GS st_count_recv%i\n' % err_gs.st_count_recv)
        self.fd.write(' GS st_count_accept%i\n' % (err_gs.st_count_recv - err_gs.count_failed_st()))

    def visit_st_pre(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        self.fd.write('%s\n' % err_st.id)
        self.fd.write('-- ST errors --\n')
        for err in err_st.errors:
            self.fd.write('  ERR %s %s\n' % err)
        for ele in err_st.elements:
            self.fd.write('  ST Element:  %s %s\n' % (ele.id, ele.name))
        
    def visit_st_post(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        pass

    def visit_seg(self, err_seg):
        """
        @param err_seg: Segment error handler
        @type err_seg: L{error_handler.err_seg}
        """
        #pdb.set_trace()
        self.fd.write('%s %s %s %s\n' % (err_seg.id, err_seg.name, err_seg.get_cur_line(), err_seg.seg_id))
        for (err_cde, err_str, err_value) in err_seg.errors:
            self.fd.write('  ERR %s (%s) "%s" \n' % (err_cde, err_value, err_str))
        #for ele in err_seg.elements:
        #    self.fd.write('  %s %s\n' % (ele.id, ele.name))

    def visit_ele(self, err_ele): 
        """
        Params:     err_ele - error_ele instance
        @param err_ele: Element error handler
        @type err_ele: L{error_handler.err_ele}
        """
        self.fd.write('  %s %s\n' % (err_ele.id, err_ele.name))
        for err in err_ele.errors:
            self.fd.write('    ERR %s %s (%s)\n' % err)
