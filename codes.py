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

import os, os.path
import sys
import cPickle
import libxml2
from stat import ST_MTIME
from stat import ST_SIZE

# Intrapackage imports
import errors

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}


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
	code_file = 'map/codes.xml'
	pickle_file = '%s.%s' % (os.path.splitext(code_file)[0], 'pkl')
	id = None
	
    	# init the map of codes from the pickled file codes.pkl
	try:
	    if os.stat(code_file)[ST_MTIME] < os.stat(pickle_file)[ST_MTIME]:
		self.codes = cPickle.load(open(pickle_file))
	    else: 
	        raise "reload codes"
	except:
            try:
            	reader = libxml2.newTextReaderFilename(code_file)
            except:
            	raise errors.x12Error, 'Code file not found: %s' % (code_file)
            try:
            	ret = reader.Read()
            	if ret == -1:
                    raise errors.XML_Reader_Error, 'Read Error'
            	elif ret == 0:
                    raise errors.XML_Reader_Error, 'End of Map File'
            	while ret == 1:
                    #print 'map_if', reader.NodeType(), reader.Depth(), reader.Name()
                    if reader.NodeType() == NodeType['element_start']:
                    	cur_name = reader.Name()
                    	if cur_name == 'codeset':
		    	    code_list = []
                            base_level = reader.Depth()
                            #base_name = 'codeset'
		    	#cur_level = reader.Depth()
                    elif reader.NodeType() == NodeType['element_end']:
		    	if reader.Name() == 'codeset':
			    self.codes[id] = code_list			    
			    #del code_list
			    id = None
#			if reader.Depth() <= base_level:
#			    ret = reader.Read()
#                            if ret == -1:
#                            	raise errors.XML_Reader_Error, 'Read Error'
#                            elif ret == 0:
#                            	raise errors.XML_Reader_Error, 'End of Map File'
#                            break
                        cur_name = ''
                    elif reader.NodeType() == NodeType['text'] and base_level + 1 <= reader.Depth():
                    	if cur_name == 'id':
                            id = reader.Value()
                    	elif cur_name == 'code':
                            code_list.append(reader.Value())

                    ret = reader.Read()
                    if ret == -1:
                    	raise errors.XML_Reader_Error, 'Read Error'
                    elif ret == 0:
                    	raise errors.XML_Reader_Error, 'End of Map File'
            except errors.XML_Reader_Error:
	    	pass
        try:
            cPickle.dump(self.codes,open(pickle_file,'w'))
        except:
            pass


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
	    	raise errors.EngineError, 'Enternel Code %s is not defined' % (key)
	    if not code in self.codes[key]:
	        return 0
	return 1

    def debug_print(self):
    	for key in self.codes.keys():
	    print self.codes[key][:10]

