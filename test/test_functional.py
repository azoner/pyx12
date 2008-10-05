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
import sys, string
import logging
from types import *
#import pdb
import tempfile
#import difflib
import subprocess
import StringIO

# Intrapackage imports
import pyx12
import pyx12.x12n_document
import pyx12.params
import pyx12.xmlx12_simple
import pyx12.x12file

logger = None

class TesterError(Exception):
    """Base class for tester engine errors."""

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

def isX12Diff(fd1, fd2):
    """
    Just want to know if the important bits of the 997 are different
    """
    src1 = pyx12.x12file.X12Reader(fd1)
    src2 = pyx12.x12file.X12Reader(fd2)
    done1 = False
    done2 = False
    while True:
        try:
            seg1 = src1.next()
        except StopIteration:
            done1 = True
        try:
            seg2 = src2.next()
        except StopIteration:
            done2 = True
        id1 = seg1.get_seg_id()
        id2 = seg2.get_seg_id()
        if seg1.format() != seg2.format() \
                and (seg1.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA') \
                or seg2.get_seg_id() not in ('ISA', 'GS', 'ST', 'SE', 'GE', 'IEA')):
            return True
        if done1 and done2:
            return False
    return False
    
def get997BaseFilename(src_filename):
    if os.path.splitext(src_filename)[1] == '.997':
        filename = src_filename + '.997.base'
    else:
        filename = os.path.splitext(src_filename)[0] + '.997.base'
    if not os.path.isfile(filename):
        raise TesterError, 'Base 997 not found: %s' % (os.path.basename(filename))
    return filename

def getXSLTFilenames(src_filename):
    filename = os.path.splitext(src_filename)[0] + '.xsl'
    if os.path.isfile(filename):
        return [filename]
    else:
        return []

def test_997(src_filename, param):
    """
    Compare the 997 output against a known 997
    """
    global logger
    logger.debug(src_filename)
    try:
        base_997 = get997BaseFilename(src_filename)
        fd_997 = StringIO.StringIO()
        xslt_files = getXSLTFilenames(src_filename)
        pyx12.x12n_document.x12n_document(param, src_filename, fd_997, None, None, xslt_files)
        fd_997.seek(0)

        fd_base = open(base_997, 'r')
        #diff_txt = diff(fd_orig.name, fd_new.name)
        sys.stdout.write('997: %s ... ' % (os.path.basename(src_filename)))
        #if diff_txt:
        if isX12Diff(fd_base, fd_997):
            sys.stdout.write('FAIL')
            #for line in diff_txt.splitlines(True):
            #    if '/tmp/' not in line:
            #        sys.stdout.write(line)
            #sys.stdout.write('\n')
        else:
            sys.stdout.write('ok')
        sys.stdout.write('\n')
    except IOError:
        sys.stderr.write('Error: Could not open files (%s)\n' % (src_filename))
        return False
        #sys.exit(2)
    except KeyboardInterrupt:
        print "\n[interrupt]"
    except:
        #logger.info('Base xml not found: %s' % (os.path.basename(base_xml)))
        return False
    return True

def test_xml(src_filename, param, xmlout='simple'):
    """
    Compare the xml output against a known good xml document
    """
    global logger
    param.set('idtag_dtd', None)
    param.set('idtagqual_dtd', None)
    try:
        for xmlout in ('simple', 'idtag', 'idtagqual'):
            fd_xml = tempfile.NamedTemporaryFile()
            base_xml = os.path.splitext(src_filename)[0] + '.xml.' + xmlout
            if not os.path.isfile(base_xml):
                #logger.info('Base xml not found: %s' % (os.path.basename(base_xml)))
                break

            param.set('xmlout', xmlout)
            result = pyx12.x12n_document.x12n_document(param, src_filename, None, None, fd_xml)
            if not result:
                break

            fd_xml.seek(0)
            fd_base = open(base_xml, 'r')

            diff_txt = diff(fd_base.name, fd_xml.name)
            sys.stdout.write('xml %s: %s ... ' % (xmlout, os.path.basename(src_filename)))
            if diff_txt:
                sys.stdout.write('FAIL\n')
                for line in diff_txt.splitlines(True):
                    if '/tmp/' not in line:
                        sys.stdout.write(line)
                sys.stdout.write('\n')
            else:
                sys.stdout.write('ok\n')

            # Back to X12
            if xmlout in ('simple'):
                fd_xml.seek(0)
                fd_x12 = tempfile.NamedTemporaryFile()
                res = pyx12.xmlx12_simple.convert(fd_xml.name, fd_x12)
                fd_xml.seek(0)
                fd_x12.seek(0)
                diff_txt = diff(src_filename, fd_x12.name)
                sys.stdout.write('xmlx12 %s: %s ... ' % (xmlout, os.path.basename(src_filename)))
                if diff_txt:
                    sys.stdout.write('FAIL\n')
                    for line in diff_txt.splitlines(True):
                        if '/tmp/' not in line:
                            sys.stdout.write(line)
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write('ok\n')
            del fd_base
            del fd_xml
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
    map_path = os.path.join(string.join(os.path.abspath(
        sys.argv[0]).split('/')[:-2], '/'), 'map')
    if os.path.isdir(map_path):
        param.set('map_path', map_path)
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

    if not debug:
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass

    dir1 = os.path.abspath('./files')
    if len(sys.argv) > 1:
        names = sys.argv[1:]
    else:
        try:
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
                    if sys.platform != 'win32':
                        test_xml(src_filename, param)
                except KeyboardInterrupt:
                    print "\n[interrupt]"
                except IOError:
                    sys.stderr.write('Unknown Error: Could not test file (%s)\n' % (name))
                    continue

    return True

if __name__ == '__main__':
    sys.exit(not main())
