from distutils import core

map_dir = 'share/pyx12/1map'
kw = {  
    'name': "pyx12",
    'version': pyx12.x12n_document.__version__,
    'description': pyx12.x12n_document.__doc__,
    #'description': "A X12 validator and converter",
    'author': "John Holland",
    'author_email': "jholland@kazoocmh.org",
    'url': "http://www.sourceforge.net/pyx12/",
    'packages': ['pyx12'],
    'scripts' = [ "bin/x12lint.py"],
    'data_files': [
        (map_dir, ['map/270.4010.X092.A1.xml']),
        (map_dir, ['map/270.4010.X092.xml']),
        (map_dir, ['map/271.4010.X092.A1.xml']),
        (map_dir, ['map/271.4010.X092.xml']),
        (map_dir, ['map/276.4010.X093.A1.xml']),
        (map_dir, ['map/276.4010.X093.xml']),
        (map_dir, ['map/277.4010.X093.A1.xml']),
        (map_dir, ['map/277.4010.X093.xml']),
        (map_dir, ['map/278.4010.X094.27.A1.xml']),
        (map_dir, ['map/278.4010.X094.27.xml']),
        (map_dir, ['map/278.4010.X094.A1.xml']),
        (map_dir, ['map/278.4010.X094.xml']),
        (map_dir, ['map/820.4010.X061.A1.xml']),
        (map_dir, ['map/820.4010.X061.xml']),
        (map_dir, ['map/834.4010.X095.A1.xml']),
        (map_dir, ['map/835.4010.X091.A1.xml']),
        (map_dir, ['map/835.4010.X091.xml']),
        (map_dir, ['map/837.4010.X096.A1.xml']),
        (map_dir, ['map/837.4010.X096.xml']),
        (map_dir, ['map/837.4010.X097.A1.xml']),
        (map_dir, ['map/837.4010.X097.xml']),
        (map_dir, ['map/837.4010.X098.A1.xml']),
        (map_dir, ['map/837.4010.X098.xml']),
        (map_dir, ['map/841.4010.XXXC.xml']),
        (map_dir, ['map/997.4010.xml']),
        (map_dir, ['map/README']),
        (map_dir, ['map/codes.xml']),
        (map_dir, ['map/codes.xsd']),
        (map_dir, ['map/comp_test.xml']),
        (map_dir, ['map/find_composites.xsl']),
        (map_dir, ['map/map.997.4010.xml']),
        (map_dir, ['map/map.xsd']),
        (map_dir, ['map/maps.xml']),
        (map_dir, ['map/test.xml']),
        (map_dir, ['map/x12.control.00401.xml'])
   ],
      #package_dir = {'': ''},
      }

if (hasattr(core, 'setup_keywords') and
    'classifiers' in core.setup_keywords):
    kw['classifiers'] = \
        ['Topic :: Communications, Office/Business',
         'Environment :: Console (Text Based)',
         'Intended Audience :: Developers, Other Audience',
         ' License: BSD License'],

core.setup(**kw)

