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

# Intrapackage imports
import errors
import codes
from utils import *

#Global Variables
subele_term = None

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
	global subele_term
	subele_term = self.subele_term

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
	if lines[-1][0] == 'IEA':
	    iea_seg = segment(iea_seg_node, lines[-1])
	    iea_seg.validate()
	else:
	    raise errors.WEDI1Error, 'Last segment should be IEA, is "%s"' % (lines[-1][0])

	# Loop through GS segments
	for loop in GetExplicitLoops(lines[:-1], 'GS', 'GE', 6, 2):
	    print loop[0]
	    print loop[-1]
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
	    raise errors.WEDI1Error, 'Last segment should be GE, is "%s"' % (gs[-1:][0][0])

	#Get map for this GS loop
        dom_maps = xml.dom.minidom.parse('map/maps.xml')
    	vers = dom_maps.getElementsByTagName("version")
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
	    raise errors.GSError, 'Map file not found, icvn=%s, fic=%s, vriic=%s' % (isa.icvn,self.fic,self.vriic)
	dom_maps.unlink()

	# Get map for this GS loop
	#print "--load whole dom"
	#self.dom_map = xml.dom.minidom.parse('map/' + self.map_file)
	#print "--end load whole dom"

	# Loop through ST segments
	#for loop in GetExplicitLoops(gs[1:-1], 'ST', 'SE', 2, 2):
	#    st = ST_loop(self, isa, loop)
	
	ge_seg.xml()
	dom_gs.unlink()

    def getMapFile(self):
    	return self.map_file

class ST_loop:
    def __init__(self, gs, isa, st):
	seg_nodes = gs.dom_map.getElementsByTagName("segment")
	for seg_node in seg_nodes:
	    if GetChildElementText(seg_node, 'id') == 'ST':
	    	st_seg_node = seg_node
	    if GetChildElementText(seg_node, 'id') == 'SE':
	    	se_seg_node = seg_node
	    if GetChildElementText(seg_node, 'id') == 'BHT':
	    	bht_seg_node = seg_node

	st_seg = segment(st_seg_node, st[0])
	st_seg.validate()
	st_seg.xml()

	bht_seg = segment(bht_seg_node, st[1])
	bht_seg.validate()
	bht_seg.xml()

	# ST Loop handles the Hierarchy of HL Loops under it
	transaction_node = gs.dom_map.getElementsByTagName("transaction")

	# Loop through HL delimited Loops
	#for loop in GetHLLoops(st[2:-1]):
	#    hl = HL_loop(self, transaction_node, loop)

	se_seg = segment(se_seg_node, st[-1:][0])
	se_seg.validate()
	se_seg.xml()
	

class HL_loop:
    """
    Takes a dom node of the loop and the parsed segment lines as a list
    """
    def __init__(self, st, parent_node, loop):
        """
        Name:    __init__
        Desc:    Handles the parsing of loop started by HL segments 
        Params:  st - parent class
		 parent_node - dom node containing the loop
		 loop - parsed segment lines as a list
        Returns: 
        """
	seg_nodes = parent_node.getElementsByTagName("loop")
	for seg_node in seg_nodes:
	    if GetChildElementText(seg_node, 'id') == 'HL':
	    	hl_seg_node = seg_node

	print loop[0]
    
	#hl_seg = segment(hl_seg_node, loop[0])
	#hl_seg.validate()
	#hl_seg.xml()


class segment:
    """
    Takes a dom node of the segment and the parsed segment line as a list
    """
    def __init__(self, node, seg):
        """
        Name:    __init__
        Desc:    Sends an xml representation of the segmens to stdout
        Params:  node - dom node of the segment
		 seg - the parsed segment line as a list
        Returns: 
        """
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
        """
        Name:    xml
        Desc:    Sends an xml representation of the segment to stdout
        Params:  
        Returns: 
        """

        sys.stdout.write('<segment code="%s">\n' % (self.id))
    	for elem in self.element_list:
	    elem.xml()
        sys.stdout.write('</segment>\n') # % (tab.indent()))
    
    def validate(self):
        """
        Name:    validate
        Desc:    Validate the segment and child elements or composites
        Params:  
        Returns: 
        """
    	for elem in self.element_list:
	    elem.validate()
	    
    def GetElementValue(self, refdes):
        """
        Name:    GetElementValue
        Desc:    Get the value of an X12 element by name
        Params:  refdes - the X12 element Reference Identifier
        Returns: Value of the element, or None if not found
        """
    	for elem in self.element_list:
	    if elem.refdes == refdes:
	        return elem.x12_elem
	return None
    	

class element:
    def __init__(self, node, x12_elem):
        """
        Name:    __init__
        Desc:    Get the values for this element
        Params:  node - a dom node of the element
		 x12_elem - the x12 element value 
        Returns: 
        """
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
        """
        Name:    xml
        Desc:    Sends an xml representation of the element to stdout
        Params:  
        Returns: 
        """
	sys.stdout.write('<elem code="%s">%s</elem>\n' % (self.refdes, self.x12_elem))
    
    def validate(self):
        """
        Name:    xml
        Desc:    Validates the element
        Params:  
        Returns: 
        """
    	if self.x12_elem == '' or self.x12_elem is None:
    	    if self.usage == 'N':
	    	return 1
    	    elif self.usage == 'R':
	    	raise errors.WEDI1Error, 'Element %s is required' % (self.refdes)
    	if (not self.data_type is None) and (self.data_type == 'R' or self.data_type[0] == 'N'):
	    elem = string.replace(string.replace(self.x12_elem, '-', ''), '.', '')
	    if len(elem) < int(self.min_len):
	    	raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
		    elem, int(self.min_len))
	    if len(elem) > int(self.max_len):
	    	raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
		    elem, int(self.min_len))
	else:
	    if len(self.x12_elem) < int(self.min_len):
	    	raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
		    self.x12_elem, int(self.min_len))
	    if len(self.x12_elem) > int(self.max_len):
	    	raise errors.WEDI1Error, 'Element %s is too short - "%s" is len=%i' % (self.refdes,
		    self.x12_elem, int(self.min_len))

	if self.x12_elem == None and self.usage == 'R':
	    raise errors.WEDI3Error
	if not (self.__valid_code__() or codes.IsValid(self.external_codes, self.x12_elem) ):
	    raise errors.WEDIError, "Not a valid code for this ID element"
	if not IsValidDataType(self.x12_elem, self.data_type, 'E'):
	    raise errors.WEDI1Error, "Invalid X12 datatype: '%s' is not a '%s'" % (self.x12_elem, self.data_type) 

    def __valid_code__(self):
        """
        Name:    __valid_code__
        Desc:    Verify the x12 element value is in the given list of valid codes
        Params:  
        Returns: 1 if found, else 0
        """
        if not self.valid_codes:
	    return 1
	if self.x12_elem in self.valid_codes:
	    return 1
	return 0


class composite:
    def __init__(self, node, x12_elem):
        """
        Name:    __init__
        Desc:    Get the values for this composite
        Params:  node - a dom node of the composite
		 x12_elem - the x12 element value 
        Returns: 
        """
        self.node = node
	self.x12_elem = x12_elem
    	self.name = GetChildElementText(node, 'name')
    	self.usage = GetChildElementText(node, 'usage')
    	self.req_des = GetChildElementText(node, 'req_des')
    	self.seq = GetChildElementText(node, 'seq')
    	self.refdes = GetChildElementText(node, 'refdes')

	composite = string.split(string.strip(x12_elem), subele_term)
	i = 0 
	self.sub_element_list = []
	for child in node.childNodes:
	    if child.nodeType == child.ELEMENT_NODE and child.tagName == 'element':
	        if i < len(composite):
	            self.sub_element_list.append(element(child, composite[i]))
	        else:
	            self.sub_element_list.append(element(child, None))
	        i = i + 1

    def xml(self):
        """
        Name:    xml
        Desc:    Sends an xml representation of the composite to stdout
        Params:  
        Returns: 
        """
        sys.stdout.write('<composite code="%s">\n' % (self.refdes))
    	for sub_elem in self.sub_element_list:
	    sub_elem.xml()
        sys.stdout.write('</composite>\n')

    def validate(self):
        """
        Name:    validate
        Desc:    Validates the composite
        Params:  
        Returns: 1 on success
        """
    	if self.x12_elem == '' or self.x12_elem is None:
    	    if self.usage == 'N':
	    	return 1
    	    elif self.usage == 'R':
	    	raise errors.WEDI1Error, 'Composite %s is required' % (self.refdes)
    	for sub_elem in self.sub_element_list:
	    sub_elem.validate()
    
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

codes = codes.ExternalCodes()
tab = Indent()

if __name__ == '__main__':
    sys.exit(not main())

