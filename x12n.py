#! /usr/bin/env /usr/local/bin/python
# script to convert a X12N batch transaction set into an XML document
    """ 
    $Id$
    This file is part of the pyX12 project.

    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
		John Holland <jholland@kazoocmh.org> <john@zoner.org>

    All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, 
	are permitted provided that the following conditions are met:

	1. Redistributions of source code must retain the above copyright notice, this list 
	   of conditions and the following disclaimer. 
	
	2. Redistributions in binary form must reproduce the above copyright notice, this 
	   list of conditions and the following disclaimer in the documentation and/or other 
	   materials provided with the distribution. 
	
	3. The name of the author may not be used to endorse or promote products derived 
	   from this software without specific prior written permission. 

	THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
	WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
	MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
	EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
	EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
	OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
	THE POSSIBILITY OF SUCH DAMAGE.
    """

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

	# ISA Segment	
	isa_seg = segment(isa_seg_node, seg)
	isa_seg.validate()
	isa_seg.xml()

	
	# parse ISA
	# print ISA
	# loop through GS loops
	self.icvn = '00401'
	#gs = GS_loop(self)

	# get IEA segment map
	# parse IEA
	# print IEA

    
class GS_loop:
    def __init__(self, isa):
        dom_map = xml.dom.minidom.parse('map/maps.xml')
    	vers = dom_map.getElementsByTagName("version")
	for ver in vers:
	    if ver.getAttribute('icvn') == isa.icvn:
	        maps = ver.getElementsByTagName("map")

	for map in maps:
	    if map.getAttribute('fic') == 'HR' and map.getAttribute('vriic') == '004010X093':
                for node in map.childNodes:
           	    if node.nodeType == a.TEXT_NODE:
		        node.normalize()
                        self.map_file = node.data
	dom_map.unlink()
	print self.map_file

    def getMapFile(self):
    	return self.map_file

    
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

    def xml(self):
        print '<segment code="%s">' % (self.id)
    	for elem in self.element_list:
	    elem.xml()
        print '</segment>'
    
    def validate(self):
    	for elem in self.element_list:
	    elem.validate()

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

    def xml(self):
	print '<elem code="%s">%s</elem>' % (self.refdes, self.x12_elem)
    
    def validate(self):
	if len(self.x12_elem) < int(self.min_len):
	    print "too short: ", self.x12_elem, int(self.min_len)
	    raise WEDI1Error, "too short"
	if len(self.x12_elem) > int(self.max_len):
	    print "too long: ", self.x12_elem, int(self.max_len)
	    raise WEDI1Error, "too long"
	if self.x12_elem == None and self.usage == 'R':
	    raise WEDI3Error
	if not (self.__valid_code__() or codes.IsValid(self.external_codes, self.x12_elem) ):
	    raise WEDIError, "Not a valid code for this ID element"

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

class ExternalCodes:
    def __init__(self):
    	# init a map of codes from codes.xml
	pass
    def IsValid(self, key, code):
	#if not given a key, do not flag an error
    	if not key:
	    return 1
    	#check the code against the list indexed by key
	return 1

def IsValidDataType(str, data_type):
    import re
    if data_type == 'ID': 
	#pID = re.compile(r"^(?P<if>ex0):.+?^\s+inet\s(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\snetmask\s(?P<net>0x[0-9a-fA-F]{8,8})", re.M|re.S)
	pID = re.compile(r"[0-9a-zA-Z!\"&'()*+,-.\/:;?=a-z].+", re.M|re.S)
	m = pID.search(str)
	if m != None:
	    if_new  = m.group('if')
    elif data_type == 'AN': pass
    elif data_type == 'DT': pass
    elif data_type == 'TM': pass
    elif data_type[0] == 'N': pass
    elif data_type == 'R': pass
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
        print msg
        print "usage: x12n.py file"
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

if __name__ == '__main__':
    sys.exit(not main())
