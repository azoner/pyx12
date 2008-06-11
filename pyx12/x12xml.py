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
Interface to create a XML rendering of the X12 document
"""

# Intrapackage imports
from errors import *
from xmlwriter import XMLWriter
from map_walker import pop_to_parent_loop

class x12xml(object):
    def __init__(self, fd, type, dtd_urn):
        self.writer = XMLWriter(fd)
        if dtd_urn:
            self.writer.doctype(
                type, u"-//J Holland//DTD XML X12 Document Conversion1.0//EN//XML",
                u"%s" % (dtd_urn))
        self.writer.push(type)

    def __del__(self):
        pass

    def seg(self, seg_node, seg_data):
        """
        """
        pass

    def _path_list(self, path_str):
        """
        Get list of path nodes from path string
        @rtype: list
        """
        return filter(lambda x: x!='', path_str.split('/'))

    def _get_path_match_idx(self, last_path, cur_path):
        """
        Get the index of the last matching path nodes
        """
        match_idx = 0
        for i in range(min(len(cur_path), len(last_path))):
            if cur_path[i] != last_path[i]:
                break
            match_idx += 1
        return match_idx
