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


"""
External Codes interface
"""

import xml.dom.minidom

# Intrapackage imports
import errors

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

