#! /usr/bin/env /usr/local/bin/python
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
Test the files in ./files
Compare the 997 output against existing output
"""

import os, os.path
import sys
import logging
from types import *
import pdb
import tempfile
#import difflib
import subprocess

# Intrapackage imports
import pyx12
import pyx12.x12n_document
import pyx12.params

def skip_headers(line1):
    if line1[:3] == 'ISA' or line1[:2] == 'GS':
        return True
    else:
        return False
   
def diff(file1, file2):
    diff_prg = "/usr/bin/diff"
    diff_args = (diff_prg, '-uBb', file1, file2)
    sp = subprocess.Popen(diff_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stout, stderr) = sp.communicate()
    if stderr:
        print stderr
    return stout
    
def main():
    """
    Set up environment for processing
    """
    param = pyx12.params.params()
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

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
    param.set('map_path', os.path.abspath('../map'))
    if not debug:
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass

    #diff = difflib.Differ(skip_headers)
    try:
        dir1 = os.path.abspath('./files')
        os.chdir(dir1)
        names = os.listdir(dir1)
    except os.error:
        logger.critical('Can''t list %s' % (dir1))
        names = []
    names.sort()
    for name in names:
        src_filename = os.path.join(dir1, name)
        if os.path.isfile(src_filename):
            head, tail = name[:-4], name[-4:]
            if tail == '.txt':
                try:
                    sys.stdout.write('\n' + ('=' * 60))
                    sys.stdout.write('\nChecking: %s\n' % (os.path.basename(src_filename)))
                    if flag_997:
                        if os.path.splitext(src_filename)[1] == '.997':
                            target_997 = src_filename + '.997'
                            base_997 = src_filename + '.997.base'
                        else:
                            target_997 = os.path.splitext(src_filename)[0] + '.997'
                            base_997 = os.path.splitext(src_filename)[0] + '.997.base'
                        fd_997 = tempfile.NamedTemporaryFile()
                    if not os.path.isfile(base_997):
                        logger.critical('Base 997 not found: %s' % (os.path.basename(base_997)))
                        continue
                    #if flag_html:
                    #    target_html = os.path.splitext(src_filename)[0] + '.html'
                    #    fd_html = open(target_html, 'w')

                    pyx12.x12n_document.x12n_document(param, src_filename, fd_997, fd_html)

                    fd_997.seek(0)
                    target_997 = fd_997.name
                    fd_new = tempfile.NamedTemporaryFile()
                    for line in fd_997.readlines():
                        if line[:3] not in ('ISA', 'GS*', 'ST*', 'SE*', 'GE*', 'IEA'):
                            fd_new.write(line)
                    #fd_new.seek(0)
                    #sys.stdout.write(fd_new.read())
                    fd_new.seek(0)
                    
                    fd_base = open(base_997, 'r')
                    fd_orig = tempfile.NamedTemporaryFile()
                    for line in fd_base.readlines():
                        if line[:3] not in ('ISA', 'GS*', 'ST*', 'SE*', 'GE*', 'IEA'):
                            fd_orig.write(line)
                    fd_orig.write(fd_base.read())
                    #fd_orig.seek(0)
                    #sys.stdout.write(fd_orig.read())
                    fd_orig.seek(0)
                    #open(target_997, 'w').write(fd_997.read())
                    #fd_997.close()

                    diff_txt = diff(fd_orig.name, fd_new.name)
                    if diff:
                        for line in diff_txt.splitlines(True):
                            if '/tmp/' not in line:
                                sys.stdout.write(line)
                    else:
                        sys.stdout.write(': OK')
                    sys.stdout.write('\n')
                except IOError:
                    sys.stderr.write('Error: Could not open files (%s)\n' % (name))
                    continue
                    #sys.exit(2)
                except KeyboardInterrupt:
                    print "\n[interrupt]"

    return True

if __name__ == '__main__':
    sys.exit(not main())
