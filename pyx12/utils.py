#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without
#        modification, are permitted provided that the following conditions are
#        met:
#
#        1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote
#        products derived from this software without specific prior written
#        permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#        IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#        DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#        INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#        STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#        IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#        POSSIBILITY OF SUCH DAMAGE.

import string
from types import *
import pdb

# Intrapackage imports
import errors


class Indent:
    def __init__(self):
        self.tab = 2 # number of spaces in a tab
        self.tabs = 0 # current tabs
    def incr(self):
        self.tabs = self.tabs + 1
    def decr(self):
        self.tabs = max(self.tabs - 1, 0)

    def indent(self):
        print ' ' * (self.tab * self.tabs)
        return ' ' * (self.tab * self.tabs)

class IsValidError(Exception): pass


def IsValidDataType(str, data_type, charset = 'B'):
    """
    Params:  str - data value to validate
             data_type - X12 data element identifier
             charset [optional] - 'B' for Basic X12 character set, 'E' for extended
    Returns: 1 if str is valid, 0 if not
    """
    import re
    #print str, data_type, charset
    if not data_type:
        return True
    if type(str) is not StringType:
        return False

    try:
        if data_type[0] == 'N':
            m = re.compile("^-?[0-9]+", re.S).search(str)
            if not m:
                raise IsValidError # nothing matched
            if m.group(0) != str:  # matched substring != original, bad
                raise IsValidError # nothing matched
        elif data_type == 'R':
            m = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S).search(str)
            if not m: 
                raise IsValidError # nothing matched
            if m.group(0) != str:  # matched substring != original, bad
                raise IsValidError 
        elif data_type in ('ID', 'AN'):
            if charset == 'E':  # extended charset
                m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S).search(str)
                if m and m.group(0):
                    raise IsValidError 
            elif charset == 'B':  # basic charset:
                m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\s]", re.S).search(str)
                if m and m.group(0):  # invalid string found
                    raise IsValidError 
        elif data_type == 'RD8':
            (start, end) = str.split('-')
            return IsValidDataType(start, 'D8', charset) and IsValidDataType(end, 'D8', charset) 
        elif data_type in ('DT', 'D8', 'D6'):
            if data_type == 'D8' and len(str) != 8:
                raise IsValidError
            if data_type == 'D6' and len(str) != 6:
                raise IsValidError
            m = re.compile("[^0-9]+", re.S).search(str)  # first test date for non-numeric chars
            if m:  # invalid string found
                raise IsValidError 
            if len(str) in (6, 8, 12): # valid lengths for date
                try:
                    if 6 == len(str):  # if 2 digit year, add CC
                        if str[0:2] < 50:
                            str = '20' + str
                        else:
                            str = '19' + str
                    month = int(str[4:6])  # check month
                    if month < 1 or month > 12:
                        raise IsValidError
                    day = int(str[6:8])  # check day
                    if month in (1, 3, 5, 7, 8, 10, 12):  # 31 day month
                        if day < 1 or day > 31:
                            raise IsValidError
                    elif month in (4, 6, 9, 11):  # 30 day month
                        if day < 1 or day > 30:
                            raise IsValidError
                    else: # else 28 day
                        year = int(str[0:4])  # get year
                        if not year%4 and not (not year%100 and year%400):
                        #if not (year % 4) and ((year % 100) or (not (year % 400)) ):  # leap year
                            if day < 1 or day > 29:
                                raise IsValidError
                        elif day < 1 or day > 28:
                            raise IsValidError
                    if len(str) == 12:
                        if not IsValidDataType(str[8:12], 'TM', charset):
                            raise IsValidError
                except TypeError:
                    raise IsValidError
            else:
                raise IsValidError 
        elif data_type == 'TM':
            m = re.compile("[^0-9]+", re.S).search(str)  # first test time for non-numeric chars
            if m:  # invalid string found
                raise IsValidError 
            elif str[0:2] > '23' or str[2:4] > '59':  # check hour, minute segment
                raise IsValidError 
            elif len(str) > 4:  # time contains seconds
                if len(str) < 6:  # length is munted
                    raise IsValidError 
                elif str[4:6] > '59':  # check seconds
                    raise IsValidError 
                # check decimal seconds here in the future
                elif len(str) > 8:
                    # print 'unhandled decimal seconds encountered'
                    raise IsValidError 
        elif data_type == 'B': pass
    except IsValidError:
        return False
    #    else:  
    #        # print 'data_type parameter is not valid, abort'
    #        return 1
    return True

def seg_str(seg, seg_term, ele_term, subele_term, eol=''):
    #if None in seg:
    #    logger.debug(seg)
    tmp = []
    for a in seg:
        if type(a) is ListType:
            tmp.append(string.join(a, subele_term))
        else:
            tmp.append(a)
    return '%s%s%s' % (string.join(tmp, ele_term), seg_term, eol)

def escape_html_chars(str):
    if str is None: 
        return str
    str = str.replace('&', '&amp;')
    str = str.replace(' ', '&nbsp;')
    str = str.replace('>', '&gt;')
    str = str.replace('<', '&lt;')
    return str
