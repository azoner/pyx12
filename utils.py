#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
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

def IsValidDataType(str, data_type, charset = 'B'):
    """
    Params:  str - data value to validate
             data_type - X12 data element identifier
             charset [optional] - 'B' for Basic X12 character set, 'E' for extended
    Returns: 1 if str is valid, 0 if not
    """
    import re
    #print str, data_type, charset
    success = 1
    if not data_type: return 1
    if data_type[0] == 'N':
        m = re.compile("^-?[0-9]+", re.S).search(str)
        if not m:
            success = 0  # nothing matched
        if m.group(0) != str:  # matched substring != original, bad
            success = 0
        return success
    elif data_type == 'R':
        m = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S).search(str)
        if not m: 
            success = 0  # nothing matched
        if m.group(0) != str:  # matched substring != original, bad
            success = 0
        return success
    elif data_type in ('ID', 'AN'):
        if charset == 'E':  # extended charset
            m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S).search(str)
            if m and m.group(0):
             success = 0
        else:
            m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\s]", re.S).search(str)
            if m and m.group(0):  # invalid string found
             success = 0
        return success
    elif data_type == 'DT':
        m = re.compile("[^0-9]+", re.S).search(str)  # first test date for non-numeric chars
        if m:  # invalid string found
            success = 0
        if 8 == len(str) or 6 == len(str): # valid lengths for date
            if 6 == len(str):  # if 2 digit year, add CC
                if str[0:2] < 50:
                    str = '20' + str
                else: str = '19' + str
            month = int(str[4:6])  # check month
            if month < 1 or month > 12:
             success = 0
            day = int(str[6:8])  # check day
            if month in (1, 3, 5, 7, 8, 10, 12):  # 31 day month
                if day < 1 or day > 31:
                 success = 0
            elif month in (4, 6, 9, 11):  # 30 day month
                if day < 1 or day > 30:
                 success = 0
            else: # else 28 day
                year = int(str[0:4])  # get year
                if not (year % 4) and ((year % 100) or (not (year % 400)) ):  # leap year
                    if day < 1 or day > 29:
                     success = 0
                elif day < 1 or day > 28:
                 success = 0
        else:
            success = 0
        return success
    elif data_type == 'TM':
        m = re.compile("[^0-9]+", re.S).search(str)  # first test time for non-numeric chars
        if m:  # invalid string found
            success = 0
        elif str[0:2] > '23' or str[2:4] > '59':  # check hour, minute segment
            success = 0
        elif len(str) > 4:  # time contains seconds
            if len(str) < 6:  # length is munted
             success = 0
            elif str[4:6] > '59':  # check seconds
             success = 0
            # check decimal seconds here in the future
            elif len(str) > 8:
                # print 'unhandled decimal seconds encountered'
             success = 0
        return success
    elif data_type == 'B': pass
#    else:  
#        # print 'data_type parameter is not valid, abort'
#        return 1
    return success
