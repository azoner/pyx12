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
Interface to an X12 data file
Efficiently handles large files
Tracks end of explicit loops
Tracks segment/line/loop counts
"""

#import logging
#import os
import sys
import string
from types import *

# Intrapackage imports
from errors import *

DEFAULT_BUFSIZE = 8*1024

class x12file:
    """
    Name:    x12file
    Desc:    Interface to an X12 data file
    """

    def __init__(self, fd, errh):
        """
        Class:      x12file
        Name:       __init__
        Desc:       Initialize the file
        Params:     fd - source file descriptor
        """
        
        self.loops = []
        self.hl_stack = []
        self.gs_count = 0
        self.st_count = 0
        self.hl_count = 0
        self.seg_count = 0
        self.gs_errors = []
        self.st_info = {}
        self.cur_line = 0
        self.buffer = None
        self.fd = fd
        self.errh = errh

        #self.logger = logging.getLogger('pyx12')

        ISA_len = 106
        line = fd.read(ISA_len)
        if line[:3] != 'ISA': 
            err = {}
            err['id'] = 'ISA'
            err['code'] = 'ISA1'
            err['str'] = "First line does not begin with 'ISA': %s" % line[:3]
            errh.add_error(err)
            raise x12Error, "First line does not begin with 'ISA': %s" % line[:3]
        assert (len(line) == ISA_len), "ISA line is only %i characters" % len(line)
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]

        self.lines = []
        self.lines.append(line[:-1])
        self.buffer = line
        self.buffer += self.fd.read(DEFAULT_BUFSIZE)
        
    def __iter__(self):
        return self

    def next(self):
        errh = self.errh
        try:
            if self.buffer.find(self.seg_term) == -1: # Need more data
                self.buffer += self.fd.read(DEFAULT_BUFSIZE)
            while 1:
                # Get first segment in buffer
                (line, self.buffer) = self.buffer.split(self.seg_term, 1) 
                line = line.strip().replace('\n','').replace('\r','')
                if line != '':
                    break
            seg = string.split(line, self.ele_term)
        except:
            raise StopIteration

        for i in xrange(len(seg)):
            if seg[i].find(self.subele_term) != -1:
                seg[i] = seg[i].split(self.subele_term) # Split composite
        if seg[0] == 'ISA': 
            seg[-1] = self.subele_term
            self.loops.append(('ISA', seg[13]))
            self.gs_count = 0
        elif seg[0] == 'IEA': 
            if self.loops[-1][0] != 'ISA' or self.loops[-1][1] != seg[2]:
                err = {}
                err['id'] = 'ISA'
                err['code'] = 'ISA2'
                err['str'] = 'IEA id=%s does not match ISA id=%s' % (seg[2], self.loops[-1][1])
                errh.add_error(err)
            if int(seg[1]) != self.gs_count:
                err = {}
                err['id'] = 'ISA'
                err['code'] = 'ISA3'
                err['str'] = 'IEA count for IEA02=%s is wrong' % (seg[2])
                errh.add_error(err)
            del self.loops[-1]
        elif seg[0] == 'GS': 
            self.gs_count += 1
            self.loops.append(('GS', seg[6]))
            self.st_count = 0
        elif seg[0] == 'GE': 
            if self.loops[-1][0] != 'GS' or self.loops[-1][1] != seg[2]:
                err = {}
                err['id'] = 'GS'
                err['str'] = 'GE id=%s does not match GS id=%s' % (seg[2], self.loops[-1][1])
                err['code'] = '4'
                errh.add_error(err)
            if int(seg[1]) != self.st_count:
                err = {}
                err['id'] = 'GS'
                err['str'] = 'GE count of %s for GE02=%s is wrong. I count %i' \
                    % (seg[1], seg[2], self.st_count)
                err['code'] = '5'
                errh.add_error(err)
            del self.loops[-1]
        elif seg[0] == 'ST': 
            self.st_count += 1
            self.loops.append(('ST', seg[2]))
            self.seg_count = 1 
        elif seg[0] == 'SE': 
            if self.loops[-1][0] != 'ST' or self.loops[-1][1] != seg[2]:
                err = {}
                err['id'] = 'ST'
                err['str'] = 'SE id=%s does not match ST id=%s' % (seg[2], self.loops[-1][1])
                err['code'] = '3'
                errh.add_error(err)
            if int(seg[1]) != self.seg_count + 1:
                err = {}
                err['id'] = 'ST'
                err['str'] = 'SE count of %s for SE02=%s is wrong. I count %i' \
                    % (seg[1], seg[2], self.seg_count + 1)
                err['code'] = '4'
                errh.add_error(err)
            del self.loops[-1]
        elif seg[0] == 'LS': 
            self.loops.append(('LS', seg[6]))
        elif seg[0] == 'LE': 
            del self.loops[-1]
        elif seg[0] == 'HL': 
            self.seg_count += 1
            self.hl_count += 1
            if self.hl_count != int(seg[1]):
                raise x12Error, 'My HL count %i does not match your HL count %s' \
                    % (self.hl_count, seg[1])
                err = {}
                err['id'] = 'SEG'
                err['str'] = 'My HL count %i does not match your HL count %s' \
                    % (self.hl_count, seg[1])
                errh.add_error(err)
            if seg[2] != '':
                parent = int(seg[2])
                if parent not in self.hl_stack:
                    self.hl_stack.append(parent)
                else:
                    if self.hl_stack:
                        while self.hl_stack[-1] != parent:
                            del self.hl_stack[-1]
        else:
            self.seg_count += 1
        self.cur_line += 1
        return seg

    def get_id(self):
        isa_id = None
        gs_id = None
        st_id = None
        ls_id = None
        for loop in self.loops:
            if loop[0] == 'ISA': isa_id = loop[1]
            if loop[0] == 'GS': gs_id = loop[1]
            if loop[0] == 'ST': st_id = loop[1]
            if loop[0] == 'LS': ls_id = loop[1]
        return (isa_id, gs_id, st_id, ls_id, self.seg_count, self.cur_line)

    def print_seg(self, seg):
        sys.stdout.write('%s\n' % (self.seg_str(seg)))

    def seg_str(self, seg, eol=''):
        tmp = []
        for a in seg:
            if type(a) is ListType:
                tmp.append(string.join(a, self.subele_term))
            else:
                tmp.append(a)
        return '%s%s%s' % (string.join(tmp, self.ele_term), self.seg_term, eol) 
