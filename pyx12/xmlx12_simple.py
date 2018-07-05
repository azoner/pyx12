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
Create an X12 document from a XML data file in the simple form
"""

import xml.etree.cElementTree as et
import logging

# Intrapackage imports
import pyx12.segment
import pyx12.x12file


def convert(filename, fd_out):
    """
    Convert a XML file in simple X12 form to an X12 file
    @param filename:  libxml2 requires a file name.  '-' gives stdin
    @type filename: string
    @param fd_out: Output file
    @type fd_out: file descripter
    """
    logger = logging.getLogger('pyx12')
    wr = pyx12.x12file.X12Writer(fd_out, '~', '*', ':', '\n', '^')
    doc = et.parse(filename)
    for node in doc.iter():
        if node.tag == 'seg':
            wr.Write(get_segment(node))
    return True


def get_segment(cSegment):
    """
    Build an X12 segment from a XML node
    """
    seg_id = cSegment.get('id')
    #seg_id = cSeg.findtext('data_ele')
    seg_data = pyx12.segment.Segment(seg_id, '~', '*', ':')
    for node in cSegment.iter():
        if node.tag == 'ele':
            ele_id = node.get('id')
            if node.text != '':
                seg_data.set(ele_id, node.text)
        elif node.tag == 'comp':
            for subele in node.findall('subele'):
                subele_id = subele.get('id')
                if subele.text is not None and subele.text != '':
                    seg_data.set(subele_id, subele.text)
    return seg_data
