#! /usr/bin/env /usr/local/bin/python

import map_if
#import getopt
import cPickle
import os.path
import sys
from stat import ST_MTIME
from stat import ST_SIZE


def load_map_file(map_file):
    pickle_file = '%s.%s' % (os.path.splitext(map_file)[0], 'pkl')

    #pdb.set_trace()
    # init the map from the pickled file
    if os.path.isfile(pickle_file):
        if os.stat(map_file)[ST_MTIME] >= os.stat(pickle_file)[ST_MTIME]:
            map = map_if.map_if(map_file)
            cPickle.dump(map, open(pickle_file,'w'))
        else:
            print 'Pickle file %s is up to date' % (pickle_file)
    else:
        map = map_if.map_if(map_file)
        cPickle.dump(map, open(pickle_file,'w'))

def main():
    for file in sys.argv[1:]:
        print 'Processing %s' % (file)
        load_map_file(file)

if __name__ == '__main__':
    sys.exit(not main())

