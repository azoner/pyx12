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
Parse a ANSI X12N data file.
Validate against a map and codeset values.
"""

import os, os.path
import sys
import logging
from types import *
#import pdb
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
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_files\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -c <file>  XML configuration file\n')
    sys.stdout.write('  -d         Debug Mode.  Implies verbose output\n')
    sys.stdout.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stdout.write('  -H         Create HTML output file\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -m <path>  Path to map files\n')
    #sys.stdout.write('  -o <file>  Override file\n')
    sys.stdout.write('  -p <path>  Path to to pickle files\n')
    sys.stdout.write('  -P         Profile script\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -s <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stdout.write('  -v         Verbose output\n')
    sys.stdout.write('  -x <tag>   Exclude external code\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:dfl:m:p:qs:vx:HP')
    except getopt.error, msg:
        usage()
        return False
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.INFO)
    #formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    fd_src = None
    fd_997 = None
    fd_html = None

    flag_html = False
    flag_997 = True
    profile = False
    debug = False
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

    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-d': 
            param.set('debug', True)
            debug = True
            logger.setLevel(logging.DEBUG)
        if o == '-x': param.set('exclude_external_codes', a)
        if o == '-f': param.set('force_map_load', True)
        if o == '-m': param.set('map_path', a)
        if o == '-p': param.set('pickle_path', a)
        if o == '-P': profile = True
        if o == '-s': param.set('charset', a)
        if o == '-H': flag_html = True
        if o == '-l':
            try:
                hdlr = logging.FileHandler(a)
                hdlr.setFormatter(formatter)
                logger.addHandler(hdlr) 
            except IOError:
                logger.error('Could not open log file: %s' % (a))
        #if o == '-9': target_997 = os.path.splitext(src_filename)[0] + '.997'

    if not debug:
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass

    for src_filename in args:
        try:
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
                profile.run('pyx12.x12n_document.x12n_document(param, src_filename, fd_997, fd_html)', 
                    'pyx12.prof')
            else:
                if pyx12.x12n_document.x12n_document(param, src_filename, fd_997, fd_html):
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

