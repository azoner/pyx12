#! /usr/bin/env /usr/local/bin/python
# script to validate a X12N batch transaction set  and convert it into an XML document
#
#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#                John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#        Redistribution and use in source and binary forms, with or without modification, 
#        are permitted provided that the following conditions are met:
#
#        1. Redistributions of source code must retain the above copyright notice, this list 
#           of conditions and the following disclaimer. 
#        
#        2. Redistributions in binary form must reproduce the above copyright notice, this 
#           list of conditions and the following disclaimer in the documentation and/or other 
#           materials provided with the distribution. 
#        
#        3. The name of the author may not be used to endorse or promote products derived 
#           from this software without specific prior written permission. 
#
#        THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#        MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#        EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#        OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#        THE POSSIBILITY OF SUCH DAMAGE.

"""
Parse a ANSI X12N data file.
Validate against a map and codeset values.
Create a XML document based on the data file
"""

import os, os.path
import sys
import logging
from types import *
import pdb
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
    sys.stdout.write('x12lint.py %s (%s)\n' % (__version__, __date__))
    sys.stdout.write('usage: x12lint.py [options] source_files\n')
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -c <b|e>   Specify X12 character set: b=basic, e=extended\n')
    sys.stdout.write('  -d         Debug Mode.  Implies verbose output\n')
    sys.stdout.write('  -f         Force map load.  Do not use the map pickle file\n')
    sys.stdout.write('  -H         Create HTML output file\n')
    sys.stdout.write('  -l <file>  Output log\n')
    sys.stdout.write('  -m <path>  Path to map files\n')
    sys.stdout.write('  -p <path>  Path to to pickle files\n')
    sys.stdout.write('  -P         Profile script\n')
    sys.stdout.write('  -q         Quiet output\n')
    sys.stdout.write('  -v         Verbose output\n')
    sys.stdout.write('  -x <tag>   Exclude external code\n')
    
def main():
    """
    Set up environment for processing
    """
    import getopt
    param = pyx12.params.params()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:dfl:m:p:qvx:HP')
    except getopt.error, msg:
        usage()
        sys.exit(2)
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
    #param.set_param('map_path', os.path.expanduser('/usr/local/share/pyx12/map'))
    #param.set_param('pickle_path', os.path.expanduser('/tmp'))
    for o, a in opts:
        if o == '-v': logger.setLevel(logging.DEBUG)
        if o == '-q': logger.setLevel(logging.ERROR)
        if o == '-c': param.set_param('charset', a)
        if o == '-d': 
            param.set_param('debug', True)
            debug = True
        if o == '-x': param.set_param('exclude_external_codes', a)
        if o == '-f': param.set_param('force_map_load', True)
        if o == '-m': param.set_param('map_path', a)
        if o == '-p': param.set_param('pickle_path', a)
        if o == '-P': profile = True
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
                if os.path.splitext(src_filename)[1] == '.997':
                    target_997 = src_filename + '.997'
                else:
                    target_997 = os.path.splitext(src_filename)[0] + '.997'
                #fd_997 = open(target_997, 'w')
                #(fd_997, temp_997) = tempfile.mkstemp(text=True)
                fd_997 = tempfile.TemporaryFile()
                #O_EXCL
            if flag_html:
                target_html = os.path.splitext(src_filename)[0] + '.html'
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
        except IOError:
            logger.error('Could not open files')
            usage()
            sys.exit(2)
        except KeyboardInterrupt:
            print "\n[interrupt]"

    return True

if __name__ == '__main__':
    #if sys.argv[0] == 'x12lintp':
    #    import profile
    #    profile.run('pyx12.x12n_document(src_filename)', 'pyx12.prof')
    #else:
    sys.exit(not main())

