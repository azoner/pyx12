#! /usr/bin/env /usr/local/bin/python
# script to convert a X12N batch transaction set into an XML document
#
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

# THIS IS PRE-ALPHA CODE.  IT DOES NOT WORK. 

#import os
#import stat
import sys
import string
#import StringIO
#import tempfile
#import time
#import pdb
import xml.dom.minidom

#from xml.dom.ext.reader import PyExpat
#from xml.xpath import Compile
#from xml.xpath.Context import Context

class x12Error(Exception): pass
class ISAError(x12Error): pass
class GSError(x12Error): pass
class STError(x12Error): pass
class WEDIError(Exception): pass
class WEDI1Error(WEDIError): pass
class WEDI2Error(WEDIError): pass
class WEDI3Error(WEDIError): pass
class WEDI4Error(WEDIError): pass
class WEDI5Error(WEDIError): pass
class WEDI6Error(WEDIError): pass
class EngineError(Exception): pass


class x12n_document:
    #dom_codes = xml.dom.minidom.parse('map/codes.xml')
    def __init__(self):
        ISA_len = 106
    	line = sys.stdin.read(ISA_len)
	#.seek(0)
	assert (line[:3] == 'ISA'), "First line does not begin with 'ISA': %s" % line[:3]
	assert (len(line) == ISA_len), "ISA line is only %i characters" % len(line)
	self.seg_term = line[-1]
	self.ele_term = line[3]
	self.subele_term = line[-2]

	# get ISA segment map
	seg = string.split(line[:-1], self.ele_term)
	#print seg

	dom_isa = xml.dom.minidom.parse('map/map.x12.control.00401.xml')
	seg_nodes = dom_isa.getElementsByTagName("segment")
	for seg_node in seg_nodes:
	    if GetChildElementText(seg_node, 'id') == 'ISA':
	    	isa_seg_node = seg_node
	    if GetChildElementText(seg_node, 'id') == 'IEA':
	    	iea_seg_node = seg_node

	# Start XML output
	sys.stdout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	tab.incr()
	# ISA Segment	
	isa_seg = segment(isa_seg_node, seg)
	isa_seg.validate()
	isa_seg.xml()
	self.icvn = isa_seg.GetElementValue('ISA12')
	
	lines = []
	for line in string.split(sys.stdin.read(), self.seg_term):
	    if string.strip(line) != '':
	        lines.append(string.split(string.strip(line), self.ele_term))
	
	# IEA Segment	
	#for line in lines:
	#    print line
	if lines[-1:][0][0] == 'IEA':
	    iea_seg = segment(iea_seg_node, lines[-1:][0])
	    iea_seg.validate()
	else:
	    raise WEDI1Error, 'Last segment should be IEA, is "%s"' % (lines[-1:][0][0])
	
	idx = 0
	gs_idx = 0
	gs_loops = []
	while idx < len(lines)-1:
	    if lines[idx][0] == 'GS': 
	    	if gs_idx != 0:
		    raise WEDI1Error, 'Encountered a GS segment before a required GE segment'
		else:
	    	    gs_idx = idx
	    if lines[idx][0] == 'GE':
	        gs_loops.append(lines[gs_idx:idx+1])
		gs_idx = 0
	    idx = idx + 1

	for loop in gs_loops:
	    #print loop
	    gs = GS_loop(self, loop)

	iea_seg.xml()
	sys.stdout.write('</xml>\n')
	dom_isa.unlink()

    
class GS_loop:
    def __init__(self, isa, gs):
	dom_gs = xml.dom.minidom.parse('map/map.x12.control.00401.xml')
	seg_nodes = dom_gs.getElementsByTagName("segment")
	for seg_node in seg_nodes:
	    if GetChildElementText(seg_node, 'id') == 'GS':
	    	gs_seg_node = seg_node
	    if GetChildElementText(seg_node, 'id') == 'GE':
	    	ge_seg_node = seg_node
	gs_seg = segment(gs_seg_node, gs[0])
	gs_seg.validate()
	gs_seg.xml()
	self.fic = gs_seg.GetElementValue('GS01')
	self.vriic = gs_seg.GetElementValue('GS08')

	if gs[-1:][0][0] == 'GE':
	    ge_seg = segment(ge_seg_node, gs[-1:][0])
	    ge_seg.validate()
	else:
	    raise WEDI1Error, 'Last segment should be GE, is "%s"' % (gs[-1:][0][0])

	#Get map for this GS loop
        dom_map = xml.dom.minidom.parse('map/maps.xml')
    	vers = dom_map.getElementsByTagName("version")
	for ver in vers:
	    if ver.getAttribute('icvn') == isa.icvn:
	        maps = ver.getElementsByTagName("map")

	for map in maps:
	    if map.getAttribute('fic') == self.fic and map.getAttribute('vriic') == self.vriic:
                for node in map.childNodes:
           	    if node.nodeType == node.TEXT_NODE:
		        node.normalize()
                        self.map_file = node.data
	if not self.map_file:
	    raise GSError, 'Map file not found, icvn=%s, fic=%s, vriic=%s' % (isa.icvn,self.fic,self.vriic)
	dom_map.unlink()

	# Loop through ST segments
	idx = 0
	st_idx = 0
	st_loops = []
	while idx < len(gs)-1:
	    if gs[idx][0] == 'ST': 
	    	if st_idx != 0:
		    raise WEDI1Error, 'Encountered a ST segment before a required SE segment'
		else:
	    	    st_idx = idx
	    if gs[idx][0] == 'SE':
	        st_loops.append(gs[st_idx:idx+1])
		st_idx = 0
	    idx = idx + 1

	for loop in st_loops:
	    #print loop
	    st = ST_loop(self, isa, loop)

	
	ge_seg.xml()
	dom_gs.unlink()

    def getMapFile(self):
    	return self.map_file

class ST_loop:
    def __init__(self, gs, isa, st):
        print st[0]
	pass
    
class segment:
    """
    Takes a dom node of the segment and the parsed segment line as a list
    """
    def __init__(self, node, seg):
    	self.id = GetChildElementText(node, 'id')
    	self.name = GetChildElementText(node, 'name')
    	self.end_tag = GetChildElementText(node, 'end_tag')
    	self.usage = GetChildElementText(node, 'usage')
    	self.req_des = GetChildElementText(node, 'req_des')
    	self.pos = GetChildElementText(node, 'pos')

	tab.incr()
	#element_nodes = node.getElementsByTagName('element')
	i = 1 
	self.element_list = []
	for child in node.childNodes:
	    if child.nodeType == child.ELEMENT_NODE and child.tagName == 'element':
	        if i < len(seg):
	            self.element_list.append(element(child, seg[i]))
	        else:
	            self.element_list.append(element(child, None))
	        i = i + 1
	    if child.nodeType == child.ELEMENT_NODE and child.tagName == 'composite':
	        if i < len(seg):
	            self.element_list.append(composite(child, seg[i]))
	        else:
	            self.element_list.append(composite(child, None))
	        i = i + 1

    def __del__(self):
	tab.decr()

    def xml(self):
        sys.stdout.write('%s<segment code="%s">' % (tab.indent(),self.id))
    	for elem in self.element_list:
	    elem.xml()
        sys.stdout.write('%s</segment>' % (tab.indent()))
    
    def validate(self):
    	for elem in self.element_list:
	    elem.validate()
	    
    def GetElementValue(self, refdes):
    	for elem in self.element_list:
	    if elem.refdes == refdes:
	        return elem.x12_elem
	return None
    	

class element:
    def __init__(self, node, x12_elem):
        self.x12_elem = x12_elem
    	self.name = GetChildElementText(node, 'name')
    	self.usage = GetChildElementText(node, 'usage')
    	self.req_des = GetChildElementText(node, 'req_des')
    	self.seq = GetChildElementText(node, 'seq')
    	self.pos = GetChildElementText(node, 'pos')
    	self.refdes = GetChildElementText(node, 'refdes')
    	self.data_type = GetChildElementText(node, 'data_type')
    	self.min_len = GetChildElementText(node, 'min_len')
    	self.max_len = GetChildElementText(node, 'max_len')
	self.valid_codes = []
	self.external_codes = None
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.tagName == 'valid_codes':
	        self.external_codes = child.getAttribute('external')
    	        for code in child.childNodes:
		    if code.nodeType == code.ELEMENT_NODE and code.tagName == 'code':
    	        	for a in code.childNodes:
           	    	    if a.nodeType == a.TEXT_NODE:
		        	a.normalize()
				self.valid_codes.append(a.data)

    def __del__(self):
	tab.decr()

    def xml(self):
	sys.stdout.write('%s<elem code="%s">%s</elem>' % (tab.indent(), self.refdes, self.x12_elem))
    
    def validate(self):
	if len(self.x12_elem) < int(self.min_len):
	    raise WEDI1Error, 'too short %s len=%i' % (self.x12_elem, int(self.min_len))
	if len(self.x12_elem) > int(self.max_len):
	    raise WEDI1Error, 'too long: %s len=%i' % (self.x12_elem, int(self.max_len))
	if self.x12_elem == None and self.usage == 'R':
	    raise WEDI3Error
	if not (self.__valid_code__() or codes.IsValid(self.external_codes, self.x12_elem) ):
	    raise WEDIError, "Not a valid code for this ID element"
	if not IsValidDataType(self.x12_elem, self.data_type, 'E'):
	    raise WEDI1Error, "Invalid X12 datatype: '%s' is not a '%s'" % (self.x12_elem, self.data_type) 

    def __valid_code__(self):
        if not self.valid_codes:
	    return 1
	if self.x12_elem in self.valid_codes:
	    return 1
	return 0


class composite(element):
    def __init__(self, node, x12_elem):
        self.node = node
	self.x12_elem = x12_elem

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

class ExternalCodes:
    """
    Name:    ExternalCodes
    Desc:    Validates an ID against an external list of codes
    """

    def __init__(self):
    	"""
    	Name:    __init__
    	Desc:    Initialize the external list of codes
    	Params:  
    	"""
	self.codes = {}
    	# init a map of codes from codes.xml
	dom_codes = xml.dom.minidom.parse('map/codes.xml')
	codeset_nodes = dom_codes.getElementsByTagName("codeset")
	for codeset_node in codeset_nodes:
	    id = GetChildElementText(codeset_node, 'id')
	    code_list = []
            for code in codeset_node.childNodes:
	        if code.nodeType == code.ELEMENT_NODE and code.tagName == 'code':
        	    for a in code.childNodes:
       	    	        if a.nodeType == a.TEXT_NODE:
	        	    a.normalize()
			    code_list.append(a.data)
	    self.codes[id] = code_list
	print self.codes.keys()

    def IsValid(self, key, code):
    	"""
    	Name:    IsValid
    	Desc:    Initialize the external list of codes
    	Params:  key - the external codeset identifier
		 code - code to be verified
    	Returns: 1 if code is valid, 0 if not
    	"""

	#if not given a key, do not flag an error
    	if not key:
	    return 1
    	#check the code against the list indexed by key
	else:
	    if not key in self.codes.keys():
	    	raise EngineError, 'Enternel Code %s is not defined' % (key)
	    if not code in self.codes[key]:
	        return 0
	return 1

def IsValidDataType(str, data_type, charset = 'D'):
    """
    Name:    IsValidDataType
    Params:  str (input string), 
             data_type (data element identifier), 
             charset [optional] ('D' for default, 'E' for extended)
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
    

def main():
    """Script main program."""
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], ':')
#        opts, args = getopt.getopt(sys.argv[1:], 'lfd:')
    except getopt.error, msg:
        sys.stderr.write(msg + '\n')
        sys.stdout.write('usage: x12n.py file\n')
        sys.exit(2)
    #for o, a in opts:
    #    if o == '-d': ddir = a
#    try:
    if 1:
        if args:
            for file in args:
		sys.stdin = open(file, 'r')
                a = x12n_document()
        else:
            a = x12n_document()

#    except KeyboardInterrupt:
#        print "\n[interrupt]"
#        success = 0
#    return success

codes = ExternalCodes()
tab = Indent()

if __name__ == '__main__':
    sys.exit(not main())

