#! /usr/bin/env /usr/local/bin/python

import map_if
#import getopt
import cPickle
import os.path
import sys
#from stat import ST_MTIME
#from stat import ST_SIZE

def main():
    for map_file in sys.argv[1:]:
        print 'Processing %s' % (file)
        pickle_file = '%s.%s' % (os.path.splitext(map_file)[0], 'pkl')

        # init the map from the pickled file
        map = map_if.map_if(map_file)
        cPickle.dump(map, open(pickle_file,'w'))

if __name__ == '__main__':
    sys.exit(not main())

