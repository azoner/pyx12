#! /usr/bin/env python

import os.path
import sys
from os.path import abspath, join, dirname, isdir, isfile

# Intrapackage imports
libpath = abspath(join(dirname(__file__), '../..'))
if isdir(libpath):
    sys.path.insert(0, libpath)

import pyx12.error_handler
import pyx12.map_if
from pyx12.params import params
import pyx12.segment


def donode(node, mylist):
    print node.get_path()
    mylist.append(node.get_path())
    #print(node.id)
    for ord1 in sorted(node.pos_map):
        for child in node.pos_map[ord1]:
            if child.is_loop():  # or child.is_segment():
                donode(child, mylist)

def iter2(node):
    yield node.get_path()
    #print(node.id)
    for ord1 in sorted(node.pos_map):
        for child in node.pos_map[ord1]:
            if child.is_loop():
                for n in iter2(child):
                    yield n
            elif child.is_segment():
                yield child.get_path()

param = params()
#param.set('map_path', os.path.expanduser('~/src/pyx12/map/'))
#filen = '834.5010.X220.A1.xml'
filen = sys.argv[1]
map = pyx12.map_if.load_map_file(filen, param)
#node = map.getnodebypath('/ST_LOOP')
#mylist = []
#donode(map, mylist)
mylist = list([x for x in iter2(map)])

print(mylist)
import json
with file(filen+'.json','w') as fp:
    json.dump(mylist, fp, indent=4)
#map.debug_get_looppaths()
