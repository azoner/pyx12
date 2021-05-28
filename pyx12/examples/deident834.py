#! /usr/bin/env python
import sys
import getopt
import os.path
import logging
import random

# Intrapackage imports
libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if os.path.isdir(libpath):
    sys.path.insert(0, libpath)

import pyx12
import pyx12.x12file
import pyx12.x12context
import pyx12.params
import pyx12.segment

from collections import namedtuple


__author__ = 'John Holland'
__version__ = '1.0'
__date__ = '2015-02-12'

"""
De-indentify 834 Enrollment file

Not production ready

"""

VERBOSE = 0

logger = logging.getLogger()
sub_idx = 0


Demographic = namedtuple('Demographic', 'primaryId, ssn, \
        medicaidId, dob, dod, firstname, lastname, middlename, street, street2, county')


class FakeDeidentify(object):
    def __init__(self):
        pass

    def getDeidentified(self, primaryId, datatree):
        demo = Demographic(primaryId, '99999999', '009999999', '19500101', \
                '', 'Joe', 'Smith', '', '123 Elm', '', '99')
        return demo


class RandomDeidentify(object):
    def __init__(self):
        self.identities = {}

    def getDeidentified(self, primaryId, datatree):
        if primaryId in self.identities:
            return self.identities[primaryId]
        demo = Demographic(
                primaryId = "{0:0>10}".format(random.randint(1000, 99999999999)),
                ssn = "{0:0>9}".format(random.randint(10000, 999999999)),
                medicaidId = "{0:0>10}".format(random.randint(1000, 99999999999)),
                dob = '19520101',
                dod = '',
                firstname = 'AA',
                lastname = 'Smith',
                middlename = '',
                street = "{0} Oak".format(random.randint(10, 9999)),
                street2 = '',
                county = '98'
        )
        self.identities[primaryId] = demo
        return demo


def deidentify_file(fd_in):
    """
    """
    param = pyx12.params.params()
    errh = pyx12.error_handler.errh_null()
    src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
    #deident = FakeDeidentify()
    deident = RandomDeidentify()

    with open('newfile.txt', 'w', encoding='ascii') as fd_out:
        wr = pyx12.x12file.X12Writer(fd_out)
        for datatree in src.iter_segments('2000'):
            if datatree.id == '2000':
                scrub2000(datatree, deident)
            for seg1 in datatree.iterate_segments():
                #wr.Write(seg1['segment'].format())
                print((seg1['segment'].format()))


def scrub2000(loop_sub, deident):
    primaryId = loop_sub.get_value('2100A/NM109')
    demo = deident.getDeidentified(primaryId, loop_sub)
    loop_sub.set_value('INS12', demo.dod)
    loop_sub.set_value('REF[0F]02', demo.primaryId)
    loop_sub.set_value('2100A/NM103', demo.lastname)
    loop_sub.set_value('2100A/NM104', demo.firstname)
    loop_sub.set_value('2100A/NM105', demo.middlename)
    loop_sub.set_value('2100A/NM109', demo.medicaidId)
    loop_sub.set_value('2100A/N301', demo.street)
    loop_sub.set_value('2100A/N302', demo.street2)
    loop_sub.set_value('2100A/N406', demo.county)
    loop_sub.set_value('2100A/DMG02', demo.dob)


def usage():
    pgm_nme = os.path.basename(sys.argv[0])
    sys.stdout.write('%s %s (%s)\n' % (pgm_nme, __version__, __date__))
    sys.stdout.write('usage: %s [options] source_file\n' % (pgm_nme))
    sys.stdout.write('\noptions:\n')
    sys.stdout.write('  -h         Help\n')
    sys.stdout.write('  -d         Debug mode\n')
    sys.stdout.write('  -o output_directory \n')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dhv')
    except getopt.error as msg:
        usage()
        return False
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    for o, a in opts:
        if o == '-h':
            usage()
            return True
        if o == '-d':
            logger.setLevel(logging.DEBUG)
        if o == '-v':
            logger.setLevel(logging.DEBUG)

    for file_in in args:
        if not os.path.isfile(file_in):
            logger.error('File %s was not found' % (file_in))
            usage()
            return False
        #file_name = os.path.basename(file_in)
        fd_in = open(file_in, 'r', encoding='ascii')
        deidentify_file(fd_in)
    return True

if __name__ == '__main__':
    sys.exit(not main())
