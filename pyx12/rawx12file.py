######################################################################
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Low level interface to an X12 data input stream.
Iterates over segment line strings.
Used by X12Reader.
"""

# Intrapackage imports
import pyx12.errors
import pyx12.segment

DEFAULT_BUFSIZE = 8 * 1024
ISA_LEN = 106


class RawX12File(object):
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
            raise pyx12.errors.X12Error(err_str)
        if len(line) != ISA_LEN:
            err_str = 'ISA line is only %i characters' % len(line)
            raise pyx12.errors.X12Error(err_str)
        self.icvn = line[84:89]
        if self.icvn not in ('00401', '00501'):
            err_str = 'ISA Interchange Control Version Number is unknown: %s for %s' % (self.icvn, line)
            raise pyx12.errors.X12Error(err_str)
        self.seg_term = line[-1]
        self.ele_term = line[3]
        self.subele_term = line[-2]
        self.repetition_term = line[82] if self.icvn == '00501' else None
        self.buffer = line
        self.buffer += self.fd.read(DEFAULT_BUFSIZE)

    def __iter__(self):
        """
        Iterate over input lines
        Often, X12 files have a CR-LF after the segment delimiter.
        Split the input stream on the delimiter and remove any leading CR-LF
        """
        while True:
            if self.buffer.find(self.seg_term) == -1:
                # Need more data
                self.buffer += self.fd.read(DEFAULT_BUFSIZE)
            if self.buffer.find(self.seg_term) == -1:
                # Still have no segment terminator
                break
            # Get first segment in buffer
            (line, self.buffer) = self.buffer.split(self.seg_term, 1)
            line = line.lstrip('\n\r')
            if line == '':
                break
            yield(line)

    def get_term(self):
        """
        Get the original terminators

        @rtype: tuple(string, string, string, string)
        """
        return (self.seg_term, self.ele_term, self.subele_term, '\n', self.repetition_term)
