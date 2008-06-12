#! /usr/bin/env python

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
Parse a ANSI X12N data file.
Validate against a map and codeset values.
"""

import os, os.path
import sys
import logging
#from types import *
import tempfile

# Intrapackage imports
import pyx12
import pyx12.x12n_document
import pyx12.params

__author__  = pyx12.__author__
__status__  = pyx12.__status__
__version__ = pyx12.__version__
__date__    = pyx12.__date__

def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stderr.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stderr.write('usage: %s [options] source_files\n' % (pgm_nme))
    sys.stderr.write('\noptions:\n')
    sys.stderr.write('  -c <file>  XML configuration file\n')
    sys.stderr.write('  -d         Debug Mode.  Implies verbose output\n')
    sys.stderr.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stderr.write('  -H         Create HTML output file\n')
    sys.stderr.write('  -l <file>  Output log\n')
    sys.stderr.write('  -m <path>  Path to map files\n')
    #sys.stderr.write('  -o <file>  Override file\n')
    sys.stderr.write('  -p <path>  Path to to pickle files\n')
    sys.stderr.write('  -P         Profile script\n')
    sys.stderr.write('  -q         Quiet output\n')
    sys.stderr.write('  -s <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stderr.write('  -t <file>  XSL Transform, applied to the map.  May be used multiple times.\n')
    sys.stderr.write('  -v         Verbose output\n')
    sys.stderr.write('  -x <tag>   Exclude external code\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:dfl:m:p:qs:t:vx:HP')
    except getopt.error, msg:
        usage()
        return False
    logger = logging.getLogger('pyx12')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    #fd_src = None
    fd_997 = None
    fd_html = None

    flag_html = False
    flag_997 = True
    profile = False
    debug = False
    configfile = None
    xslt_files = []
    for opt, val in opts:
        if opt == '-c':
            configfile = val
    param = pyx12.params.params(configfile)

    for xslt_file in param.get('xslt_files'):
        if os.path.isfile(xslt_file):
            xslt_files.append(xslt_file)
        else:
            logger.debug("XSL Transform '%s' not found" % (xslt_file))

    for opt, val in opts:
        if opt == '-v': logger.setLevel(logging.DEBUG)
        if opt == '-q': logger.setLevel(logging.ERROR)
        if opt == '-d': 
            param.set('debug', True)
            debug = True
            logger.setLevel(logging.DEBUG)
        if opt == '-x': param.set('exclude_external_codes', val)
        if opt == '-f': param.set('force_map_load', True)
        if opt == '-m': param.set('map_path', val)
        if opt == '-p': param.set('pickle_path', val)
        if opt == '-P': profile = True
        if opt == '-s': param.set('charset', val)
        if opt == '-t': 
            if os.path.isfile(val):
                xslt_files.append(val)
            else:
                logger.debug("XSL Transform '%s' not found" % (val))
        if opt == '-H': flag_html = True
        if opt == '-l':
            try:
                hdlr = logging.FileHandler(val)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr) 
            except IOError:
                logger.error('Could not open log file: %s' % (val))

    if not debug and not profile:
        try:
            #print 'import psyco'
            import psyco
            psyco.full()
        except ImportError:
            pass

    for src_filename in args:
        try:
            if not os.path.isfile(src_filename):
                logger.error('Could not open file "%s"' % (src_filename))
                continue
            #fd_src = open(src_filename, 'U')
            if flag_997:
                if os.path.splitext(src_filename)[1] == '.txt':
                    target_997 = os.path.splitext(src_filename)[0] + '.997'
                else:
                    target_997 = src_filename + '.997'
                #fd_997 = open(target_997, 'w')
                #(fd_997, temp_997) = tempfile.mkstemp(text=True)
                fd_997 = tempfile.TemporaryFile()
                #O_EXCL
            if flag_html:
                if os.path.splitext(src_filename)[1] == '.txt':
                    target_html = os.path.splitext(src_filename)[0] + '.html'
                else:
                    target_html = src_filename + '.html'
                fd_html = open(target_html, 'w')

            if profile:
                import profile
                prof_str = 'pyx12.x12n_document.x12n_document(param, src_filename, ' \
                        + 'fd_997, fd_html, None, xslt_files)'
                print prof_str
                print param
                profile.run(prof_str, 'pyx12.prof')
            else:
                if pyx12.x12n_document.x12n_document(param=param, src_file=src_filename, 
                        fd_997=fd_997, fd_html=fd_html, fd_xmldoc=None, xslt_files=xslt_files):
                    sys.stderr.write('%s: OK\n' % (src_filename))
                else:
                    sys.stderr.write('%s: Failure\n' % (src_filename))
            fd_997.seek(0)
            open(target_997, 'w').write(fd_997.read())
            if fd_997:
                fd_997.close()
            if fd_html:
                fd_html.close()
        except IOError:
            logger.error('Could not open files')
            usage()
            return False
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

if __name__ == '__main__':
    #if sys.argv[0] == 'x12validp':
    #    import profile
    #    profile.run('pyx12.x12n_document(src_filename)', 'pyx12.prof')
    #else:
    sys.exit(not main())

