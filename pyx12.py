#! /usr/bin/env /usr/local/bin/python
# script to validate a X12N batch transaction set  and convert it into an XML document
#
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

# THIS IS PRE-ALPHA CODE.  IT DOES NOT WORK. 

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a XML document based on the data file
"""

import os, os.path
#import stat
import sys
#import string
from types import *
#import StringIO
#import tempfile
#import time
#import pdb
#import xml.dom.minidom

# Intrapackage imports
from errors import *
import codes
import map_index
import map_if
import x12file
from map_walker import walk_tree
from utils import *

#Global Variables
__version__ = "0.1.0"

def x12n_document():

        # Get X12 DATA file
        src = x12file.x12file(sys.stdin) 

        #Get Map of Control Segments
        control = map_if.map_if('map/map.x12.control.00401.xml')
        
        #Determine which map to use for this transaction
        for line in src:
            if line[0] == 'ISA':
                isa_seg = segment(control.getnodebypath('/ISA'), line)
                isa_seg.validate()
                icvn = isa_seg.GetElementValue('ISA12')
            elif line[0] == 'GS':
                gs_seg = segment(control.getnodebypath('/GS'), line)
                gs_seg.validate()
                fic = gs_seg.GetElementValue('GS01')
                vriic = gs_seg.GetElementValue('GS08')

                #Get map for this GS loop
                map_index_if = map_index.map_index('map/maps.xml')
                map_file = map_index_if.get_filename(icvn, vriic, fic)
                #print map_file
            else:
                break        

        #Determine which map to use for this transaction
        map = map_if.map_if(os.path.join('map', map_file))
        node = map.getnodebypath('/ST')

        for seg in src:
            #find node
            node = walk_tree(node, seg)

            #validate intra-element dependancies

            if len(seg) > node.get_child_count(): raise x12Error, 'Too many elements in segment %s' % (seg[0])
            for i in xrange(node.get_child_count()):
                # Validate Elements
                if i < len(seg):
                    if type(seg[i]) is ListType: # composite
                        # Validate composite
                        comp_node = node.get_child_node_by_idx(i)
                        if len(seg) > node.get_child_count():
                            raise x12Error, 'Too many elements in segment %s' % (seg[0])
                    else: # element
                        node.get_child_node_by_idx(i).is_valid(seg[i])
                else: #missing required elements
                    node.get_child_node_by_idx(i).is_valid(None)
                
            #get special values
            #generate xml

#############################################################################
###  SEGMENT - Link data segment to map
#############################################################################
class segment:
    """
    Parse and validate a segment data line.
    Takes a map_py node of the segment and the parsed segment line as a list
    """
    def __init__(self, node, seg):
        """
        Name:    __init__
        Desc:    Sends an xml representation of the segmens to stdout
        Params:  node - map_py node of the segment
                 seg - the parsed segment line as a list
        Returns: 
        """

        if node == None: raise x12Error
        self.node = node
        #self.id = GetChildElementText(node, 'id')
        #self.name = GetChildElementText(node, 'name')
        #self.end_tag = GetChildElementText(node, 'end_tag')
        #self.usage = GetChildElementText(node, 'usage')
        #self.req_des = GetChildElementText(node, 'req_des')
        #self.pos = GetChildElementText(node, 'pos')

        tab.incr()
        #element_nodes = node.getElementsByTagName('element')
        i = 1 
        self.element_list = []
        # APPLY LIST OF ELEMENTS TO ELEMENTS IN NODE
        for child in node.children:
            if child.base_name == 'element':
                if i < len(seg):
                    self.element_list.append(element(child, seg[i]))
                else:
                    self.element_list.append(element(child, None))
                i += 1
            elif child.base_name == 'composite':
                if i < len(seg):
                    self.element_list.append(composite(child, seg[i]))
                else:
                    self.element_list.append(composite(child, None))
                i += 1

    def __del__(self):
        tab.decr()

    def xml(self):
        """
        Name:    xml
        Desc:    Sends an xml representation of the segment to stdout
        Params:  
        Returns: 
        """

        sys.stdout.write('<segment code="%s">\n' % (self.node.id))
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
        

#############################################################################
###  ELEMENT - Link data element to map
#############################################################################
class element:
    def __init__(self, node, x12_elem):
        """
        Name:    __init__
        Desc:    Get the values for this element
        Params:  node - a map_if node of the element
                 x12_elem - the x12 element value 
        Returns: 
        """

        self.node = node
        self.x12_elem = x12_elem
        
    def __del__(self):
        tab.decr()

    def xml(self):
        """
        Name:    xml
        Desc:    Sends an xml representation of the element to stdout
        Params:  
        Returns: 
        """
        sys.stdout.write('<element code="%s">%s</element>\n' % (node.refdes, self.x12_elem))
        
    def validate(self):
        """
        Name:    xml
        Desc:    Validates the element
        Params:  
        Returns: 
        """

        return self.node.is_valid(self.x12_elem)

   
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

