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
from utils import seg_str
import logging

# Intrapackage imports
from errors import *

DEFAULT_BUFSIZE = 8*1024

logger = logging.getLogger('pyx12.x12file')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

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
        self.fd = fd
        self.errh = errh
        self.loops = []
        self.hl_stack = []
        self.gs_count = 0
        self.st_count = 0
        self.hl_count = 0
        self.seg_count = 0
        self.cur_line = 0
        self.buffer = None
        self.isa_ids = []
        self.gs_ids = []
        self.st_ids = []
        self.isa_usage = None

        #self.logger = logging.getLogger('pyx12')

        ISA_len = 106
        line = fd.read(ISA_len)
        if line[:3] != 'ISA': 
            err_str = "First line does not begin with 'ISA': %s" % line[:3]
            #errh.isa_error('ISA1', err_str)
            raise x12Error, err_str
        if len(line) != ISA_len:
            err_str = 'ISA line is only %i characters' % len(line)
            #errh.isa_error('ISA4', err_str)
            raise x12Error, err_str
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]
        logger.debug('seg_term "%s" / ele_term "%s" / subele_term "%s"' % \
            (self.seg_term, self.ele_term, self.subele_term))
       
        self.buffer = line
        self.buffer += self.fd.read(DEFAULT_BUFSIZE)
        
    def __iter__(self):
        return self

    def next(self):
        #errh = self.errh
        try:
            if self.buffer.find(self.seg_term) == -1: # Need more data
                self.buffer += self.fd.read(DEFAULT_BUFSIZE)
            while 1:
                # Get first segment in buffer
                (line, self.buffer) = self.buffer.split(self.seg_term, 1) 
                line = line.strip().replace('\n','').replace('\r','')
                if line != '':
                    break
            if line[-1] == self.ele_term:
                err_str = 'Segment contains trailing element terminators'
                self.errh.seg_error('SEG1', err_str, src_line=self.cur_line+1 )
            seg = string.split(line, self.ele_term)
        except:
            raise StopIteration

        try:
            for i in xrange(len(seg)):
                if seg[i].find(self.subele_term) != -1:
                    seg[i] = seg[i].split(self.subele_term) # Split composite
            if seg[0] == 'ISA': 
                if len(seg) != 17:
                    raise x12Error, 'The ISA segement must have 16 elements (%s)' % (seg)
                seg[-1] = self.subele_term
                interchange_control_number = seg[13]
                if interchange_control_number in self.isa_ids:
                    err_str = 'ISA Interchange Control Number %s not unique within file' \
                        % (interchange_control_number)
                    self.errh.isa_error('025', err_str)
                self.loops.append(('ISA', interchange_control_number))
                self.isa_ids.append(interchange_control_number)
                self.gs_count = 0
                self.gs_ids = []
                self.isa_usage = seg[15]
            elif seg[0] == 'IEA': 
                if self.loops[-1][0] != 'ISA' or self.loops[-1][1] != seg[2]:
                    err_str = 'IEA id=%s does not match ISA id=%s' % (seg[2], self.loops[-1][1])
                    self.errh.isa_error('001', err_str)
                if int(seg[1]) != self.gs_count:
                    err_str = 'IEA count for IEA02=%s is wrong' % (seg[2])
                    self.errh.isa_error('021', err_str)
                del self.loops[-1]
            elif seg[0] == 'GS': 
                group_control_number = seg[6]
                if group_control_number in self.gs_ids:
                    err_str = 'GS Interchange Control Number %s not unique within file' \
                        % (group_control_number)
                    self.errh.gs_error('6', err_str)
                self.gs_count += 1
                self.gs_ids.append(group_control_number)
                self.loops.append(('GS', group_control_number))
                self.st_count = 0
                self.st_ids = []
            elif seg[0] == 'GE': 
                if self.loops[-1][0] != 'GS' or self.loops[-1][1] != seg[2]:
                    err_str = 'GE id=%s does not match GS id=%s' % (seg[2], self.loops[-1][1])
                    self.errh.gs_error('4', err_str)
                if int(seg[1]) != self.st_count:
                    err_str = 'GE count of %s for GE02=%s is wrong. I count %i' \
                        % (seg[1], seg[2], self.st_count)
                    self.errh.gs_error('5', err_str)
                del self.loops[-1]
            elif seg[0] == 'ST': 
                transaction_control_number = seg[2]
                if transaction_control_number in self.st_ids:
                    err_str = 'ST Interchange Control Number %s not unique within file' \
                        % (transaction_control_number)
                    self.errh.st_error('23', err_str)
                self.st_count += 1
                self.st_ids.append(transaction_control_number)
                self.loops.append(('ST', transaction_control_number))
                self.seg_count = 1 
                self.hl_count = 0
            elif seg[0] == 'SE': 
                se_trn_control_num = seg[2]
                if self.loops[-1][0] != 'ST' or self.loops[-1][1] != se_trn_control_num:
                    err_str = 'SE id=%s does not match ST id=%s' % (se_trn_control_num, self.loops[-1][1])
                    self.errh.st_error('3', err_str)
                if int(seg[1]) != self.seg_count + 1:
                    err_str = 'SE count of %s for SE02=%s is wrong. I count %i' \
                        % (seg[1], se_trn_control_num, self.seg_count + 1)
                    self.errh.st_error('4', err_str)
                del self.loops[-1]
            elif seg[0] == 'LS': 
                self.loops.append(('LS', seg[6]))
            elif seg[0] == 'LE': 
                del self.loops[-1]
            elif seg[0] == 'HL': 
                self.seg_count += 1
                self.hl_count += 1
                if self.hl_count != int(seg[1]):
                    #raise x12Error, 'My HL count %i does not match your HL count %s' \
                    #    % (self.hl_count, seg[1])
                    err_str = 'My HL count %i does not match your HL count %s' \
                        % (self.hl_count, seg[1])
                    self.errh.seg_error('HL1', err_str)
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
        except IndexError:
            err_str = "Expected element not found': %s" % seg
            raise x12Error, err_str

        self.cur_line += 1
        return seg

    def cleanup(self):
        if self.loops:
            for (seg, id) in self.loops.reverse(): 
                if self.loops[-1][0] == 'ST':
                    err_str = 'ST id=%s was not closed with a SE' % (id)
                    self.errh.st_error('3', err_str)
                    self.errh.close_st_loop(None, None, self)
                elif self.loops[-1][0] == 'GS':
                    err_str = 'GS id=%s was not closed with a GE' % (id)
                    self.errh.gs_error('3', err_str)
                    self.errh.close_gs_loop(None, None, self)
                elif self.loops[-1][0] == 'ISA':
                    err_str = 'ISA id=%s was not closed with a IEA' % (id)
                    self.errh.isa_error('023', err_str)
                    self.errh.close_isa_loop(None, None, self)
                #elif self.loops[-1][0] == 'LS':
                #    err_str = 'LS id=%s was not closed with a LE' % (id, self.loops[-1][1])
                #    self.errh.ls_error('3', err_str)
        

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
        sys.stdout.write('%s' % (seg_str(seg, self.seg_term, self.ele_term, self.subele_term, '\n')))

    def format_seg(self, seg):
        return '%s' % (seg_str(seg, self.seg_term, self.ele_term, self.subele_term, '\n'))

    def get_term(self):
        return (self.seg_term, self.ele_term, self.subele_term, '\n')
