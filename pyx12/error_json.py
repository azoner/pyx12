######################################################################
# Copyright (c) SWMBH,
#   John Holland <john.holland@swmbh.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Generates error debug output
Visitor - Visits an error_handler composite
"""

import logging

# Intrapackage imports
from error_visitor import error_visitor

ISA_ELE_ERR_MAP = {1: '010', 2: '011', 3: '012', 4: '013', 5: '005', 6: '006',
                    7: '007', 8: '008', 9: '014', 10: '015', 11: '016', 12: '017', 13: '018',
                    14: '019', 15: '020', 16: '027'
                    }
IEA_ELE_ERR_MAP = {1: '021', 2: '018'}


class error_json_visitor(pyx12.error_visitor.error_visitor):
    """
    Visit an error_handler composite.  Generate a JSON file of error detail
    """
    def __init__(self, fd):
        """
        @param fd: target file
        @type fd: file descriptor
        """
        self.fd = fd
        self.logger = logging.getLogger('pyx12.error_json')
        self.logger.setLevel(logging.DEBUG)
        #self.seg_count = 0
        #self.st_control_num = 0
        self.errors = []

    def visit_root_pre(self, errh):
        """
        @param errh: Error_handler instance
        @type errh: L{error_handler.err_handler}
        """
        #self.fd.write('%s\n' % errh.id)
        self.logger.debug('%s\n' % errh.id)

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
        pass

    def _get_isa_code_by_position(self, err_str, pos):
        if 'ISA' in err_str:
            return ISA_ELE_ERR_MAP[pos]
        elif 'IEA' in err_str:
            return IEA_ELE_ERR_MAP[pos]

    def visit_isa_post(self, err_isa):
        """
        @param err_isa: ISA Loop error handler
        @type err_isa: L{error_handler.err_isa}
        """
        line_num = err_isa.cur_line_isa
        for (err_cde, err_str, err_value) in err_isa.errors:
            self.errors.append(self._get_error_dict(line_num, err_cde, err_str))
        for ele in err_isa.elements:
            #self.fd.write(' %s %s\n' % (ele.id, ele.name))
            #print((ele.parent))
            for (err_cde, err_str, bad_value) in ele.errors:
                #code = self._get_isa_code_by_position(err_str, elem.ele_pos)
                self.errors.append(self._get_error_dict(line_num, err_cde, err_str, '', bad_value))
                #self.logger.info('%s %s (%s)\n' % (err_cde, err_str, bad_value))

    def visit_gs_pre(self, err_gs):
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        pass

    def _get_gs_code_by_position(self, err_str, pos):
        gs_ele_err_map = {6: '6', 8: '2'}
        ge_ele_err_map = {2: '6'}
        if 'GS' in err_str:
            return gs_ele_err_map[pos]
        elif 'GE' in err_str:
            return ge_ele_err_map[pos]

    def visit_gs_post(self, err_gs):
        """
        @param err_gs: GS Loop error handler
        @type err_gs: L{error_handler.err_gs}
        """
        line_num = err_gs.cur_line_gs
        for (err_cde, err_str) in err_gs.errors:
            self.errors.append(self._get_error_dict(line_num, err_cde, err_str))
        for ele in err_gs.elements:
            for (err_cde, err_str, bad_value) in ele.errors:
                #code = self._get_gs_code_by_position(err_str, elem.ele_pos)
                self.errors.append(self._get_error_dict(line_num, err_cde, err_str, '', bad_value))
                #self.logger.info('%s %s (%s)\n' % (err_cde, err_str, bad_value))

    def visit_st_pre(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        pass
        self.fd.write('%s\n' % err_st.id)
        self.fd.write('-- ST errors --\n')
        for err in err_st.errors:
            self.fd.write('  ERR %s %s\n' % err)
        for ele in err_st.elements:
            self.fd.write('  ST Element:  %s %s\n' % (ele.id, ele.name))
            for err in ele.errors:
                self.fd.write('    ERR %s %s (%s)\n' % err)

    def visit_st_post(self, err_st):
        """
        @param err_st: ST Loop error handler
        @type err_st: L{error_handler.err_st}
        """
        line_num = err_st.cur_line_st
        for (err_cde, err_str) in err_st.errors:
            self.errors.append(self._get_error_dict(line_num, err_cde, err_str))
        for ele in err_st.elements:
            for (err_cde, err_str, bad_value) in ele.errors:
                #code = self._get_gs_code_by_position(err_str, elem.ele_pos)
                self.errors.append(self._get_error_dict(line_num, err_cde, err_str, '', bad_value))
                #self.logger.info('%s %s (%s)\n' % (err_cde, err_str, bad_value))
        

    def visit_seg(self, err_seg):
        """
        @param err_seg: Segment error handler
        @type err_seg: L{error_handler.err_seg}
        """
        #pdb.set_trace()
        self.fd.write('%s %s %s %s\n' % (err_seg.id, err_seg.name,
                                         err_seg.get_cur_line(), err_seg.seg_id))
        for (err_cde, err_str, err_value) in err_seg.errors:
            self.fd.write('  ERR %s (%s) "%s" \n' % (err_cde,
                                                     err_value, err_str))
        #for ele in err_seg.elements:
        #    self.fd.write(' %s %s\n' % (ele.id, ele.name))

    def visit_ele(self, err_ele):
        """
        Params:     err_ele - error_ele instance
        @param err_ele: Element error handler
        @type err_ele: L{error_handler.err_ele}
        """
        self.fd.write('  %s %s\n' % (err_ele.id, err_ele.name))
        for err in err_ele.errors:
            self.fd.write('    ERR %s %s (%s)\n' % err)

    def _get_error_dict(self, line_number, code, message, fieldname='', bad_value='', log_level='ERROR'):
        return {
            'LogLevel': log_level,
            'LogMessage': message,
            'LineNumber': line_number,
            'ErrorCode': code,
            'ErrorFieldName': fieldname,
            'ErrorValue': bad_value
        }