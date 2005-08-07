#! /usr/bin/env /usr/local/bin/python

import sys
import os.path
import string

def main():
    manifest = map(string.rstrip, open('MANIFEST').readlines())
    fd_out =  sys.stdout
    site = '%%PYTHON_SITELIBDIR%%/'
    ex = 'share/examples/pyx12/'
    [(fd_out.write(x[:-3]+'\n')) for x in filter(lambda x: x[:3] == 'bin' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x+'\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyc\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    [(fd_out.write(site+x[:-3]+'.pyo\n')) for x in filter(lambda x: x[:5] == 'pyx12' and x[-3:] == '.py', manifest)]
    fd_out.write('etc/pyx12.conf.xml.sample\n')
    fd_out.write('share/examples/pyx12/pyx12.conf.xml.sample\n')
    [(fd_out.write(ex+x+'\n')) for x in filter(lambda x: x[:4] == 'test' and x[-3:] == '.py', manifest)]
    [(fd_out.write(ex+x+'\n')) for x in filter(lambda x: x[:10] == 'test/files' 
        and (x[-4:] == '.txt' or x[-5:] == '.base' or x[-4:] == '.txt' or x[-7:] == '.simple'
        or x[-6:] == '.idtag' or x[-9:] == '.idtagref'), 
        manifest)]


if __name__ == '__main__':
    sys.exit(not main())
"""
share/doc/pyx12/LICENSE.txt
share/doc/pyx12/README.txt
share/doc/pyx12/view/Makefile
share/doc/pyx12/view/codes.xsl
share/doc/pyx12/view/loop.css
share/doc/pyx12/view/loop.xsl
share/doc/pyx12/view/map_seg.xsl
share/doc/pyx12/view/map_sum.xsl
share/doc/pyx12/view/seg.css
share/doc/pyx12/view/sum.css
share/pyx12/map/270.4010.X092.A1.xml
share/pyx12/map/270.4010.X092.xml
share/pyx12/map/271.4010.X092.A1.xml
share/pyx12/map/271.4010.X092.xml
share/pyx12/map/276.4010.X093.A1.xml
share/pyx12/map/276.4010.X093.xml
share/pyx12/map/277.4010.X093.A1.xml
share/pyx12/map/277.4010.X093.xml
share/pyx12/map/278.4010.X094.27.A1.xml
share/pyx12/map/278.4010.X094.27.xml
share/pyx12/map/278.4010.X094.A1.xml
share/pyx12/map/278.4010.X094.xml
share/pyx12/map/820.4010.X061.A1.xml
share/pyx12/map/820.4010.X061.xml
share/pyx12/map/834.4010.X095.A1.xml
share/pyx12/map/835.4010.X091.A1.xml
share/pyx12/map/835.4010.X091.xml
share/pyx12/map/837.4010.X096.A1.xml
share/pyx12/map/837.4010.X096.xml
share/pyx12/map/837.4010.X097.A1.xml
share/pyx12/map/837.4010.X097.xml
share/pyx12/map/837.4010.X098.A1.xml
share/pyx12/map/837.4010.X098.xml
share/pyx12/map/841.4010.XXXC.xml
share/pyx12/map/997.4010.xml
share/pyx12/map/270.4010.X092.A1.pkl
share/pyx12/map/270.4010.X092.pkl
share/pyx12/map/271.4010.X092.A1.pkl
share/pyx12/map/271.4010.X092.pkl
share/pyx12/map/276.4010.X093.A1.pkl
share/pyx12/map/276.4010.X093.pkl
share/pyx12/map/277.4010.X093.A1.pkl
share/pyx12/map/277.4010.X093.pkl
share/pyx12/map/278.4010.X094.27.A1.pkl
share/pyx12/map/278.4010.X094.27.pkl
share/pyx12/map/278.4010.X094.A1.pkl
share/pyx12/map/278.4010.X094.pkl
share/pyx12/map/820.4010.X061.A1.pkl
share/pyx12/map/820.4010.X061.pkl
share/pyx12/map/834.4010.X095.A1.pkl
share/pyx12/map/835.4010.X091.A1.pkl
share/pyx12/map/835.4010.X091.pkl
share/pyx12/map/837.4010.X096.A1.pkl
share/pyx12/map/837.4010.X096.pkl
share/pyx12/map/837.4010.X097.A1.pkl
share/pyx12/map/837.4010.X097.pkl
share/pyx12/map/837.4010.X098.A1.pkl
share/pyx12/map/837.4010.X098.pkl
share/pyx12/map/841.4010.XXXC.pkl
share/pyx12/map/997.4010.pkl
share/pyx12/map/README
share/pyx12/map/codes.xml
share/pyx12/map/codes.pkl
share/pyx12/map/codes.xsd
share/pyx12/map/comp_test.xml
share/pyx12/map/map.xsd
share/pyx12/map/maps.xml
share/pyx12/map/x12.control.00401.xml
share/pyx12/map/x12.control.00401.pkl
@dirrm share/doc/pyx12/view
@dirrm share/doc/pyx12
@dirrm share/pyx12/map
@dirrm share/pyx12
@dirrm share/examples/pyx12/test/files
@dirrm share/examples/pyx12/test
@dirrm share/examples/pyx12
@dirrm %%PYTHON_SITELIBDIR%%/pyx12
"""
