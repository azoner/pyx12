#! /usr/bin/env python

#import getopt
import cPickle
import os.path
import sys
#from stat import ST_MTIME
#from stat import ST_SIZE
import libxml2

import pyx12.codes
import pyx12.map_if
import pyx12.params

def main():
    param = pyx12.params.params()
    try:
        map_dir = sys.argv[1]
        param.set('map_path', map_dir)
    except:
        map_dir = param.get('map_path')
    try:
        pickle_dir = sys.argv[2]
    except:
        pickle_dir = map_dir
    map_files = [
        '270.4010.X092.A1.xml',
        '271.4010.X092.A1.xml',
        '276.4010.X093.A1.xml',
        '277.4010.X093.A1.xml',
        '277U.4010.X070.xml',
        '278.4010.X094.27.A1.xml',
        '278.4010.X094.A1.xml',
        '820.4010.X061.A1.xml',
        '830.4010.PS.xml',
        '834.4010.X095.A1.xml',
        '835.4010.X091.A1.xml',
        '837.4010.X096.A1.xml',
        '837.4010.X097.A1.xml',
        '837.4010.X098.A1.xml',
        '841.4010.XXXC.xml',
        '997.4010.xml',
        'x12.control.00401.xml'
    ]

    for map_file in map_files:
        print 'Pickling %s' % (map_file)
        pickle_file = '%s.%s' % (os.path.splitext(map_file)[0], 'pkl')
        map_full = os.path.join(map_dir, map_file)

        # init the map from the pickled file
        try:
            doc = libxml2.parseFile(map_full)
            reader = doc.readerWalker()
            map1 = pyx12.map_if.map_if(reader, param)
            cPickle.dump(map1, open(os.path.join(pickle_dir, pickle_file),'w'))
        except:
            print 'Pickle failed for %s' % (map_file)
            raise

    # Codes data structure
    print 'Pickling codes.xml'
    try:
        codes = pyx12.codes.ExternalCodes(map_dir, None)
        cPickle.dump(codes.codes, open(os.path.join(pickle_dir, 'codes.pkl'),'w'))
    except:
        print 'Pickle failed for codes.xml'
    return True

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    sys.exit(not main())

