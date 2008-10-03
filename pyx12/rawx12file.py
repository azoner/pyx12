######################################################################
# Copyright (c) 2001-2008 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.  
#
######################################################################

#    $Id: x12file.py 1073 2007-05-03 21:06:10Z johnholland $

"""
Low level interface to an X12 data input stream.
Iterates over segment line strings.
Used by X12FileReader.
"""

# Intrapackage imports
import pyx12.errors
import pyx12.segment

DEFAULT_BUFSIZE = 8*1024
ISA_LEN = 106

class RawX12file(object):
    """
    Interface to an X12 data file
    """

    def __init__(self, fin):
        """
        Initialize the file X12 file reader

        @param fin: an open, readable file object
        @type fin: open file object
        """
        self.fd = fin
        self.buffer = None
        line = self.fd.read(ISA_LEN)
        if line[:3] != 'ISA': 
            err_str = "First line does not begin with 'ISA': %s" % line[:3]
            raise pyx12.errors.X12Error, err_str
        if len(line) != ISA_LEN:
            err_str = 'ISA line is only %i characters' % len(line)
            raise pyx12.errors.X12Error, err_str
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]
        self.buffer = line
        self.buffer += self.fd.read(DEFAULT_BUFSIZE)
        
    def __iter__(self):
        return self

    def next(self):
        """
        Iterate over input lines
        """
        try:
            while True:
                if self.buffer.find(self.seg_term) == -1: 
                    # Need more data
                    self.buffer += self.fd.read(DEFAULT_BUFSIZE)
                # Get first segment in buffer
                (line, self.buffer) = self.buffer.split(self.seg_term, 1) 
                line = line.replace('\n','').replace('\r','')
                if line != '':
                    break
        except:
            raise StopIteration

        return line

    def get_term(self):
        """
        Get the original terminators

        @rtype: tuple(string, string, string, string)
        """
        return (self.seg_term, self.ele_term, self.subele_term, '\n')

