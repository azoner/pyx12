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
Interface to an X12 data file.
Efficiently handles large files.
Tracks end of explicit loops.
Tracks segment/line/loop counts.
"""

import sys
#import string
#from types import *
import logging
#import pdb

# Intrapackage imports
import pyx12.errors
import pyx12.segment

DEFAULT_BUFSIZE = 8*1024
ISA_LEN = 106

logger = logging.getLogger('pyx12.x12file')
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)

class X12file:
    """
    Interface to an X12 data file
    """

    def __init__(self, src_file):
        """
        Initialize the file

        @param src_file: absolute path of source file 
        @type src_file: string
        """
        if src_file == '-':
            self.fd = sys.stdin
        else:
            self.fd = open(src_file, 'U')
        self.err_list = []
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
        #self.errors = []

        #self.logger = logging.getLogger('pyx12')

        line = self.fd.read(ISA_LEN)
        if line[:3] != 'ISA': 
            err_str = "First line does not begin with 'ISA': %s" % line[:3]
            raise pyx12.X12Error, err_str
        if len(line) != ISA_LEN:
            err_str = 'ISA line is only %i characters' % len(line)
            raise pyx12.X12Error, err_str
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]
        logger.debug('seg_term "%s" / ele_term "%s" / subele_term "%s"' % \
            (self.seg_term, self.ele_term, self.subele_term))
       
        self.buffer = line
        self.buffer += self.fd.read(DEFAULT_BUFSIZE)
        
    def __del__(self):
        try:
            self.fd.close()
        except:
            pass

    def __iter__(self):
        return self

    def next(self):
        """
        Iterate over input file segments
        """
        self.err_list = []
        #self.errors = []
        try:
            while True:
                if self.buffer.find(self.seg_term) == -1: # Need more data
                    self.buffer += self.fd.read(DEFAULT_BUFSIZE)
                while True:
                    # Get first segment in buffer
                    (line, self.buffer) = self.buffer.split(self.seg_term, 1) 
                    line = line.replace('\n','').replace('\r','')
                    if line != '':
                        break
                # We have not yet incremented cur_line
                if line[-1] == self.ele_term:
                    err_str = 'Segment contains trailing element terminators'
                    self._seg_error('SEG1', err_str, None, 
                        src_line=self.cur_line+1)
                #seg = string.split(line, self.ele_term)
                seg = pyx12.segment.segment(line, self.seg_term, self.ele_term, \
                    self.subele_term)
                if seg.is_empty():
                    err_str = 'Segment "%s" is empty' % (line)
                    self._seg_error('8', err_str, None, 
                        src_line=self.cur_line+1)
                if not seg.is_seg_id_valid():
                    err_str = 'Segment identifier "%s" is invalid' % (
                        seg.get_seg_id())
                    self._seg_error('1', err_str, None, 
                        src_line=self.cur_line+1)
                else:
                    break # Found valid segment, so can stop looking
        except:
            raise StopIteration

        try:
            #for i in xrange(1, len(seg)+1):
            #    if seg[i].find(self.subele_term) != -1:
            #        seg[i] = seg[i].split(self.subele_term) # Split composite
            if seg.get_seg_id() == 'ISA': 
                if len(seg) != 16:
                    raise pyx12.X12Error, \
                        'The ISA segment must have 16 elements (%s)' % (seg)
                #seg[-1] = self.subele_term
                interchange_control_number = seg.get_value('ISA13')
                if interchange_control_number in self.isa_ids:
                    err_str = 'ISA Interchange Control Number '
                    err_str += '%s not unique within file' \
                        % (interchange_control_number)
                    self._isa_error('025', err_str)
                self.loops.append(('ISA', interchange_control_number))
                self.isa_ids.append(interchange_control_number)
                self.gs_count = 0
                self.gs_ids = []
                self.isa_usage = seg.get_value('ISA15')
            elif seg.get_seg_id() == 'IEA': 
                if self.loops[-1][0] != 'ISA':
                    #pdb.set_trace()
                    err_str = 'Unterminated Loop %s' % (self.loops[-1][0])
                    self._isa_error('024', err_str)
                    del self.loops[-1]
                if self.loops[-1][1] != seg.get_value('IEA02'):
                    err_str = 'IEA id=%s does not match ISA id=%s' % \
                        (seg.get_value('IEA02'), self.loops[-1][1])
                    self._isa_error('001', err_str)
                if self._int(seg.get_value('IEA01')) != self.gs_count:
                    err_str = 'IEA count for IEA02=%s is wrong' % \
                        (seg.get_value('IEA02'))
                    self._isa_error('021', err_str)
                del self.loops[-1]
            elif seg.get_seg_id() == 'GS': 
                group_control_number = seg.get_value('GS06')
                if group_control_number in self.gs_ids:
                    err_str = 'GS Interchange Control Number '
                    err_str += '%s not unique within file' \
                        % (group_control_number)
                    self._gs_error('6', err_str)
                self.gs_count += 1
                self.gs_ids.append(group_control_number)
                self.loops.append(('GS', group_control_number))
                self.st_count = 0
                self.st_ids = []
            elif seg.get_seg_id() == 'GE': 
                if self.loops[-1][0] != 'GS':
                    err_str = 'Unterminated segment %s' % (self.loops[-1][1])
                    self._gs_error('3', err_str)
                    del self.loops[-1]
                if self.loops[-1][1] != seg.get_value('GE02'):
                    err_str = 'GE id=%s does not match GS id=%s' % \
                        (seg.get_value('GE02'), self.loops[-1][1])
                    self._gs_error('4', err_str)
                if self._int(seg.get_value('GE01')) != self.st_count:
                    err_str = 'GE count of %s for GE02=%s is wrong. I count %i'\
                        % (seg.get_value('GE01'), \
                        seg.get_value('GE02'), self.st_count)
                    self._gs_error('5', err_str)
                del self.loops[-1]
            elif seg.get_seg_id() == 'ST': 
                self.hl_stack = []
                self.hl_count = 0
                transaction_control_number = seg.get_value('ST02')
                if transaction_control_number in self.st_ids:
                    err_str = 'ST Interchange Control Number '
                    err_str += '%s not unique within file' \
                        % (transaction_control_number)
                    self._st_error('23', err_str)
                self.st_count += 1
                self.st_ids.append(transaction_control_number)
                self.loops.append(('ST', transaction_control_number))
                self.seg_count = 1 
                self.hl_count = 0
            elif seg.get_seg_id() == 'SE': 
                se_trn_control_num = seg.get_value('SE02')
                if self.loops[-1][0] != 'ST' or \
                        self.loops[-1][1] != se_trn_control_num:
                    err_str = 'SE id=%s does not match ST id=%s' % \
                        (se_trn_control_num, self.loops[-1][1])
                    self._st_error('3', err_str)
                if self._int(seg.get_value('SE01')) != self.seg_count + 1:
                    err_str = 'SE count of %s for SE02=%s is wrong. I count %i'\
                        % (seg.get_value('SE01'), \
                            se_trn_control_num, self.seg_count + 1)
                    self._st_error('4', err_str)
                del self.loops[-1]
            elif seg.get_seg_id() == 'LS': 
                self.loops.append(('LS', seg.get_value('LS06')))
            elif seg.get_seg_id() == 'LE': 
                del self.loops[-1]
            elif seg.get_seg_id() == 'HL': 
                self.seg_count += 1
                self.hl_count += 1
                hl_count = seg.get_value('HL01')
                if self.hl_count != self._int(hl_count):
                    #raise pyx12.X12Error, \
                    #   'My HL count %i does not match your HL count %s' \
                    #    % (self.hl_count, seg[1])
                    err_str = 'My HL count %i does not match your HL count %s' \
                        % (self.hl_count, hl_count)
                    self._seg_error('HL1', err_str)
                if seg.get_value('HL02') != '':
                    hl_parent = self._int(seg.get_value('HL02'))
                    if hl_parent not in self.hl_stack:
                        err_str = 'HL parent (%i) is not a valid parent' \
                            % (hl_parent)
                        self._seg_error('HL2', err_str)
                    while self.hl_stack and hl_parent != self.hl_stack[-1]:
                        del self.hl_stack[-1]
                else:
                    if len(self.hl_stack) != 0:
                        err_str = 'HL parent is blank, but stack not empty'
                        self._seg_error('HL2', err_str)
                self.hl_stack.append(self.hl_count)
            else:
                self.seg_count += 1
        except IndexError:
            raise
            #err_str = "Expected element not found': %s" % seg.format()
            #raise pyx12.X12Error, err_str

        self.cur_line += 1
        return seg

    def get_errors(self):
        """
        Get Errors
        DEPRECATED
        """
        raise pyx12.EngineError, 'X12file.get_errors is no longer used'
        
    def pop_errors(self):
        """
        Pop error list
        @return: List of errors
        """
        tmp = self.err_list
        self.err_list = []
        return tmp

    def _isa_error(self, err_cde, err_str):
        """
        @param err_cde: ISA level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_list.append(('isa', err_cde, err_str, None, None))

    def _gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_list.append(('gs', err_cde, err_str, None, None))

    def _st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_list.append(('st', err_cde, err_str, None, None))

    def _seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_list.append(('seg', err_cde, err_str, err_value, src_line))
        
    def _int(self, str_val):
        """
        Converts a string to an integer
        @type str_val: string
        @return: Int value if successful, None if not
        @rtype: int
        """
        try:
            return int(str_val)
        except ValueError:
            return None
        return None
        
    def cleanup(self):
        """
        At EOF, check for missing loop trailers
        """
        #self.err_list = []
        if self.loops:
            for (seg, id1) in self.loops: 
                if seg == 'ST':
                    err_str = 'Mandatory segment "Transaction Set Trailer" '
                    err_str += '(SE=%s) missing' % (id1)
                    self._st_error('2', err_str)
                elif seg == 'GS':
                    err_str = 'Mandatory segment "Functional Group Trailer" '
                    err_str += '(GE=%s) missing' % (id1)
                    self._gs_error('3', err_str)
                elif seg == 'ISA':
                    err_str = 'Mandatory segment "Interchange Control Trailer" '
                    err_str += '(IEA=%s) missing' % (id1)
                    self._isa_error('023', err_str)
                #elif self.loops[-1][0] == 'LS':
                #    err_str = 'LS id=%s was not closed with a LE' % \
                #    (id1, self.loops[-1][1])
        
    def get_isa_id(self): 
        """
        Get the current ISA identifier

        @rtype: string
        """
        for loop in self.loops:
            if loop[0] == 'ISA': 
                return loop[1]
        return None

    def get_gs_id(self): 
        """
        Get the current GS identifier

        @rtype: string
        """
        for loop in self.loops:
            if loop[0] == 'GS': 
                return loop[1]
        return None

    def get_st_id(self): 
        """
        Get the current ST identifier

        @rtype: string
        """
        for loop in self.loops:
            if loop[0] == 'ST': 
                return loop[1]
        return None

    def get_ls_id(self): 
        """
        Get the current LS identifier

        @rtype: string
        """
        for loop in self.loops:
            if loop[0] == 'LS': 
                return loop[1]
        return None

    def get_seg_count(self): 
        """
        Get the current segment count

        @rtype: int
        """
        return self.seg_count

    def get_cur_line(self):
        """
        Get the current line

        @rtype: int
        """
        return self.cur_line

    def get_term(self):
        """
        Get the original terminators

        @rtype: tuple(string, string, string, string)
        """
        return (self.seg_term, self.ele_term, self.subele_term, '\n')
