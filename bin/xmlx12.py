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
import string
#import StringIO
#import tempfile
import pdb
#import profile

# Intrapackage imports
import pyx12.params
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
    sys.stdout.write('  -c <file>  XML configuration file\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -o <file>  Output file\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')

def convert(filename, fd_out):
    global logger
    try:
        reader = libxml2.newTextReaderFilename(filename)
        ret = reader.Read()
        while ret == 1:
            tmpNodeType = reader.NodeType()
            if tmpNodeType == NodeType['element_start']:
                cur_name = reader.Name()
                if cur_name == 'seg':
                    while reader.MoveToNextAttribute():
                        if reader.Name() == 'id':
                            #fd_out.write(reader.Value())
                            seg_data = pyx12.segment.segment(reader.Value(), \
                                '~', '*', ':')
                elif cur_name == 'comp':
                    comp = []
                elif cur_name == 'ele' and reader.IsEmptyElement():
                    seg_data.append('')
            elif tmpNodeType == NodeType['CData2']:
                #print tmpNodeType, cur_name, reader.Name(), reader.Value()
                #pdb.set_trace()
                if cur_name in ('ele', 'subele'):
                    seg_data.append(reader.Value().replace('\n', ''))
            elif tmpNodeType == NodeType['text']:
                if cur_name == 'ele':
                    seg_data.append(reader.Value())
                elif cur_name == 'subele':
                    comp.append(reader.Value())
            elif tmpNodeType == NodeType['element_end']:
                cur_name = reader.Name()
                if cur_name == 'seg':
                    fd_out.write(seg_data.format())
                    fd_out.write('\n')
                #elif cur_name == 'ele':
                #    fd_out.write('*')
                elif cur_name == 'comp':
                    seg_data.append(string.join(comp, ':'))
                #elif cur_name == 'subele':
                #    fd_out.write(':')
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
        opts, args = getopt.getopt(sys.argv[1:], 'c:l:o:qvh')
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
    configfile = None
    for o, a in opts:
        if o == '-c':
            configfile = a
    if configfile:
        param = pyx12.params.params('/usr/local/etc/pyx12.conf.xml',\
            os.path.expanduser('~/.pyx12.conf.xml'), \
            configfile)
    else:
        param = pyx12.params.params('/usr/local/etc/pyx12.conf.xml',\
            os.path.expanduser('~/.pyx12.conf.xml'))

    #param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-o': target_x12 = a
        if o == '-H': flag_html = True
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
        #target_x12 = os.path.splitext(src_filename)[0] + '.xml'
    else:
        fd_x12 = sys.stdout

    try:
        result = convert(src_filename, fd_x12)
        fd_x12.close()
        if not result:
            logger.error('File %s had errors.' % (src_filename))
            #if target_x12:
            #    os.remove(target_x12)
            return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
        
    return True

#profile.run('x12n_document(src_filename)', 'pyx12.prof')
if __name__ == '__main__':
    try:
        import psyco
        #psyco.full()
    except ImportError:
        pass

    sys.exit(not main())
