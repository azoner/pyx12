######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Apply local overrides to the current map.
Overrides defined in a xml document. 
"""

import libxml2
import errors


class map_override:
    """
    Apply local overrides to the current map. Overrides defined in a xml document.
    """
    def __init__(self, map_root, override_file, icvn, vriic, fic):
        try:
            reader = libxml2.newTextReaderFilename(map_file)
        except:
            raise errors.EngineError, 'Map file not found: %s' % (map_file)
                    
        NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, \
            'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, \
            'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, \
            'notation': 12}

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
                #self.maps.append((icvn, vriic, fic, file_name))
                vriic = None
                fic = None
                file_name = None

            if reader.NodeType() == NodeType['text']:
                file_name = reader.Value()

    def _set_value(self, map_root, path, variable, value):
        pass

    def _append_value(self, map_root, path, variable, value):
        pass

    def _reset_list(self, map_root, path, variable, value):
        pass

