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

