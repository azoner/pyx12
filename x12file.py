#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#		John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification, 
#	are permitted provided that the following conditions are met:
#
#	1. Redistributions of source code must retain the above copyright notice, this list 
#	   of conditions and the following disclaimer. 
#	
#	2. Redistributions in binary form must reproduce the above copyright notice, this 
#	   list of conditions and the following disclaimer in the documentation and/or other 
#	   materials provided with the distribution. 
#	
#	3. The name of the author may not be used to endorse or promote products derived 
#	   from this software without specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#	WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#	MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#	EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#	EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#	OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#	THE POSSIBILITY OF SUCH DAMAGE.


"""
Interface to an X12 data file
Efficiently handles large files
Tracks end of explicit loops
Tracks segment/line/loop counts
"""

#import os
#import sys
import string

# Intrapackage imports
import errors


class x12file:
    """
    Name:    x12file
    Desc:    Interface to an X12 data file
    """

    def __init__(self, fd):
    	"""
    	Name:    __init__
    	Desc:    Initialize the file
    	Params:  fd - file descriptor
    	"""
	
	self.cur_line = 0
	self.lines = []
	self.loops = []
	self.gs_count = 0
	self.st_count = 0
	self.seg_count = 0
	#os.linesep = self.seg_term

        ISA_len = 106
        line = fd.read(ISA_len)
        #.seek(0)
        assert (line[:3] == 'ISA'), "First line does not begin with 'ISA': %s" % line[:3]
        assert (len(line) == ISA_len), "ISA line is only %i characters" % len(line)
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]

	self.lines = []
	self.lines.append(line)
	for line in string.split(fd.read(), self.seg_term):
	    if string.strip(line) != '':
		self.lines.append(string.strip(line).replace('\n','').replace('\r',''))
	
    def __iter__(self):
        return self

    def next(self):
        if self.cur_line >= len(self.lines):
            raise StopIteration
    	line = self.lines[self.cur_line]
	seg = string.split(line, self.ele_term)
	if seg[0] == 'ISA': 
	    self.loops.append(('ISA', seg[13]))
	    self.gs_count = 0
	elif seg[0] == 'IEA': 
	    if self.loops[-1][0] != 'ISA' or self.loops[-1][1] != seg[2]:
		raise errors.ISAError, 'IEA does not match ISA id'
	    if int(seg[1]) != self.gs_count:
	    	raise errors.ISAError, 'IEA count for IEA02=%s is wrong' % (seg[2])
	    del self.loops[-1]
	elif seg[0] == 'GS': 
	    self.gs_count += 1
	    self.loops.append(('GS', seg[6]))
	    self.st_count = 0
	elif seg[0] == 'GE': 
	    if self.loops[-1][0] != 'GS' or self.loops[-1][1] != seg[2]:
		raise errors.GSError, 'GE does not match GS id'
	    if int(seg[1]) != self.st_count:
	    	raise errors.GSError, 'GE count for GE02=%s is wrong. I count %i' % (seg[2], self.st_count)
	    del self.loops[-1]
	elif seg[0] == 'ST': 
	    self.st_count += 1
	    self.loops.append(('ST', seg[2]))
	    self.seg_count = 1 
	elif seg[0] == 'SE': 
	    if self.loops[-1][0] != 'ST' or self.loops[-1][1] != seg[2]:
		raise errors.STError, 'SE does not match ST id'
	    if int(seg[1]) != self.seg_count + 1:
	    	raise errors.STError, 'SE count for SE02=%s is wrong. I count %i' % (seg[2], self.seg_count + 1)
	    del self.loops[-1]
	else:
	    self.seg_count += 1
    	self.cur_line += 1
	return seg

#    def close(self):
#        """Free the memory buffer.
#        """
#        if not self.closed:
#            self.closed = 1
#            del self.buf, self.pos
