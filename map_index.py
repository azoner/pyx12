#! /usr/bin/env /usr/local/bin/python

import libxml2

import errors

#NodeType: 
#	1 for start element, 15 for end of element, 2 for attributes, 3 for text nodes, 4 for CData sections, 
#	5 for entity references, 6 for entity declarations, 7 for PIs, 8 for comments, 9 for the document nodes, 
#	10 for DTD/Doctype nodes, 11 for document fragment and 12 for notation nodes. 

#AttributeCount: provides the number of attributes of the current node. 
#BaseUri: the base URI of the node. See the XML Base W3C specification. 
#Depth: the depth of the node in the tree, starts at 0 for the root node. 
#HasAttributes: whether the node has attributes. 
#HasValue: whether the node can have a text value. 
#IsDefault: whether an Attribute node was generated from the default value 
#	defined in the DTD or schema (unsupported yet). 
#IsEmptyElement: check if the current node is empty, this is a bit bizarre 
#	in the sense that <a/> will be considered empty while <a></a> will not. 
#LocalName: the local name of the node. 
#Name: the qualified name of the node, equal to (Prefix:)LocalName. 
#NamespaceUri: the URI defining the namespace associated with the node. 
#Prefix: a shorthand reference to the namespace associated with the node. 
#Value: provides the text value of the node if present. 
#XmlLang: the xml:lang scope within which the node resides. 


NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

"""
       if not self.map_file:
            raise errors.GSError, 'Map file not found, icvn=%s, fic=%s, vriic=%s' % (isa.icvn,self.fic,self.vriic)
"""

class map_index:
    def __init__(self, map_file):
        self.maps = []
        try:
	    reader = libxml2.newTextReaderFilename(map_file)
    	except:
            raise errors.GSError, 'Map file not found: %s' % (map_file)
		    
        while reader.Read():
    	    #processNode(reader)
    	    if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'version':
            	while reader.MoveToNextAttribute():
	    	    if reader.Name() == 'icvn':
		    	icvn = reader.Value()

    	    if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'version':
	    	icvn = None

    	    if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'map':
		file_name = ''
            	while reader.MoveToNextAttribute():
	    	    if reader.Name() == 'vriic':
		    	vriic = reader.Value()
		    elif reader.Name() == 'fic':
		    	fic = reader.Value()

    	    if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'map':
    		self.maps.append((icvn, vriic, fic, file_name))
		vriic = None
		fic = None
		file_name = None

    	    if reader.NodeType() == NodeType['text']:
		file_name = reader.Value()

    
    def add_map(self, icvn, vriic, fic, map_file):
    	self.maps.append((icvn, vriic, fic, map_file))
    	#self.icvn = icvn
	#self.vriic = vriic
	#self.fic = fic
	#self.map_file = map_file
    
    def get_filename(self, icvn, vriic, fic):
    	for a in self.maps:
	    if a[0] == icvn and a[1] == vriic and a[2] == fic:
    		return a[3]
    def print_all(self):
    	for a in self.maps:
	    print a[0], a[1], a[2], a[3]

