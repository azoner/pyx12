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
Create an X12 document from a XML data file in the idtag form
"""

import libxml2
import logging

# Intrapackage imports
import pyx12.segment

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3,
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8,
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12, 'CData2': 14}

def convert(filename, fd_out):
    """
    Convert a XML file in simple X12 form to an X12 file
    @param filename:  libxml2 requires a file name.  '-' gives stdin
    @type filename: string
    @param fd_out: Output file
    @type fd_out: file descripter
    """
    logger = logging.getLogger('pyx12')
    try:
        reader = libxml2.newTextReaderFilename(filename)
        ret = reader.Read()
        found_text = False
        subele_term = ''
        while ret == 1:
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                found_text = False
                cur_name = reader.Name()
                if cur_name == 'seg':
                            seg_data = pyx12.segment.Segment(reader.Value(), \
                                '~', '*', ':')
                elif cur_name == 'ele':
                    while reader.MoveToNextAttribute():
                        if reader.Name() == 'id':
                            ele_id = reader.Value()
                #elif cur_name == 'comp':
                #    comp = []
                elif cur_name == 'subele':
                    while reader.MoveToNextAttribute():
                        if reader.Name() == 'id':
                            subele_id = reader.Value()
            elif tmpNodeType == NodeType['CData2']:
                if cur_name == 'ele':
                    seg_data.set(ele_id, reader.Value().replace('\n', ''))
                    found_text = True
                elif cur_name == 'subele':
                    seg_data.set(subele_id, reader.Value().replace('\n', ''))
                    found_text = True
            elif tmpNodeType == NodeType['text']:
                if cur_name == 'ele':
                    if ele_id == 'ISA16':
                        subele_term = ':'
                    else:
                        seg_data.set(ele_id, reader.Value())
                    found_text = True
                elif cur_name == 'subele':
                    #comp.set(subele_id, reader.Value())
                    seg_data.set(subele_id, reader.Value())
                    found_text = True
            elif tmpNodeType == NodeType['element_end']:
                cur_name = reader.Name()
                if cur_name == 'seg':
                    if seg_data.get_seg_id() == 'ISA':
                        seg_str = seg_data.format()
                        fd_out.write(seg_str[:-1] + seg_str[-3] + subele_term + seg_str[-1])
                    else:
                        fd_out.write(seg_data.format())
                    fd_out.write('\n')
                elif cur_name == 'ele':
                    if not found_text:
                        seg_data.set(ele_id, '')
                        found_text = True
                    ele_id = None
                elif cur_name == 'subele' and not found_text:
                    #comp.append('')
                    seg_data.set(subele_id, '')
                    found_text = True
                    subele_id = None
                elif cur_name == 'comp':
                    #seg_data.append(string.join(comp, ':'))
                    subele_id = None
                cur_name = None
            ret = reader.Read()
    except:
        logger.error('Read of file "%s" failed' % (filename))
        raise
        return False
    return True
