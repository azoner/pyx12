#! /usr/bin/env /usr/local/bin/python

#import getopt
import cPickle
import os.path
import sys
#from stat import ST_MTIME
#from stat import ST_SIZE

import pyx12.map_if
import pyx12.params

def main():
    param = pyx12.params.params()
    for map_file in sys.argv[1:]:
        print 'Processing %s' % (map_file)
        pickle_file = '%s.%s' % (os.path.splitext(map_file)[0], 'pkl')

        # init the map from the pickled file
        map = pyx12.map_if.map_if(map_file, param)
        cPickle.dump(map, open(pickle_file,'w'))

if __name__ == '__main__':
    sys.exit(not main())

