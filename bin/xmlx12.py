#! /usr/bin/env /usr/local/bin/python

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
Create an X12 document from a XML data file
"""

import os, os.path
import sys
import libxml2
import logging

# Intrapackage imports
import pyx12.segment

#Global Variables
__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3,
    'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8,
    'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12, 'CData2': 14}

logger = None

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -o <file>  Output file\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')

def convert(filename, fd_out):
    """
    Convert a XML file in simple X12 form to an X12 file
    @param filename:  libxml2 requires a file name.  '-' gives stdin
    @type filename: string
    @param fd_out: Output file
    @type fd_out: file descripter
    """
    global logger
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
                    while reader.MoveToNextAttribute():
                        if reader.Name() == 'id':
                            #fd_out.write(reader.Value())
                            seg_data = pyx12.segment.segment(reader.Value(), \
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

def main():
    """Script main program."""
    global logger
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:o:qvh')
    except getopt.error, msg:
        usage()
        raise
        return False
    logger = logging.getLogger('pyx12')
    hdlr = logging.FileHandler('./run.log')
    stderr_hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.addHandler(stderr_hdlr)
    logger.setLevel(logging.INFO)
    target_x12 = None
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-o': target_x12 = a
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr)
            except IOError:
                logger.error('Could not open log file: %s' % (a))
                return False

    if len(args) > 0:
        src_filename = args[0]
        logger.debug('src=%s    xml=%s' % (src_filename, target_x12))
    else:
        src_filename = '-'
    if target_x12:
        try:
            fd_x12 = open(target_x12, 'w')
        except:
            logger.error('Could not open file %s' % (target_x12))
            return False
    else:
        fd_x12 = sys.stdout

    try:
        result = convert(src_filename, fd_x12)
        fd_x12.close()
        if not result:
            logger.error('File %s had errors.' % (src_filename))
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    sys.exit(not main())
