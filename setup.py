#from distutils import core
from distutils import core
from distutils.file_util import copy_file
from distutils.dir_util import mkpath
import os
import sys

import pyx12
import pyx12.map_if
import pyx12.params

map_dir = 'share/pyx12/map'
MAP_FILES = ['map/%s' % (file1) for file1 in 
    filter(lambda x: os.path.splitext(x)[1] == '.xml', os.listdir('map'))]
mkpath('build/bin')
SCRIPTS = ('x12_build_pkl.py', 'x12html.py', 'x12info.py', 'x12valid.py', 
    'x12norm.py', 'x12sql.py', 'x12xml.py', 'xmlx12.py')
for filename in SCRIPTS:
    if sys.platform == 'win32':
        target_script = filename
    else:
        target_script = os.path.splitext(filename)[0]
    copy_file(os.path.join('bin', filename), 
        os.path.join('build/bin', target_script))
test_dir = 'share/pyx12/test'
TEST_FILES = ['test/%s' % (file1) for file1 in 
    filter(lambda x: os.path.splitext(x)[1] in ('.py', '.xml'),
    os.listdir('test'))]
TEST_DATA = ['test/files/%s' % (file1) for file1 in 
    filter(lambda x: os.path.splitext(x)[1] 
        in ('.base', '.txt', '.idtag', '.idtagqual', '.simple', '.xsl'),
    os.listdir('test/files'))]
    
kw = {  
    'name': "pyx12",
    'version': pyx12.__version__,
    'description': pyx12.__doc__,
    'long_description': pyx12.__doc__,
    'license': 'BSD',
    'description': "An X12 validator and converter",
    'author': "John Holland",
    'author_email': "jholland@kazoocmh.org",
    'url': "http://pyx12.sourceforge.net/",
    'platforms': 'All',
    'packages': ['pyx12', 'pyx12.tests'],
    'scripts': ['build/bin/%s' % (script) for script in SCRIPTS],
    'data_files': [
        (map_dir, MAP_FILES),
        (map_dir, ['map/README', 'map/codes.xml', 'map/codes.xsd',
            'map/comp_test.xml', 'map/map.xsd', 'map/maps.xml', 
            'map/x12simple.dtd', 'map/dataele.xml']),
        ('share/doc/pyx12', ['README.txt', 'LICENSE.txt',
            'CHANGELOG.txt', 'INSTALL.txt']),
        (test_dir, TEST_FILES),
        (test_dir+'/files', TEST_DATA)
    ],
      #package_dir = {'': ''},
}

if sys.platform == 'win32':
    # Update registry
    kw['data_files'].append(('share/pyx12', ['bin/pyx12.conf.xml.sample']))
    kw['data_files'].append(('etc', ['bin/pyx12.conf.xml.sample']))
else:
    kw['data_files'].append(('share/pyx12', ['bin/pyx12.conf.xml.sample']))
    kw['data_files'].append(('etc', ['bin/pyx12.conf.xml.sample']))

if (hasattr(core, 'setup_keywords') and
    'classifiers' in core.setup_keywords):
    kw['classifiers'] = \
        ['Topic :: Communications, Office/Business',
         'Environment :: Console (Text Based)',
         'Intended Audience :: Developers, Other Audience',
         ' License :: OSI Approved :: BSD License'],

core.setup(**kw)
