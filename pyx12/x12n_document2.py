#####################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#
#    $Id$

"""
Parse a ANSI X12N data file.  Validate against a map and codeset values.
Create XML, HTML, and 997 documents based on the data file.
"""

import os, os.path
import logging

# Intrapackage imports
import pyx12
import error_handler
import errors
import map_index
import map_if
import x12context
from map_walker import walk_tree

def get_xmldoc(fd, param, xmlout='simple'):
    if xmlout == 'idtag':
        import x12xml_idtag
        return x12xml_idtag.x12xml_idtag(fd_xmldoc, param.get('idtag_dtd'))
    elif xmlout == 'idtagqual':
        import x12xml_idtagqual
        return x12xml_idtagqual.x12xml_idtagqual(fd_xmldoc, param.get('idtagqual_dtd'))
    else:
        import x12xml_simple
        return x12xml_simple.x12xml_simple(fd_xmldoc, param.get('simple_dtd'))

def x12n_xml(param, src_file, fd_xmldoc, xslt_files = []):
    """
    Primary X12 validation function
    @param param: pyx12.param instance
    @param src_file: Source document
    @type src_file: string
    @param fd_997: 997 output document
    @type fd_997: file descriptor
    @param fd_html: HTML output document
    @type fd_html: file descriptor
    @param fd_xmldoc: XML output document
    @type fd_xmldoc: file descriptor
    @rtype: boolean
    """
    map_path = param.get('map_path')
    logger = logging.getLogger('pyx12')
    logger.debug('MAP PATH: %s' % (map_path))
    errh = error_handler.err_handler()
    
    # Get X12 DATA file
    try:
        context = x12context.X12ContextReader(param, errh, src_file, xslt_files)
    except pyx12.errors.X12Error:
        logger.error('"%s" does not look like an X12 data file' % (src_file))
        return False

    if fd_xmldoc:
        logger.debug('xmlout: %s' % (param.get('xmlout')))
        xmldoc = get_xmldoc(fd_xmldoc, param, param.get('xmlout'))

    valid = True
    for datatree in context.iter_segments():
        for datanode in datatree.iterate_loop_segments():
            seg_id = datanode['segment'].id
            #valid &= node.is_valid(seg, errh)

        if fd_xmldoc:
            xmldoc.seg_context(node, seg)

    src.cleanup() #Catch any skipped loop trailers
    errh.handle_errors(src.pop_errors())
    
    if fd_xmldoc:
        del xmldoc

    try:
        if not valid or errh.get_error_count() > 0:
            return False
        else:
            return True
    except Exception:
        print(errh)
        return False
