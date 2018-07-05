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
Visitor - Visits an error_handler composite
"""


class error_visitor(object):
    """
    """

    def __init__(self, fd):
        """
        Params:     fd - target file
        """
        pass

    def visit_root_pre(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        pass

    def visit_root_post(self, errh):
        """
        @param errh: Error handler
        @type errh: L{error_handler.err_handler}
        """
        pass

    def visit_isa_pre(self, err_isa):
        pass

    def visit_isa_post(self, err_isa):
        """
        Params:     err_isa - error_isa instance
        """
        pass

    def visit_gs_pre(self, err_gs):
        pass

    def visit_gs_post(self, err_gs):
        """
        Params:     err_gs - error_gs instance
        """
        pass

    def visit_st_pre(self, err_st):
        pass

    def visit_st_post(self, err_st):
        """
        Params:     err_st - error_st instance
        """
        pass

    def visit_seg(self, err_seg):
        """
        Params:     err_seg - error_seg instance
        """
        pass

    def visit_ele(self, err_ele):
        """
        Params:     err_ele - error_ele instance
        """
        pass
