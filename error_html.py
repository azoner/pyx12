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
Generates HTML error output
"""

#import os
#import sys
import string
from types import *
import time
import logging

# Intrapackage imports
from errors import *
from x12file import seg_str

__author__  = "John Holland <jholland@kazoocmh.org> <john@zoner.org>"

logger = logging.getLogger('pyx12.error_html')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)





class error_html_visitor(error_visitor.error_visitor):
    """
    Class:      error_html_visitor
    Desc:    
    """
    def __init__(self, fd, src, term=('~', '*', '~', '\n')): 
        """
        Class:      error_html_visitor
        Name:       __init__
        Desc:    
        Params:     fd - target file
                    src = x12 source file
                    term - tuple of x12 terminators used
        """
        self.fd = fd
        self.src = src
        (self.seg_term, self.ele_term, self.subele_term) = src.get_term()
        self.eol = ''
        self.cur_line = 0

        self.fd.write('<html>\n<head>\n')
        self.fd.write('<title>pyx12 Error Analysis</title>\n')
        self.fd.write('<style type="text/css">\n<!--\n')
        self.fd.write('  span.seg { color: black; font-style: normal; }\n')
        self.fd.write('  span.error { background-color: #CCCCFF; color: red; font-style: normal; }\n')
        self.fd.write('-->\n</style>\n')
        self.fd.write('</head>\n<body>\n')
        self.fd.write('<h1>pyx12 Error Analysis</h1>\n<h3>Analysis Date: %s</h3><p>\n' % \
            (time.strftime('%y%m%d %H%M%S')))
        self.fd.write('<div class="segs" style="">\n')

    def __del__(self):
        self.fd.write('</div>\n')
        self.fd.write('<p>\n<a href="http://sourceforge.net/projects/pyx12/">pyx12 project page</a>\n</p>\n')
        self.fd.write('</body>\n</html>\n')

    def visit_root_pre(self, errh):
        """
        Class:      error_html_visitor 
        Name:       visit_root_pre
        Desc:    
        Params:     errh - error_handler instance
        """

    def visit_root_post(self, errh):
        """
        Class:      error_html_visitor 
        Name:       visit_root_post
        Desc:    
        Params:     errh - error_handler instance
        """
        
    def visit_isa_pre(self, err_isa):
        """
        Class:      error_html_visitor
        Name:       visit_isa_pre
        Desc:    
        Params:     err_isa - error_isa instance
        """

    def visit_isa_post(self, err_isa):
        """
        Class:      error_html_visitor
        Name:       visit_isa_post
        Desc:    
        Params:     err_isa - error_isa instance
        """

    def visit_gs_pre(self, err_gs): 
        """
        Class:      error_html_visitor 
        Name:       visit_gs_pre
        Desc:    
        Params:     err_gs - error_gs instance
        """
         
    def visit_gs_post(self, err_gs): 
        """
        Class:      error_html_visitor 
        Name:       visit_gs_post
        Desc:    
        Params:     err_gs - error_gs instance
        """

    def visit_st_pre(self, err_st):
        """
        Class:      error_html_visitor
        Name:       visit_st_pre
        Desc:    
        Params:     err_st - error_st instance
        """
        
    def visit_st_post(self, err_st):
        """
        Class:      error_html_visitor
        Name:       visit_st_post
        Desc:    
        Params:     err_st - error_st instance
        """

    def visit_seg(self, err_seg):
        """
        Class:      error_html_visitor
        Name:       visit_seg
        Desc:    
        Params:     err_seg - error_seg instance
        """
        #Print all seg up to this one
        while self.src
        err_seg.cur_line
        for (err_cde, err_str, err_value) in err_seg.errors:
            self.fd.write('<span class="seg">%s</span><br>\n' % (err_str))
                                        
        
    def visit_ele(self, err_ele): 
        """
        Class:      error_html_visitor
        Name:       visit_ele
        Desc:    
        Params:     err_ele - error_ele instance
        """

    def _print_seg(self, seg, src):
        """
        Class:      error_html_visitor
        Name:       visit_root_pre
        Desc:    
        Params:     seg - list of elements
        """
        self.fd.write('<span class="seg">%s:&nbsp;&nbsp;%s</span><br>\n' % \
            (src.cur_line, self._seg_str(seg))
        
    def _seg_str(self, seg):
        """
        Class:      error_html_visitor
        Name:       _seg_str
        Desc:    
        Params:     seg - list of elements
        """
        return seg_str(seg, self.seg_term, self.ele_term, self.subele_term, \
            self.eol).replace(' ', '&nbsp;')



