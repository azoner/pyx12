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

import xml.dom.minidom

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
    Name:    IsValidDataType
    Params:  str (input string), 
             data_type (data element identifier), 
             charset [optional] ('B' for Basic, 'E' for extended)
    Returns: 1 if str is valid, 0 if not
    """
    import re
    #print str, data_type, charset
    if not data_type: return 1
    if data_type[0] == 'N':
        m = re.compile("^-?[0-9]+", re.S).search(str)
        if not m:
            # print 'nothing matched'
            return 0  # nothing matched
        if m.group(0) != str:  # matched substring != original, bad
            # print m.group(0)
            return 0
    elif data_type == 'R':
        m = re.compile("^-?[0-9]*(\.[0-9]+)?", re.S).search(str)
        if not m: return 0  # nothing matched
        if m.group(0) != str:  # matched substring != original, bad
            # print m.group(0)
            return 0
    elif data_type in ('ID', 'AN'):
        if charset == 'E':  # extended charset
            m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\sa-z%~@\[\]_{}\\\|<>#$\s]", re.S).search(str)
            if m and m.group(0):
                # print "'" + m.group(0) + "'"
                return 0
	else:
            m = re.compile("[^A-Z0-9!\"&'()*+,\-\\\./:;?=\s]", re.S).search(str)
            if m and m.group(0):  # invalid string found
           	#print "'" + m.group(0) + "'"
                return 0
    elif data_type == 'DT':
        m = re.compile("[^0-9]+", re.S).search(str)  # first test date for non-numeric chars
        if m:  # invalid string found
            # print 'invalid str, ' + m.group(0)
            return 0
        # else...
        if 8 == len(str) or 6 == len(str): # valid lengths for date
            if 6 == len(str):  # if 2 digit year, add CC
                if str[0:2] < 50:
                    str = '20' + str
                else: str = '19' + str
            s = str[4:6]  # check month
            if s < '01' or s > '12':
                # print str + ", " + s
                return 0
            s2 = str[6:8]  # check day
            if s in ('01', '03', '05', '07', '08', '10', '12'):  # 31 day month
                if s2 < '01' or s2 > '31':
                    # print str + ", " + s2
                    return 0
            elif s in ('04', '06', '09', '11'):  # 30 day month
                if s2 < '01' or s2 > '30':
                    # print str + ", " + s2
                    return 0
            else: # else 28 day
                s3 = str[0:4]  # get year
                # print s3
                if not (int(s3) % 4) and ((int(s3) % 100) or (not (int(s3) % 400)) ):  # leap year
                    if s2 < '01' or s2 > '29':
                        # print str + ", " + s3 + ', ' + s2
                        return 0
                elif s2 < '01' or s2 > '28':
                    # print str + ", " + s2
                    return 0
        else:
            # print 'invalid length, ' + str
            return 0
    elif data_type == 'TM':
        m = re.compile("[^0-9]+", re.S).search(str)  # first test time for non-numeric chars
        if m:  # invalid string found
            # print m.group(0)
            return 0
        s = str[0:2]  # check hour segment
        if s > '23': 
            # print s
            return 0
        s = str[2:4]  # check minute segment
        if s > '59':
            # print s
            return 0
        if len(str) > 4:  # time contains seconds
            if len(str) < 6:  # length is munted
                # print 'length munted, ' + str
                return 0
            s = str[4:6]
            if s > '59':  # check seconds
                # print s
                return 0
            # check decimal seconds here in the future
            if len(str) > 8:
                # print 'unhandled decimal seconds encountered'
                return 0
    elif data_type == 'B': pass
    else:  
        # print 'data_type parameter is not valid, abort'
        return 1
    return 1


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
    return
    

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
    Name:    GetExplicitLoops
    Desc:    Locate the loop blocks for a loop sets with explicit start and end tags
    Params:  lines - a list of lists containing the lines to be split
             start_tag - the loop start tag (ISA, GS, ST)
             end_tag - the loop end tag (IEA, GE, SE)
	     start_idx - the index in the segment containing the control number
	     end_idx - the index in the segment containing the control number
    Returns: a list containing segment lists
    """
    loops = []
    loop_idx = 0
    if lines[loop_idx][0] != start_tag:
        raise errors.WEDI1Error, 'This segment should be a %s, is %s' % (start_tag, lines[loop_idx][0])
    control_num = lines[loop_idx][start_idx]
    while loop_idx < len(lines):
        for i in xrange(loop_idx+1, len(lines)):
	    #print 'i=', i, start_tag, end_tag, lines[i]
            if lines[i][0] == end_tag and control_num == lines[i][end_idx]:
	        # found correct end tag
	        for j in xrange(loop_idx+1, i):
                    if lines[j][0] == start_tag:
        	        raise errors.WEDI1Error, 'A %s(%s) segment was found within another %s loop' % (start_tag, 
		    	    control_num, start_tag)
                    if lines[j][0] == end_tag:
        	        raise errors.WEDI1Error, 'A %s(%s) segment was found within another %s loop' % (end_tag, 
		    	    control_num, start_tag)
                loops.append(lines[loop_idx:i+1])
		#print 'loop_idx ', loop_idx, i+1
	        loop_idx = i + 1
		break
	loop_idx = len(lines)
    if lines[-1][0] != end_tag:
        raise errors.WEDI1Error, 'Last segment should be %s, is "%s"' % (end_tag, lines[-1][0])
    return loops

def GetHLLoops(lines):
    """
    Name:    GetExplicitLoops
    Desc:    Locate the loop blocks for a loop sets delimited by HL segments
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
