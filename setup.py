#from distutils import core
from distutils import core
from distutils.file_util import copy_file
from distutils.dir_util import mkpath
import cPickle
import os
import sys

import pyx12
import pyx12.map_if
import pyx12.params

map_dir = 'share/pyx12/map'
MAP_FILES = ['map/%s' % (file1) for file1 in 
    filter(lambda x: x[:4] == 'map' and os.path.splitext(x)[1] == '.xml',
    os.listdir('map'))]
mkpath('build/bin')
SCRIPTS = ('x12_build_pkl', 'x12html', 'x12info', 'x12valid', 
    'x12norm', 'x12sql', 'x12xml', 'xmlx12')
for filename in SCRIPTS:
    if sys.platform == 'win32':
        target_script = filename+'.py'
    else:
        target_script = filename
    copy_file(os.path.join('bin', filename+'.py'), 
        os.path.join('build/bin', target_script))
TEST_FILES = ['test/%s' % (file1) for file1 in 
    filter(lambda x: x[:4] == 'test' and os.path.splitext(x)[1] == '.py',
    os.listdir('test'))]
TEST_DATA = ['test/files/%s' % (file1) for file1 in 
    filter(lambda x: os.path.splitext(x)[1] 
        in ('.base', '.txt', '.idtag', '.idtagqual', '.simple'),
    os.listdir('test/files'))]
    
kw = {  
    'name': "pyx12",
    'version': pyx12.__version__,
    #'description': pyx12.__doc__,
    'description': "An X12 validator and converter",
    'author': "John Holland",
    'author_email': "jholland@kazoocmh.org",
    'url': "http://pyx12.sourceforge.net/",
    'packages': ['pyx12'],
    'scripts': ['build/bin/%s' % (script) for script in SCRIPTS],
    'data_files': [
        (map_dir, MAP_FILES),
        (map_dir, ['map/README', 'map/codes.xml', 'map/codes.xsd',
        'map/comp_test.xml', 'map/map.xsd', 'map/maps.xml', 
        'map/x12simple.dtd']),
        ('share/doc/pyx12', ['README.txt', 'LICENSE.txt',
        'CHANGELOG.txt', 'INSTALL.txt']),
        ('share/examples/pyx12/test', TEST_FILES),
        ('share/examples/pyx12/test/files', TEST_DATA)
    ],
      #package_dir = {'': ''},
}

if sys.platform == 'win32':
    # Update registry
    kw['data_files'].append(('share/examples/pyx12', ['bin/pyx12.conf.xml.sample']))
    kw['data_files'].append(('etc', ['bin/pyx12.conf.xml.sample']))
else:
    kw['data_files'].append(('share/examples/pyx12', ['bin/pyx12.conf.xml.sample']))
    kw['data_files'].append(('etc', ['bin/pyx12.conf.xml.sample']))

if (hasattr(core, 'setup_keywords') and
    'classifiers' in core.setup_keywords):
    kw['classifiers'] = \
        ['Topic :: Communications, Office/Business',
         'Environment :: Console (Text Based)',
         'Intended Audience :: Developers, Other Audience',
         ' License :: OSI Approved :: BSD License'],

param = pyx12.params.params()
for file in MAP_FILES:
    param.set('map_path', 'map')
    map_file = os.path.basename(file)

core.setup(**kw)
