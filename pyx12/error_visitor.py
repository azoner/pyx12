######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Visitor - Visits an error_handler composite
"""

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"


class error_visitor:
    """
    Class:      error_visitor
    Desc:    
    """

    def __init__(self, fd):
        """
        Class:      error_visitor
        Name:       __init__
        Desc:    
        Params:     fd - target file
        """
        pass

    def visit_root_pre(self, err_handler):
        pass
    def visit_root_post(self, err_handler):
        """
        Class:      error_visitor
        Name:       visit_root
        Desc:    
        Params:     err_handler - error_handler instance
        """
        pass

    def visit_isa_pre(self, err_isa):
        pass
    def visit_isa_post(self, err_isa):
        """
        Class:      error_visitor
        Name:       visit_isa
        Desc:    
        Params:     err_isa - error_isa instance
        """
        pass

    def visit_gs_pre(self, err_gs):
        pass
    def visit_gs_post(self, err_gs):
        """
        Class:      error_visitor
        Name:       visit_gs
        Desc:    
        Params:     err_gs - error_gs instance
        """
        pass

    def visit_st_pre(self, err_st):
        pass
    def visit_st_post(self, err_st):
        """
        Class:      error_visitor
        Name:       visit_st
        Desc:    
        Params:     err_st - error_st instance
        """
        pass

    def visit_seg(self, err_seg):
        """
        Class:      error_visitor
        Name:       visit_seg
        Desc:    
        Params:     err_seg - error_seg instance
        """
        pass

    def visit_ele(self, err_ele):
        """
        Class:      error_visitor
        Name:       visit_ele
        Desc:    
        Params:     err_ele - error_ele instance
        """
        pass

