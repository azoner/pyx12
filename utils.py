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

#import xml.dom.minidom

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


def GetChildElementText(node, elem_name):
    """
    Returns the text value of the first child element matching the element name
    """
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == elem_name:
            for a in child.childNodes:
                if a.nodeType == a.TEXT_NODE:
                    a.normalize()
                    return a.data
    return None
    
def GetChildNodeByChildElementValue(node, elem_name, child_elem_name, child_elem_value):
    """
    Returns the DOM node of the first matching element
    """
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == elem_name:
            for b in child.childNodes:
                if b.nodeType == b.ELEMENT_NODE and b.tagName == child_elem_name:
                    for a in b.childNodes:
                        if a.nodeType == a.TEXT_NODE:
                            a.normalize()
                            if a.data == child_elem_value:
                                return child
    return None
    
def GetChildNodeByAttrib(node, elem_name, attrib_name, attrib_value):
    """
    Returns the DOM node of the first matching element
    """
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == elem_name:
            if child.getAttribute(attrib_name) == attrib_value:
                return child
    return None
    

def getfirstfield(seg_list, segment_name, field_idx):
    """
    Finds the indexed field in the first matching element
    """
    for seg in seg_list:
        if seg[0] == segment_name:
            return seg[field_idx]
        else:
            return None

def GetExplicitLoops(lines, start_tag, end_tag, start_idx, end_idx):
    """
    Locate the loop blocks for a loop sets with explicit start and end tags
    Params:  lines - a list of lists containing the lines to be split
             start_tag - the loop start tag (ISA, GS, ST)
             end_tag - the loop end tag (IEA, GE, SE)
             start_idx - the index in the segment containing the control number
             end_idx - the index in the segment containing the control number
    Returns: a list containing segment lists
    """
    loops = []
    loop_idx = 0
    for i in xrange(0, len(lines)):
        if i == loop_idx:
            if lines[loop_idx][0] != start_tag:
                raise errors.WEDI1Error, 'This segment should be a %s, is %s' % (start_tag, lines[loop_idx][0])
            else:
                control_num = lines[loop_idx][start_idx]
        if lines[i][0] == end_tag:
            if control_num != lines[i][end_idx]:
                raise errors.WEDI1Error, 'The control numbers for this %s segment do not match, \
                        should be %s, is %s' % (start_tag, control_num, lines[i][end_idx])
            else:
                for j in xrange(loop_idx+1, i):
                    if lines[j][0] == start_tag:
                        raise errors.WEDI1Error, 'A %s(%s) segment was found within another %s loop' % (start_tag, 
                            control_num, start_tag)
                    if lines[j][0] == end_tag:
                        raise errors.WEDI1Error, 'A %s(%s) segment was found within another %s loop' % (end_tag, 
                            control_num, start_tag)
                loops.append(lines[loop_idx:i+1])
                loop_idx = i + 1
    return loops


def GetHLLoops(lines):
    """
    Locate the loop blocks for a loop sets delimited by HL segments
    Params:  lines - a list of lists containing the lines to be split
    Returns: a list containing segment lists
    """
    loops = []
    loop_idx = 0
    if lines[loop_idx][0] != 'HL':
        raise errors.WEDI1Error, 'This segment should be a HL, is %s' % (lines[loop_idx][0])
    #for i in xrange(loop_idx+1, len(lines)):
    for i in xrange(1, len(lines)):
        if lines[i][0] == 'HL': 
            loops.append(lines[loop_idx:i])
            loop_idx = i
    loops.append(lines[loop_idx:i])
    return loops
