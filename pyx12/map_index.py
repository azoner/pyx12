######################################################################
# Copyright (c) 2001-2008 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$

"""
Locate the correct xml map file given:
    - Interchange Control Version Number (ISA12)
    - Functional Identifier Code (GS01)
    - Version / Release / Industry Identifier Code (GS08)
    - Transaction Set Purpose Code (BHT02) (For 278 only)
"""

import libxml2
import errors

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

class map_index(object):
    """
    Interface to the maps.xml file
    """
    def __init__(self, map_index_file):
        """
        @param map_index_file: Absolute path of maps.xml
        @type map_index_file: string
        """
        self.maps = []
        tspc = None
        abbr = None
        try:
            reader = libxml2.newTextReaderFilename(map_index_file)
        except:
            raise errors.EngineError, 'Map file not found: %s' % (map_index_file)
                    
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
                    elif reader.Name() == 'tspc':
                        tspc = reader.Value()
                    elif reader.Name() == 'abbr':
                        abbr = reader.Value()

            if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'map':
                self.maps.append((icvn, vriic, fic, tspc, file_name, abbr))
                vriic = None
                fic = None
                tspc = None
                abbr = None
                file_name = None

            if reader.NodeType() == NodeType['text']:
                file_name = reader.Value()

    
    def add_map(self, icvn, vriic, fic, tspc, map_file, abbr):
        self.maps.append((icvn, vriic, fic, tspc, map_file, abbr))
    
    def get_filename(self, icvn, vriic, fic, tspc=None):
        """
        Get the map filename associated with the given icvn, vriic, fic, 
        and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a[0] == icvn and a[1] == vriic and a[2] == fic \
                    and (tspc is None or a[3] == tspc):
                return a[4]
        return None

    def get_abbr(self, icvn, vriic, fic, tspc=None):
        """
        Get the informal abbreviation associated with the given icvn, vriic, 
        fic, and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a[0] == icvn and a[1] == vriic and a[2] == fic \
                    and (tspc is None or a[3] == tspc):
                return a[5]
        return None

    def print_all(self):
        for a in self.maps:
            print(a[0], a[1], a[2], a[3], a[4], a[5])

