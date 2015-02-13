######################################################################
# Copyright (c) 
#   John Holland <john@zoner.org>
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

# Intrapackage imports
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
            print((ele.parent))
            for err in ele.errors:
                self.fd.write('    ERR %s %s (%s)\n' % err)

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
            for err in ele.errors:
                self.fd.write('    ERR %s %s (%s)\n' % err)

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
        self.fd.write(' GS st_count_orig%s\n' % err_gs.st_count_orig)
        self.fd.write(' GS st_count_recv%i\n' % err_gs.st_count_recv)
        self.fd.write(' GS st_count_accept%i\n' % (
            err_gs.st_count_recv - err_gs.count_failed_st()))

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
            for err in ele.errors:
                self.fd.write('    ERR %s %s (%s)\n' % err)

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
        self.fd.write('%s %s %s %s\n' % (err_seg.id, err_seg.name,
                                         err_seg.get_cur_line(), err_seg.seg_id))
        for (err_cde, err_str, err_value) in err_seg.errors:
            self.fd.write('  ERR %s (%s) "%s" \n' % (err_cde,
                                                     err_value, err_str))
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
