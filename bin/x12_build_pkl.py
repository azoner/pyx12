#! /usr/bin/env /usr/local/bin/python

#import getopt
import cPickle
import os.path
import sys
#from stat import ST_MTIME
#from stat import ST_SIZE

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
        '270.4010.X092.xml',
        '271.4010.X092.A1.xml',
        '271.4010.X092.xml',
        '276.4010.X093.A1.xml',
        '276.4010.X093.xml',
        '277.4010.X093.A1.xml',
        '277.4010.X093.xml',
        '278.4010.X094.27.A1.xml',
        '278.4010.X094.27.xml',
        '278.4010.X094.A1.xml',
        '278.4010.X094.xml',
        '820.4010.X061.A1.xml',
        '820.4010.X061.xml',
        '834.4010.X095.A1.xml',
        '835.4010.X091.A1.xml',
        '835.4010.X091.xml',
        '837.4010.X096.A1.xml',
        '837.4010.X096.xml',
        '837.4010.X097.A1.xml',
        '837.4010.X097.xml',
        '837.4010.X098.A1.xml',
        '837.4010.X098.xml',
        '841.4010.XXXC.xml',
        '997.4010.xml',
        'x12.control.00401.xml'
    ]

    for map_file in map_files:
        print 'Pickling %s' % (map_file)
        pickle_file = '%s.%s' % (os.path.splitext(map_file)[0], 'pkl')

        # init the map from the pickled file
        try:
            map = pyx12.map_if.map_if(map_file, param)
            cPickle.dump(map, open(os.path.join(pickle_dir, pickle_file),'w'))
        except:
            print 'Pickle failed for %s' % (map_file)

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

