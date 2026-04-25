######################################################################
# Copyright
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
"""
Locate the correct xml map file given:
    - Interchange Control Version Number (ISA12)
    - Functional Identifier Code (GS01)
    - Version / Release / Industry Identifier Code (GS08)
    - Transaction Set Purpose Code (BHT02) (For 278 only)
"""

import os.path
import logging
import xml.etree.ElementTree as et
from importlib.resources import files as _res_files

class map_index:
    """
    Interface to the maps.xml file
    """
    def __init__(self, base_path=None):
        """
        @param base_path: Override directory containing maps.xml.  If None,
                    uses package resource folder
        @type base_path: string
        """
        logger = logging.getLogger('pyx12')
        self.maps = []
        maps_index_file = 'maps.xml'
        if base_path is not None:
            logger.debug(f"Looking for map index file '{maps_index_file}' in map_path '{base_path}'")
            if not os.path.isdir(base_path):
                raise OSError(2, "Map path does not exist", base_path)
            fd = open(os.path.join(base_path, maps_index_file), encoding='utf-8')
        else:
            logger.debug(f"Looking for map index file '{maps_index_file}' in package resources")
            fd = _res_files('pyx12').joinpath('map', maps_index_file).open('rb')
        with fd:
            parser = et.XMLParser(encoding='utf-8')
            for _v in et.parse(fd, parser=parser).iter('version'):
                icvn = _v.get('icvn')
                for _m in _v.iterfind('map'):
                    self.add_map(icvn, _m.get('vriic'), _m.get('fic'),
                                 _m.get('tspc'), _m.text, _m.get('abbr'))

    def add_map(self, icvn, vriic, fic, tspc, map_file, abbr):
        self.maps.append({'icvn': icvn, 'vriic': vriic, 'fic': fic,
                          'tspc': tspc, 'map_file': map_file, 'abbr': abbr})

    def get_filename(self, icvn, vriic, fic, tspc=None):
        """
        Get the map filename associated with the given icvn, vriic, fic,
        and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a['icvn'] == icvn and a['vriic'] == vriic and a['fic'] == fic \
                    and (tspc is None or a['tspc'] == tspc):
                return a['map_file']
        return None

    def get_abbr(self, icvn, vriic, fic, tspc=None):
        """
        Get the informal abbreviation associated with the given icvn, vriic,
        fic, and tspc values
        @rtype: string
        """
        for a in self.maps:
            if a['icvn'] == icvn and a['vriic'] == vriic and a['fic'] == fic \
                    and (tspc is None or a['tspc'] == tspc):
                return a['abbr']
        return None

    def print_all(self):
        for a in self.maps:
            print(a)
