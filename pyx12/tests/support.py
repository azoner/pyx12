#    $Id$

import sys
from os.path import dirname, abspath, join, isdir, isfile
import pyx12.params 

def getMapPath():
    """
    First, try relative path
    Then look in standard installation location
    """
    base_dir = dirname(dirname(abspath(sys.argv[0])))
    map_path = join(base_dir, 'map')
    if isdir(map_path):
        return map_path
    else:
        params = pyx12.params.params()
        map_path = params.get('map_path')
        return map_path
