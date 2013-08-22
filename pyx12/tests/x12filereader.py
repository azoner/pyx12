#!/usr/bin/env python

import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
import os
import os.path
import logging
import logging.handlers
#import tempfile
import pprint
import json
from collections import OrderedDict

import pyx12.error_handler
import pyx12.x12file
import pyx12.rawx12file
import pyx12.x12n_fastparse
import pyx12.x12n_document
import pyx12.params


def read_x12(filename):
    with open(filename) as fd:
        src = pyx12.x12file.X12Reader(fd)
        for seg in src:
            pass
            #x = seg.seg_id


def read_rawx12(filename):
    with open(filename) as fd:
        src = pyx12.rawx12file.RawX12File(fd)
        for seg in src:
            #print seg
            pass


def read_fastx12(filename):
    pp = pprint.PrettyPrinter(indent=4)
    param = pyx12.params.params('../../test/pyx12.conf.xml')
    with open(filename) as fd:
        hist = pyx12.x12n_fastparse.x12n_fastparser(param, fd)
        res2 = {}
        for k, v in hist.iteritems():
            k1 = v['start_path']
            v1 = {'segid': v['segid'], 'count': v['count'], 'newpath': v['newpath']}
            if k1 in hist:
                res2[k1].append(v1)
            else:
                res2[k1] = [v1]
        #res = [{'segid': v['segid'], 'start_path': v['start_path'], 'count': v['count'], 'newpath': v['newpath']} for k, v in hist.iteritems()]
        #res = [{'segid': v['segid'], 'start_path': v['start_path'], 'count': v['count'], 'newpath': v['newpath']} for k, v in hist.iteritems()]
        s = json.dumps(res2, indent=2)
        print s
        #pp.pprint(res)


def read_x12n(filename):
    param = pyx12.params.params('../../test/pyx12.conf.xml')
    with open(filename) as fd:
        hist = pyx12.x12n_document.x12n_document(param, fd, None, None)
        res2 = OrderedDict()
        for k in sorted(hist.keys()):
            v = hist[k]
            k1 = v['start_path']
            v1 = {'segid': v['segid'], 'f': 'seg', 'newpath': v['newpath']}
            if k1 in hist:
                res2[k1].append(v1)
            else:
                res2[k1] = [v1]
        s = json.dumps({'Maps': res2}, indent=2)
        open("834.used.json", 'w').write(s)


def main():
    """Script main program."""
    import argparse
    parser = argparse.ArgumentParser(description='Test line parser')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--background', '-b', action='store_true')
    parser.add_argument('--test', '-t', action='store_true')
    #parser.add_argument('--version', action='version', version='{prog} {version}'.format(prog=parser.prog, version=__version__))
    parser.add_argument('--profile', action='store_true', help='Profile the code with plop')
    parser.add_argument('input_files', nargs='*')
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s')

    stderr_hdlr = logging.StreamHandler()
    stderr_hdlr.setFormatter(formatter)
    logger.addHandler(stderr_hdlr)

    if args.debug or args.verbose > 0:
        logger.setLevel(logging.DEBUG)

    if len(args.input_files) > 0:
        for file1 in args.input_files:
            #read_rawx12(file1)
            #read_x12(file1)
            #read_fastx12(file1)
            read_x12n(file1)


if __name__ == '__main__':
    sys.exit(not main())
