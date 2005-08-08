#! /usr/bin/env /usr/local/bin/python

import sys
import os.path
import string

def main():
    manifest = map(string.rstrip, open('MANIFEST').readlines())
    fd_out =  sys.stdout
    site = '%%PYTHON_SITELIBDIR%%/'
    ex = 'share/examples/pyx12/'
    doc = 'share/doc/pyx12/'
    share = 'share/pyx12/'
    [(fd_out.write(x[:-3]+'\n')) for x in filter(lambda x: x[:3] == 'bin' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x+'\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyc\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyo\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    fd_out.write('etc/pyx12.conf.xml.sample\n')
    fd_out.write('share/examples/pyx12/pyx12.conf.xml.sample\n')
    [(fd_out.write(ex+x+'\n')) for x in filter(lambda x: x[:4] == 'test' and x[-3:] == '.py', manifest)]
    [(fd_out.write(ex+x+'\n')) for x in filter(lambda x: x[:10] == 'test/files' 
        and (x[-4:] == '.txt' or x[-5:] == '.base' or x[-4:] == '.txt' or x[-7:] == '.simple'
        or x[-6:] == '.idtag' or x[-10:] == '.idtagqual'), 
        manifest)]
    for x in ('CHANGELOG.txt', 'INSTALL.txt', 'LICENSE.txt', 'README.txt'):
        fd_out.write(doc+x+'\n')
    fd_out.write(doc+'view/Makefile'+'\n')
    [(fd_out.write(doc+x+'\n')) for x in filter(lambda x: x[:4] == 'view' and x[-4:] == '.xsl', manifest)]
    [(fd_out.write(doc+x+'\n')) for x in filter(lambda x: x[:4] == 'view' and x[-4:] == '.css', manifest)]
    maps = filter(lambda x: x[:3] == 'map' and x[-4:] == '.xml', manifest)
    [(fd_out.write(share+x+'\n')) for x in maps]
    [(fd_out.write(share+x[:-4]+'.pkl\n')) for x in filter(lambda x: os.path.basename(x) 
        not in ('maps.xml', 'comp_test.xml'), maps)]
    for x in ('map/README', 'map/codes.xsd', 'map/map.xsd', 'map/x12simple.dtd'):
        fd_out.write(share+x+'\n')

    for dir1 in (doc+'view', doc[:-1], share+'map', share[:-1], \
            ex+'test/files', ex+'test', ex[:-1], \
            site+'pyx12'):
        fd_out.write('@dirrm '+dir1+'\n')
   

if __name__ == '__main__':
    sys.exit(not main())
