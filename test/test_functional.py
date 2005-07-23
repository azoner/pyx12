#! /usr/bin/env /usr/local/bin/python
#
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
Test the files in ./files
Compare the 997 output against existing output
"""

import os, os.path
import sys
import logging
from types import *
#import pdb
import tempfile
#import difflib
import subprocess

# Intrapackage imports
import pyx12
import pyx12.x12n_document
import pyx12.params

logger = None

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
    
def test_997(src_filename, param):
    """
    Compare the 997 output against a known good 997
    """
    global logger
    try:
        if os.path.splitext(src_filename)[1] == '.997':
            target_997 = src_filename + '.997'
            base_997 = src_filename + '.997.base'
        else:
            target_997 = os.path.splitext(src_filename)[0] + '.997'
            base_997 = os.path.splitext(src_filename)[0] + '.997.base'
        fd_997 = tempfile.NamedTemporaryFile()
        if not os.path.isfile(base_997):
            logger.info('Base 997 not found: %s' % (os.path.basename(base_997)))
            return False

        pyx12.x12n_document.x12n_document(param, src_filename, fd_997, None)

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
        sys.stdout.write('%s ... ' % (os.path.basename(src_filename)))
        if diff_txt:
            sys.stdout.write('FAIL\n')
            for line in diff_txt.splitlines(True):
                if '/tmp/' not in line:
                    sys.stdout.write(line)
            sys.stdout.write('\n')
        else:
            sys.stdout.write('ok')
        sys.stdout.write('\n')
    except IOError:
        sys.stderr.write('Error: Could not open files (%s)\n' % (src_filename))
        return False
        #sys.exit(2)
    except KeyboardInterrupt:
        print "\n[interrupt]"
    return True

def test_xml(src_filename, param, xmlout='simple'):
    """
    Compare the xml output against a known good xml document
    """
    global logger
    try:
        target_xml = os.path.splitext(src_filename)[0] + '.xml'
        fd_xml = tempfile.NamedTemporaryFile()
        for xmlout in ('simple', 'idtag', 'idtagqual'):
            base_xml = os.path.splitext(src_filename)[0] + '.xml.' + xmlout
            if not os.path.isfile(base_xml):
                #logger.info('Base xml not found: %s' % (os.path.basename(base_xml)))
                break

            param.set('xmlout', xmlout)
            result = pyx12.x12n_document.x12n_document(param, src_filename, None, None, fd_xml)
            if not result:
                break

            fd_xml.seek(0)
            target_xml = fd_xml.name
            fd_new = tempfile.NamedTemporaryFile()
            for line in fd_xml.readlines():
                #if line[:3] not in ('ISA', 'GS*', 'ST*', 'SE*', 'GE*', 'IEA'):
                fd_new.write(line)
            #fd_new.seek(0)
            #sys.stdout.write(fd_new.read())
            fd_new.seek(0)
            
            fd_base = open(base_xml, 'r')
            fd_orig = tempfile.NamedTemporaryFile()
            for line in fd_base.readlines():
                #if line[:3] not in ('ISA', 'GS*', 'ST*', 'SE*', 'GE*', 'IEA'):
                fd_orig.write(line)
            fd_orig.write(fd_base.read())
            #fd_orig.seek(0)
            #sys.stdout.write(fd_orig.read())
            fd_orig.seek(0)

            diff_txt = diff(fd_orig.name, fd_new.name)
            sys.stdout.write('%s ... ' % (os.path.basename(src_filename)))
            if diff_txt:
                sys.stdout.write('FAIL\n')
                for line in diff_txt.splitlines(True):
                    if '/tmp/' not in line:
                        sys.stdout.write(line)
                sys.stdout.write('\n')
            else:
                sys.stdout.write('ok')
            sys.stdout.write('\n')
    except IOError:
        sys.stderr.write('Error: Could not open files (%s)\n' % (src_filename))
        return False
    except KeyboardInterrupt:
        print "\n[interrupt]"
    return True

def main():
    """
    Set up environment for processing
    """
    global logger
    param = pyx12.params.params('pyx12.conf.xml')
    logger = logging.getLogger('pyx12')
    logger.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    fd_src = None
    fd_997 = None

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
                    test_997(src_filename, param)
                    test_xml(src_filename, param)
                except KeyboardInterrupt:
                    print "\n[interrupt]"
                except IOError:
                    sys.stderr.write('Unknown Error: Could not test file (%s)\n' % (name))
                    continue

    return True

if __name__ == '__main__':
    sys.exit(not main())
