######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Generates a 997 Response
Visitor - Visits an error_handler composite
"""

#import os
#import sys
from types import *
import time
import logging
import pdb

# Intrapackage imports
from errors import *
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
        self.isa_control_num = ('%s%s'%(time.strftime('%y%m%d'), time.strftime('%H%M')))[1:]

        #logger.info('\n'+seg.format())
        #pdb.set_trace()
        isa_seg = pyx12.segment.Segment('ISA*00*          *00*          ', '~', '*', ':')
        isa_seg.append(seg.get_value('ISA07'))
        isa_seg.append(seg.get_value('ISA08'))
        isa_seg.append(seg.get_value('ISA05'))
        isa_seg.append(seg.get_value('ISA06'))
        isa_seg.append(time.strftime('%y%m%d')) # Date
        isa_seg.append(time.strftime('%H%M')) # Time
        isa_seg.append(seg.get_value('ISA11'))
        isa_seg.append(seg.get_value('ISA12'))
        isa_seg.append(self.isa_control_num) # ISA Interchange Control Number
        isa_seg.append(seg.get_value('ISA14'))
        isa_seg.append(seg.get_value('ISA15'))
        isa_seg.append(self.subele_term)
        self._write(isa_seg)
        self.isa_seg = isa_seg
        self.gs_loop_count = 0

        # GS*FA*ENCOUNTER*00GR*20030425*150153*653500001*X*004010
        seg = errh.cur_gs_node.seg_data
        gs_seg = pyx12.segment.Segment('GS', '~', '*', ':')
        gs_seg.append('FA')
        gs_seg.append(seg.get_value('GS03').rstrip())
        gs_seg.append(seg.get_value('GS02').rstrip())
        gs_seg.append(time.strftime('%Y%m%d'))
        gs_seg.append(time.strftime('%H%M%S'))
        gs_seg.append(seg.get_value('GS06'))
        gs_seg.append(seg.get_value('GS07'))
        gs_seg.append('004010')
        self._write(gs_seg)
        self.gs_seg = gs_seg
        self.gs_id = seg.get_value('GS06')
        #self.gs_997_count = 0
        self.st_loop_count = 0
        self.gs_loop_count += 1

    def visit_root_post(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        self._write(pyx12.segment.Segment('GE*%i*%s' % (self.st_loop_count, \
            self.gs_seg.get_value('GS06')), '~', '*', ':'))
        self.gs_loop_count = 1

        #pdb.set_trace()
        #TA1 segment
        err_isa = errh.cur_isa_node
        if err_isa.ta1_req == '1':
            #seg = ['TA1', err_isa.isa_trn_set_id, err_isa.orig_date, \
            #    err_isa.orig_time]
            ta1_seg = pyx12.segment.Segment('TA1', '~', '*', ':')
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
        
        self._write(pyx12.segment.Segment('IEA*%i*%s' % \
            (self.gs_loop_count, self.isa_control_num), '~', '*', ':'))
        
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
        self._write(pyx12.segment.Segment('ST*997*%04i' % \
            (self.st_control_num), '~', '*', ':'))
        self.seg_count = 0
        self.seg_count = 1
        self.st_loop_count += 1

        #AK1
        #seg = ['AK1', err_gs.fic, err_gs.gs_control_num]
        #self._write(seg)
        self._write(pyx12.segment.Segment('AK1*%s*%s' % \
            (err_gs.fic, err_gs.gs_control_num), '~', '*', ':'))
        
 
    def visit_gs_post(self, err_gs): 
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        if not (err_gs.ack_code and err_gs.st_count_orig and \
            err_gs.st_count_recv):
            #raise EngineError, 'err_gs variables not set'
            if not err_gs.ack_code:
                err_gs.ack_code = 'R'
            if not err_gs.st_count_orig:
                err_gs.st_count_orig = 0
            if not err_gs.st_count_recv:
                err_gs.st_count_recv = 0
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

        seg_data = pyx12.segment.Segment('AK9', '~', '*', ':')
        seg_data.append(err_gs.ack_code)
        seg_data.append('%i' % err_gs.st_count_orig)
        seg_data.append('%i' % err_gs.st_count_recv)
        count_ok = max(err_gs.st_count_recv - err_gs.count_failed_st(), 0)
        seg_data.append('%i' % (count_ok))
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
        seg_data = pyx12.segment.Segment('SE', '~', '*', ':')
        seg_data.append('%i' % seg_count)
        seg_data.append('%04i' % self.st_control_num)
        #seg = ['SE', '%i' % seg_count, '%04i' % self.st_control_num]
        self._write(seg_data)

    def visit_st_pre(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        seg_data = pyx12.segment.Segment('AK2', '~', '*', ':')
        seg_data.append(err_st.trn_set_id)
        seg_data.append(err_st.trn_set_control_num.strip())
        self._write(seg_data)
        
    def visit_st_post(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        if err_st.ack_code is None:
            raise EngineError, 'err_st.ack_cde variable not set'
#        self.ack_code = None # AK501
        seg_data = pyx12.segment.Segment('AK5', '~', '*', ':')
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
        valid_AK3_codes = ('1', '2', '3', '4', '5', '6', '7', '8')
        seg_base = pyx12.segment.Segment('AK3', '~', '*', ':')
        seg_base.append(err_seg.seg_id)
        seg_base.append('%i' % err_seg.seg_count)
        if err_seg.ls_id:
            seg_base.append(err_seg.ls_id)
        else:
            seg_base.append('')
        seg_str = seg_base.format('~', '*', ':')
        errors = [x[0] for x in err_seg.errors]
        if 'SEG1' in errors:
            if '8' not in errors:
                errors.append('8')
            errors = filter(lambda x: x!='SEG1', errors)
        for err_cde in list(set(errors)):
            if err_cde in valid_AK3_codes: # unique codes
                seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
                seg_data.set('AK304', err_cde)
                self._write(seg_data)
        if err_seg.child_err_count() > 0 and '8' not in errors:
            seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
            seg_data.set('AK304', '8')
            self._write(seg_data)
        
    def visit_ele(self, err_ele): 
        """
        @param err_ele: Segment error handler
        @type err_ele: L{error_handler.err_ele}
        """
        valid_AK4_codes = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        seg_base = pyx12.segment.Segment('AK4', '~', '*', ':')
        if err_ele.subele_pos: 
            seg_base.append('%i:%i' % (err_ele.ele_pos, err_ele.subele_pos))
        else:
            seg_base.append('%i' % (err_ele.ele_pos))
        if err_ele.ele_ref_num:
            seg_base.append(err_ele.ele_ref_num)
        #else:
        #    seg_base.append('')
        seg_str = seg_base.format('~', '*', ':')
        for (err_cde, err_str, bad_value) in err_ele.errors:
            if err_cde in valid_AK4_codes:
                seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
                seg_data.set('AK403', err_cde)
                if bad_value:
                    seg_data.set('AK404', bad_value)
                self._write(seg_data)

    def _write(self, seg_data):
        """
        Params:     seg_data - 
        @param seg_data: Data segment instance
        @type seg_data: L{segment.Segment}
        """
        self.fd.write('%s\n' % (seg_data.format(self.seg_term, self.ele_term, \
            self.subele_term)))
        self.seg_count += 1
