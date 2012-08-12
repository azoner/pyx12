#! /usr/bin/env /usr/local/bin/python

import sys
from os.path import basename, splitext, join, dirname
import string

"""
Generate the plist files for the FreeBSD port
"""

def ext(filename):
    try:
        return splitext(filename)[1]
    except:
        return ''

def main():
    manfile = join(dirname(sys.argv[0]), 'MANIFEST')
    manifest = map(string.rstrip, open(manfile).readlines())
    fd_out =  sys.stdout
    site = '%%PYTHON_SITELIBDIR%%/'
    ex = '%%EXAMPLESDIR%%/'
    doc = '%%DOCSDIR%%/'
    share = '%%DATADIR%%/'
    [(fd_out.write(x[:-3]+'\n')) for x in filter(lambda x: x[:3] == 'bin' and ext(x) == '.py', manifest)]
    [(fd_out.write(site+x+'\n')) for x in filter(lambda x: x[:5] == 'pyx12' and ext(x) == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyc\n')) for x in filter(lambda x: x[:5] == 'pyx12' and ext(x) == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyo\n')) for x in filter(lambda x: x[:5] == 'pyx12' and ext(x) == '.py', manifest)]
    fd_out.write('etc/pyx12.conf.xml.sample\n')
    fd_out.write(share+'pyx12.conf.xml.sample\n')
    [(fd_out.write(share+x+'\n')) for x in filter(lambda x: x[:4] == 'test' and ext(x) in ('.py', '.xml'), manifest)]
    for x in ('CHANGELOG.txt', 'INSTALL.txt', 'LICENSE.txt', 'README.md'):
        fd_out.write(doc+x+'\n')
    maps = filter(lambda x: x[:3] == 'map' and ext(x) == '.xml', manifest)
    [(fd_out.write(share+x+'\n')) for x in maps]
    [(fd_out.write(share+x[:-4]+'.pkl\n')) for x in filter(lambda x: basename(x) 
        not in ('maps.xml', 'comp_test.xml', 'dataele.xml'), maps)]
    for x in ('map/README', 'map/codes.xsd', 'map/map.xsd', 'map/dataele.xsd', 'map/x12simple.dtd'):
        fd_out.write(share+x+'\n')
    for dir1 in (share+'map', share+'test', share[:-1], \
            doc[:-1], site+'pyx12/tests', site+'pyx12'):
        fd_out.write('@dirrm '+dir1+'\n')

if __name__ == '__main__':
    sys.exit(not main())
