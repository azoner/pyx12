from setuptools import setup
#from os import listdir
from os.path import join, dirname
#import sys

#map_dir = 'share/pyx12/map'
#MAP_FILES = ['map/%s' % (file1) for file1 in
#             filter(lambda x: splitext(x)[1] == '.xml', listdir('map'))]
#SCRIPTS = ('x12html.py', 'x12info.py', 'x12valid.py',
#           'x12norm.py', 'x12xml.py', 'xmlx12.py')

#data_files = [
#    (map_dir, MAP_FILES),
#    (map_dir, ['map/README', 'map/codes.xml', 'map/codes.xsd',
#               'map/comp_test.xml', 'map/map.xsd', 'map/maps.xml',
#               'map/x12simple.dtd', 'map/dataele.xml', 'map/dataele.xsd']),
#    ('share/doc/pyx12', ['README.md', 'LICENSE.txt',
#                         'CHANGELOG.txt', 'INSTALL.txt']),
#    #(test_dir, TEST_FILES)
#]
#if sys.platform == 'win32':
#    data_files.append((join('share', 'pyx12'), ['bin/pyx12.conf.xml.sample']))
#    data_files.append(('etc', ['bin/pyx12.conf.xml.sample']))
#else:
#    data_files.append((join('share', 'pyx12'), ['bin/pyx12.conf.xml.sample']))
#    data_files.append(('etc', ['bin/pyx12.conf.xml.sample']))

__version__ = ""
execfile('pyx12/version.py')
setup(
    name="pyx12",
    version=__version__,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    license='BSD',
    description="An X12 validator and converter",
    keywords='x12 hipaa healthcare edi',
    author="John Holland",
    author_email="jholland@kazoocmh.org",
    url="http://github.com/azoner/pyx12#pyx12",
    platforms='All',
    packages=['pyx12', 'pyx12.scripts'],
    #scripts=['bin/%s' % (script) for script in SCRIPTS],
    entry_points={
        'console_scripts': [
            'x12html = pyx12.scripts.x12html:main',
            'x12valid = pyx12.scripts.x12valid:main',
            'x12info = pyx12.scripts.x12info:main',
            'x12norm = pyx12.scripts.x12norm:main',
            'x12xml = pyx12.scripts.x12xml:main',
            'xmlx12 = pyx12.scripts.xmlx12:main',
        ]
    },
    package_data={'': ['*.xml', '*.md'], 'pyx12': ['*.xml']},
    #data_files=data_files,
    #include_package_data=True,
    test_suite="pyx12.tests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
