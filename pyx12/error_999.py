######################################################################
# Copyright 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Generates a 999 Response
Visitor - Visits an error_handler composite
"""

import time
import logging
import random

# Intrapackage imports
from pyx12.errors import EngineError
import pyx12.error_visitor
import pyx12.segment
import pyx12.x12file

logger = logging.getLogger('pyx12.error_999')
logger.setLevel(logging.DEBUG)


class error_999_visitor(pyx12.error_visitor.error_visitor):
    """
    Visit an error_handler composite.  Generate a 999.
    """
    def __init__(self, fd, term=('~', '*', ':', '\n', '^')):
        """
        @param fd: target file
        @type fd: file descriptor
        @param term: tuple of x12 terminators used
        @type term: tuple(string, string, string, string)
        """
        self.fd = fd
        self.wr = pyx12.x12file.X12Writer(fd, '~', '*', ':', '\n', '^')
        self.seg_term = '~'
        self.ele_term = '*'
        self.subele_term = ':'
        self.repetition_term = '^'
        self.eol = '\n'
        self.isa_control_num = None
        self.gs_control_num = None
        self.st_control_num = 0
        self.vriic = '005010X231'


    def visit_root_pre(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}

        Uses:
        isa_node seg_data
        gs_node seg_data
        """
        seg = errh.cur_isa_node.seg_data
        #ISA*00*          *00*          *ZZ*ENCOUNTER      *ZZ*00GR           *030425*1501*U*00501*000065350*0*T*:~
        self.isa_control_num = ('%s%s' % (time.strftime('%y%m%d'),
                                          time.strftime('%H%M')))[1:]
        self.gs_control_num = '%i' % (random.randint(10000000, 999999999))
        icvn = seg.get_value('ISA12')
        isa_seg = pyx12.segment.Segment('ISA*00*          *00*          ',
                                        self.seg_term, self.ele_term, self.subele_term)
        isa_seg.set('05', seg.get_value('ISA07'))
        isa_seg.set('06', seg.get_value('ISA08'))
        isa_seg.set('07', seg.get_value('ISA05'))
        isa_seg.set('08', seg.get_value('ISA06'))
        isa_seg.set('09', time.strftime('%y%m%d'))  # Date
        isa_seg.set('10', time.strftime('%H%M'))  # Time
        isa_seg.set('11', self.repetition_term)
        isa_seg.set('12', icvn)
        isa_seg.set('13', self.isa_control_num)  # ISA Interchange Control Number
        isa_seg.set('14', seg.get_value('ISA14'))
        isa_seg.set('15', seg.get_value('ISA15'))
        isa_seg.set('16', self.subele_term)
        self.wr.Write(isa_seg)

        # GS*FA*ENCOUNTER*00GR*20030425*150153*653500001*X*005010
        seg = errh.cur_gs_node.seg_data
        gs_seg = pyx12.segment.Segment('GS', '~', '*', ':')
        gs_seg.set('01', 'FA')
        gs_seg.set('02', seg.get_value('GS03').rstrip())
        gs_seg.set('03', seg.get_value('GS02').rstrip())
        gs_seg.set('04', time.strftime('%Y%m%d'))
        gs_seg.set('05', time.strftime('%H%M%S'))
        gs_seg.set('06', self.gs_control_num)
        gs_seg.set('07', seg.get_value('GS07'))
        gs_seg.set('08', self.vriic)
        self.wr.Write(gs_seg)

    def __get_isa_errors(self, err_isa):
        """
        Build list of TA1 level errors
        Only the first error is used
        """
        isa_ele_err_map = {1: '010', 2: '011', 3: '012', 4: '013', 5: '005', 6: '006',
                           7: '007', 8: '008', 9: '014', 10: '015', 11: '016', 12: '017', 13: '018',
                           14: '019', 15: '020', 16: '027'
                           }
        iea_ele_err_map = {1: '021', 2: '018'}
        err_codes = [err[0] for err in err_isa.errors]
        for elem in err_isa.elements:
            for (err_cde, err_str, bad_value) in elem.errors:
                # Ugly
                if 'ISA' in err_str:
                    err_codes.append(isa_ele_err_map[elem.ele_pos])
                elif 'IEA' in err_str:
                    err_codes.append(iea_ele_err_map[elem.ele_pos])
        # return unique codes
        return list(set(err_codes))

    def visit_root_post(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        ge = pyx12.segment.Segment('GE', '~', '*', ':')
        ge.set('02', self.gs_control_num)
        self.wr.Write(ge)

        #TA1 segment
        err_isa = errh.cur_isa_node
        if err_isa.ta1_req == '1':
            #seg = ['TA1', err_isa.isa_trn_set_id, err_isa.orig_date, \
            #    err_isa.orig_time]
            ta1_seg = pyx12.segment.Segment('TA1', '~', '*', ':')
            ta1_seg.append(err_isa.isa_trn_set_id)
            ta1_seg.append(err_isa.orig_date)
            ta1_seg.append(err_isa.orig_time)
            err_codes = self.__get_isa_errors(err_isa)
            if err_codes:
                err_cde = err_codes[0]
                ta1_seg.append('R')
                ta1_seg.append(err_cde)
            else:
                ta1_seg.append('A')
                ta1_seg.append('000')
            self.wr.Write(ta1_seg)
        self.wr.Write(pyx12.segment.Segment('IEA', '~', '*', ':'))

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
        pass

    def visit_gs_pre(self, err_gs):
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        #ST
        self.st_control_num += 1
        st_seg = pyx12.segment.Segment('ST*999', '~', '*', ':')
        st_seg.set('02', '%04i' % (self.st_control_num))
        st_seg.set('03', self.vriic)
        self.wr.Write(st_seg)
        ak1 = pyx12.segment.Segment('AK1', '~', '*', ':')
        ak1.set('01', err_gs.fic)
        ak1.set('02', err_gs.gs_control_num)
        ak1.set('03', err_gs.vriic)
        self.wr.Write(ak1)

    def __get_gs_errors(self, err_gs):
        """
        Build list of GS level errors
        """
        gs_ele_err_map = {6: '6', 8: '2'}
        ge_ele_err_map = {2: '6'}
        err_codes = [err[0] for err in err_gs.errors]
        for elem in err_gs.elements:
            for (err_cde, err_str, bad_value) in elem.errors:
                # Ugly
                if 'GS' in err_str:
                    if elem.ele_pos in gs_ele_err_map:
                        err_codes.append(gs_ele_err_map[elem.ele_pos])
                    else:
                        err_codes.append('1')
                elif 'GE' in err_str:
                    if elem.ele_pos in ge_ele_err_map:
                        err_codes.append(ge_ele_err_map[elem.ele_pos])
                    else:
                        err_codes.append('1')
        # return unique codes
        ret = list(set(err_codes))
        ret.sort()
        return ret

    def visit_gs_post(self, err_gs):
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        if not (err_gs.ack_code and err_gs.st_count_orig and
                err_gs.st_count_recv):
            if not err_gs.ack_code:
                err_gs.ack_code = 'R'
            if not err_gs.st_count_orig:
                err_gs.st_count_orig = 0
            if not err_gs.st_count_recv:
                err_gs.st_count_recv = 0

        seg_data = pyx12.segment.Segment('AK9', '~', '*', ':')
        seg_data.set('01', err_gs.ack_code)
        seg_data.set('02', '%i' % err_gs.st_count_orig)
        seg_data.set('03', '%i' % err_gs.st_count_recv)
        count_ok = max(err_gs.st_count_recv - err_gs.count_failed_st(), 0)
        seg_data.set('04', '%i' % (count_ok))
        err_codes = self.__get_gs_errors(err_gs)
        for err_cde in err_codes[:5]:
            seg_data.append(err_cde)
        self.wr.Write(seg_data)

        #SE
        seg_data = pyx12.segment.Segment('SE', '~', '*', ':')
        seg_data.append('%i' % (0))
        seg_data.append('%04i' % self.st_control_num)
        self.wr.Write(seg_data)

    def visit_st_pre(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        if err_st is None:
            raise EngineError('Cannot create AK2 : err_st is None')
        if err_st.trn_set_id is None:
            raise EngineError('Cannot create AK2: err_st.trn_set_id was not set')
        if err_st.trn_set_control_num is None:
            raise EngineError('Cannot create AK2: err_st.trn_set_control_num was not set')
        if err_st.vriic is None:
            raise EngineError('Cannot create AK2: err_st.vriic was not set')
        seg_data = pyx12.segment.Segment('AK2', '~', '*', ':')
        seg_data.set('01', err_st.trn_set_id)
        seg_data.set('02', err_st.trn_set_control_num.strip())
        seg_data.set('03', err_st.vriic)
        self.wr.Write(seg_data)

    def __get_st_errors(self, err_st):
        """
        Build list of ST level errors
        """
        st_ele_err_map = {1: '6', 2: '7'}
        se_ele_err_map = {1: '6', 2: '7'}
        err_codes = [err[0] for err in err_st.errors]
        if err_st.child_err_count() > 0:
            err_codes.append('5')
        for elem in err_st.elements:
            for (err_cde, err_str, bad_value) in elem.errors:
                # Ugly
                if 'ST' in err_str:
                    err_codes.append(st_ele_err_map[elem.ele_pos])
                elif 'SE' in err_str:
                    err_codes.append(se_ele_err_map[elem.ele_pos])
        # return unique codes
        ret = list(set(err_codes))
        ret.sort()
        return ret

    def visit_st_post(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        if err_st.ack_code is None:
            raise EngineError('err_st.ack_cde variable not set')
        seg_data = pyx12.segment.Segment('IK5', '~', '*', ':')
        seg_data.set('01', err_st.ack_code)
        err_codes = self.__get_st_errors(err_st)
        for err_code in err_codes[:5]:
            seg_data.append(err_code)
        self.wr.Write(seg_data)

    def visit_seg(self, err_seg):
        """
        @param err_seg: Segment error handler
        @type err_seg: L{error_handler.err_seg}
        """
        valid_IK3_codes = ('1', '2', '3', '4', '5', '6', '7', '8', 'I4', 'I6', 'I7', 'I8', 'I9')
        seg_base = pyx12.segment.Segment('IK3', '~', '*', ':')
        seg_base.set('01', err_seg.seg_id)
        seg_base.set('02', '%i' % err_seg.seg_count)
        if err_seg.ls_id:
            seg_base.set('03', err_seg.ls_id)
        #else:
        #    seg_base.set('')
        seg_str = seg_base.format('~', '*', ':')
        errors = [x[0] for x in err_seg.errors]
        if 'SEG1' in errors:
            if '8' not in errors:
                errors.append('8')
            errors = [x for x in errors if x != 'SEG1']
        for err_cde in list(set(errors)):
            if err_cde in valid_IK3_codes:  # unique codes
                seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
                seg_data.set('IK304', err_cde)
                self.wr.Write(seg_data)
# todo: add segment context
# todo: add business unit context
        if err_seg.child_err_count() > 0 and '8' not in errors:
            seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
            seg_data.set('IK304', '8')
            self.wr.Write(seg_data)

    def visit_ele(self, err_ele):
        """
        @param err_ele: Segment error handler
        @type err_ele: L{error_handler.err_ele}
        """
        valid_IK4_codes = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '12', '13',
                           'I10', 'I11', 'I12', 'I13', 'I6', 'I9')
        seg_base = pyx12.segment.Segment('IK4', '~', '*', ':')
        seg_base.set('01-1', '%i' % (err_ele.ele_pos))
        if err_ele.subele_pos:
            seg_base.set('01-2', '%i' % (err_ele.subele_pos))
        if err_ele.repeat_pos:
            seg_base.set('01-3', '%i' % (err_ele.repeat_pos))
        if err_ele.ele_ref_num:
            seg_base.set('02', err_ele.ele_ref_num)
        seg_str = seg_base.format('~', '*', ':')
        for (err_cde, err_str, bad_value) in err_ele.errors:
            if err_cde in valid_IK4_codes:
                seg_data = pyx12.segment.Segment(seg_str, '~', '*', ':')
                seg_data.set('IK403', err_cde)
                if bad_value:
                    seg_data.set('IK404', bad_value)
# todo: add element context
                self.wr.Write(seg_data)
