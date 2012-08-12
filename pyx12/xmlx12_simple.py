######################################################################
# Copyright Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
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
    try:
        for cSeg in et.parse(filename).iterfind('seg'):
            seg_id = cSeg.get('id')
            #seg_id = cSeg.findtext('data_ele')
            seg_data = pyx12.segment.Segment(seg_id, '~', '*', ':')
            for ele in cSeg.findall('ele'):
                ele_id = ele.get('id')
                if ele.text.strip() != '':
                    seg_data.set(ele_id, ele.text.strip())
                for subele in ele.findall('subele'):
                    subele_id = subele.get('id')
                    seg_data.set(subele_id, subele.text.strip())
            wr.Write(seg_data) 
    except:
        logger.error('Read of file "%s" failed' % (filename))
        raise
        #return False
    return True
