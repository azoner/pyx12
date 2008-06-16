#from distutils import core
from distutils import core
from distutils.file_util import copy_file
from distutils.dir_util import mkpath
import os
from os.path import join, splitext
import sys

import pyx12
import pyx12.map_if
import pyx12.params

map_dir = 'share/pyx12/map'
MAP_FILES = ['map/%s' % (file1) for file1 in 
    filter(lambda x: splitext(x)[1] == '.xml', os.listdir('map'))]
mkpath('build/bin')
SCRIPTS = ('x12_build_pkl.py', 'x12html.py', 'x12info.py', 'x12valid.py', 
    'x12norm.py', 'x12sql.py', 'x12xml.py', 'xmlx12.py')
if sys.platform == 'win32':
    for filename in SCRIPTS:
        copy_file(join('bin', filename), 
            join('build/bin', filename))
else:
    for filename in SCRIPTS:
        target_script = splitext(filename)[0]
        copy_file(join('bin', filename), 
            join('build/bin', target_script))
    SCRIPTS = [splitext(filename)[0] for filename in SCRIPTS]
test_dir = 'share/pyx12/test'
TEST_FILES = ['test/%s' % (file1) for file1 in 
    filter(lambda x: splitext(x)[1] in ('.py', '.xml'),
    os.listdir('test'))]
TEST_DATA = ['test/files/%s' % (file1) for file1 in 
    filter(lambda x: splitext(x)[1] 
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
    'download_url': "https://sourceforge.net/project/platformdownload.php?group_id=40379",
    'platforms': 'All',
    'packages': ['pyx12', 'pyx12.tests'],
    'scripts': ['build/bin/%s' % (script) for script in SCRIPTS],
    'data_files': [
        (map_dir, MAP_FILES),
        (map_dir, ['map/README', 'map/codes.xml', 'map/codes.xsd',
            'map/comp_test.xml', 'map/map.xsd', 'map/maps.xml', 
            'map/x12simple.dtd', 'map/dataele.xml', 'map/dataele.xsd']),
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
        [
         'Development Status :: 5 - Production/Stable',
         'Environment :: Console',
         'Intended Audience :: Healthcare Industry',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: BSD License',
         'Programming Language :: Python',
         'Topic :: Office/Business',
         'Topic :: Software Development :: Libraries :: Python Modules',
         ]

core.setup(**kw)
