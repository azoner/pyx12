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
Generates a 997 Response
Visitor - Visits an error_handler composite
"""

#import os
#import sys
import string
from types import *
import time
import logging
import pdb

# Intrapackage imports
from errors import *
from utils import seg_str
import error_visitor
import pyx12.segment

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"

logger = logging.getLogger('pyx12.error_997')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class error_997_visitor(error_visitor.error_visitor):
    """
    Visit an error_handler composite.  Generate a 997.
    """
    def __init__(self, fd, term=('~', '*', '~', '\n')): 
        """
        @param fd: target file
        @type fd: file descriptor
        @param term: tuple of x12 terminators used
        @type term: tuple(string, string, string, string)
        """
        self.fd = fd
        self.seg_term = '~'
        self.ele_term = '*'
        self.subele_term = ':'
        #self.seg_term = term[0]
        #self.ele_term = term[1]
        #self.subele_term = term[2]
        #self.eol = term[3]
        self.eol = '\n'
        self.seg_count = 0
        self.st_control_num = 0

    def visit_root_pre(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        #now = time.localtime()
        seg = errh.cur_isa_node.seg_data
        #ISA*00*          *00*          *ZZ*ENCOUNTER      *ZZ*00GR           *030425*1501*U*00401*000065350*0*T*:~
        #isa_seg = ['ISA','00','          ','00','          ']
        #isa_seg.extend([seg[7],seg[8],seg[5],seg[6]])
        #isa_seg.append(time.strftime('%y%m%d')) # Date
        #isa_seg.append(time.strftime('%H%M')) # Time
        #isa_seg.extend([seg[11],seg[12]])
        self.isa_control_num = ('%s%s'%(time.strftime('%y%m%d'), time.strftime('%H%M')))[1:]
        #isa_seg.append(self.isa_control_num) # ISA Interchange Control Number
        #isa_seg.extend([seg[14],seg[15]])
        #isa_seg.append(self.subele_term)

        #logger.info('\n'+seg.format())
        #pdb.set_trace()
        isa_seg = pyx12.segment.segment('ISA*00*          *00*          ', '~', '*', ':')
        isa_seg.append(seg[6].get_value())
        isa_seg.append(seg[7].get_value())
        isa_seg.append(seg[4].get_value())
        isa_seg.append(seg[5].get_value())
        isa_seg.append(time.strftime('%y%m%d')) # Date
        isa_seg.append(time.strftime('%H%M')) # Time
        isa_seg.append(seg[10].get_value())
        isa_seg.append(seg[11].get_value())
        isa_seg.append(self.isa_control_num) # ISA Interchange Control Number
        isa_seg.append(seg[13].get_value())
        isa_seg.append(seg[14].get_value())
        isa_seg.append(self.subele_term)
        self._write(isa_seg)
        self.isa_seg = isa_seg
        self.gs_loop_count = 0

        #TA1 segment
        err_isa = errh.cur_isa_node
        if err_isa.ta1_req == '1':
            #seg = ['TA1', err_isa.isa_trn_set_id, err_isa.orig_date, \
            #    err_isa.orig_time]
            ta1_seg = pyx12.segment.segment('TA1', '~', '*', ':')
            ta1_seg.append(err_isa.isa_trn_set_id)
            ta1_seg.append(err_isa.orig_date)
            ta1_seg.append(err_isa.orig_time)
            if err_isa.errors:
                (err_cde, err_str) = err_isa.errors[0]
                #seg.extend(['R', err_cde])
                ta1_seg.append('R')
                ta1_seg.append(err_cde)
            else:
                #seg.extend(['A', '000'])
                ta1_seg.append('A')
                ta1_seg.append('000')
            self._write(ta1_seg)

        # GS*FA*ENCOUNTER*00GR*20030425*150153*653500001*X*004010
        seg = errh.cur_gs_node.seg_data
        gs_seg = pyx12.segment.segment('GS', '~', '*', ':')
        gs_seg.append('FA')
        gs_seg.append(seg[2].get_value())
        gs_seg.append(seg[1].get_value())
        gs_seg.append(time.strftime('%Y%m%d'))
        gs_seg.append(time.strftime('%H%M%S'))
        gs_seg.append(seg[5].get_value())
        gs_seg.append(seg[6].get_value())
        gs_seg.append('004010')
        #gs_str = '%s*%s*%s*%s' % (seg.get_seg_id(), 'FA', seg[2].get_value(), seg[1].get_value()) 
        #gs_str += '*%s*%s' % (time.strftime('%Y%m%d'), time.strftime('%H%M%S'))
        #gs_str += '*%s*%s*%s' % (seg[5].get_value(), seg[6].get_value(), '004010')
        #gs_str += '~'
        self._write(gs_seg)
        self.gs_seg = gs_seg
        self.gs_id = seg[5].get_value()
        #self.gs_997_count = 0
        self.st_loop_count = 0
        self.gs_loop_count += 1

    def visit_root_post(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        self._write(pyx12.segment.segment('GE*%i*%s' % (self.st_loop_count, \
            self.gs_seg[5].get_value()), '~', '*', ':'))
        #self._write(['GE', '%i' % self.st_loop_count, self.gs_seg[6]])
        self.gs_loop_count = 1
        self._write(pyx12.segment.segment('IEA*%i*%s' % \
            (self.gs_loop_count, self.isa_control_num), '~', '*', ':'))
        #self._write(['IEA', '%i' % self.gs_loop_count, self.isa_control_num]) # isa_seg[13]])
        
    def visit_isa_pre(self, err_isa):
        """
        @param err_isa: ISA Loop error handler
        @type err_isa: L{error_handler.err_isa}
        """

    def visit_isa_post(self, err_isa):
        """
        @param err_isa: ISA Loop error handler
        @type err_isa: L{error_handler.err_isa}
        """

    def visit_gs_pre(self, err_gs): 
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        #ST
        self.st_control_num += 1
        #seg = ['ST', '997', '%04i' % self.st_control_num]
        #self._write(seg)
        self._write(pyx12.segment.segment('ST*997*%04i' % \
            (self.st_control_num), '~', '*', ':'))
        self.seg_count = 0
        self.seg_count = 1
        self.st_loop_count += 1

        #AK1
        #seg = ['AK1', err_gs.fic, err_gs.gs_control_num]
        #self._write(seg)
        self._write(pyx12.segment.segment('AK1*%s*%s' % \
            (err_gs.fic, err_gs.gs_control_num), '~', '*', ':'))
        
 
    def visit_gs_post(self, err_gs): 
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        if not (err_gs.ack_code and err_gs.st_count_orig and \
            err_gs.st_count_recv):
            raise EngineError, 'err_gs variables not set'
        #.st_count_orig = None # AK902
        #.st_count_recv = None # AK903
        #.st_count_accept = None # AK904
        #.err_cde = [] # AK905-9

        #seg.append(err_st.ack_code)
#        if '1' in err_gs.errors: ack_code = 'R'
#        elif '2' in err_gs.errors: ack_code = 'R'
#        elif '3' in err_gs.errors: ack_code = 'R'
#        elif '4' in err_gs.errors: ack_code = 'R'
#        elif '5' in err_gs.errors: ack_code = 'E'
#        elif '6' in err_gs.errors: ack_code = 'E'
#        else: ack_code = 'A'

        seg_data = pyx12.segment.segment('AK9', '~', '*', ':')
        seg_data.append(err_gs.ack_code)
        seg_data.append('%i' % err_gs.st_count_orig)
        seg_data.append('%i' % err_gs.st_count_recv)
        seg_data.append('%i' % (err_gs.st_count_recv - err_gs.count_failed_st()))
        #seg = ['AK9', err_gs.ack_code, '%i' % err_gs.st_count_orig, \
        #    '%i' % err_gs.st_count_recv, \
        #    '%i' % (err_gs.st_count_recv - err_gs.count_failed_st())]
        for (err_cde, err_str) in err_gs.errors:
            seg_data.append('%s' % err_cde)
            #seg.append('%s' % err_cde)
        self._write(seg_data)
        #for child in err_gs.children:
            #print child.cur_line, child.seg
        #logger.info('err_gs has %i children' % len(self.children))
        
        #SE
        seg_count = self.seg_count + 1
        seg_data = pyx12.segment.segment('SE', '~', '*', ':')
        seg_data.append('%i' % seg_count)
        seg_data.append('%04i' % self.st_control_num)
        #seg = ['SE', '%i' % seg_count, '%04i' % self.st_control_num]
        self._write(seg_data)

    def visit_st_pre(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        seg_data = pyx12.segment.segment('AK2', '~', '*', ':')
        seg_data.append(err_st.trn_set_id)
        seg_data.append(err_st.trn_set_control_num)
        self._write(seg_data)
        
    def visit_st_post(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        if err_st.ack_code is None:
            raise EngineError, 'err_st.ack_cde variable not set'
#        self.ack_code = None # AK501
        seg_data = pyx12.segment.segment('AK5', '~', '*', ':')
        #seg = ['AK5']
#        self.err_cde = [] # AK502-6
        err_codes = []
        if err_st.child_err_count() > 0:
            err_codes.append('5')
        for (err_cde, err_str) in err_st.errors:
            err_codes.append(err_cde)
        #seg.append(err_st.ack_code)
        seg_data.append(err_st.ack_code)
        err_codes.sort()
        for i in range(min(len(err_codes),5)):
            seg_data.append(err_codes[i])
            #seg.append(err_codes[i])
        self._write(seg_data)

    def visit_seg(self, err_seg):
        """
        @param err_seg: Segment error handler
        @type err_seg: L{error_handler.err_seg}
        """
        #logger.debug('visit_deg: AK3 - ')
        #seg_base = ['AK3', err_seg.seg_id, '%i' % err_seg.seg_count]
        seg_base = pyx12.segment.segment('AK3', '~', '*', ':')
        seg_base.append(err_seg.seg_id)
        seg_base.append('%i' % err_seg.seg_count)
        if err_seg.ls_id:
            seg_base.append(err_seg.ls_id)
        else:
            seg_base.append('')
        seg_str = seg_base.format('~', '*', ':')
        for (err_cde, err_str, err_value) in err_seg.errors:
            seg_data = pyx12.segment.segment(seg_str, '~', '*', ':')
            seg_data.append(err_cde)
            self._write(seg_data)
        if err_seg.child_err_count() > 0:
            seg_data = pyx12.segment.segment(seg_str, '~', '*', ':')
            seg_data.append('8')
            self._write(seg_data)
        
    def visit_ele(self, err_ele): 
        """
        @param err_ele: Segment error handler
        @type err_ele: L{error_handler.err_ele}
        """
        seg_base = pyx12.segment.segment('AK4', '~', '*', ':')
        if err_ele.subele_pos: 
            seg_base.append('%i:%i' % (err_ele.ele_pos, err_ele.subele_pos))
        else:
            seg_base.append('%i' % (err_ele.ele_pos))
        if err_ele.ele_ref_num:
            seg_base.append(err_ele.ele_ref_num)
        else:
            seg_base.append('')
        seg_str = seg_base.format('~', '*', ':')
        for (err_cde, err_str, bad_value) in err_ele.errors:
            seg_data = pyx12.segment.segment(seg_str, '~', '*', ':')
            seg_data.append(err_cde)
            if bad_value:
                seg_data.append(bad_value)
            self._write(seg_data)

    def _write(self, seg_data):
        """
        Params:     seg_data - 
        @param seg_data: Data segment instance
        @type seg_data: L{segment.segment}
        """
        self.fd.write('%s\n' % (seg_data.format(self.seg_term, self.ele_term, \
            self.subele_term)))
        self.seg_count += 1
