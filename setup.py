from distutils import core
kw = {  
    'name': "pyx12",
    'version': "1.0.1b1",
    'description': "A X12 validator and converter",
    'author': "John Holland",
    'author_email': "jholland@kazoocmh.org",
    'url': "http://www.sourceforge.net/pyx12/",
    'packages': ['pyx12'],
    'data_files': [
        ('share/pyx12/map', ['map/270.4010.X092.A1.xml']),
        ('share/pyx12/map', ['map/270.4010.X092.xml']),
        ('share/pyx12/map', ['map/271.4010.X092.A1.xml']),
        ('share/pyx12/map', ['map/271.4010.X092.xml']),
        ('share/pyx12/map', ['map/276.4010.X093.A1.xml']),
        ('share/pyx12/map', ['map/276.4010.X093.xml']),
        ('share/pyx12/map', ['map/277.4010.X093.A1.xml']),
        ('share/pyx12/map', ['map/277.4010.X093.xml']),
        ('share/pyx12/map', ['map/278.4010.X094.27.A1.xml']),
        ('share/pyx12/map', ['map/278.4010.X094.27.xml']),
        ('share/pyx12/map', ['map/278.4010.X094.A1.xml']),
        ('share/pyx12/map', ['map/278.4010.X094.xml']),
        ('share/pyx12/map', ['map/820.4010.X061.A1.xml']),
        ('share/pyx12/map', ['map/820.4010.X061.xml']),
        ('share/pyx12/map', ['map/834.4010.X095.A1.xml']),
        ('share/pyx12/map', ['map/835.4010.X091.A1.xml']),
        ('share/pyx12/map', ['map/835.4010.X091.xml']),
        ('share/pyx12/map', ['map/837.4010.X096.A1.xml']),
        ('share/pyx12/map', ['map/837.4010.X096.xml']),
        ('share/pyx12/map', ['map/837.4010.X097.A1.xml']),
        ('share/pyx12/map', ['map/837.4010.X097.xml']),
        ('share/pyx12/map', ['map/837.4010.X098.A1.xml']),
        ('share/pyx12/map', ['map/837.4010.X098.xml']),
        ('share/pyx12/map', ['map/841.4010.XXXC.xml']),
        ('share/pyx12/map', ['map/997.4010.xml']),
        ('share/pyx12/map', ['map/README']),
        ('share/pyx12/map', ['map/codes.xml']),
        ('share/pyx12/map', ['map/codes.xsd']),
        ('share/pyx12/map', ['map/comp_test.xml']),
        ('share/pyx12/map', ['map/find_composites.xsl']),
        ('share/pyx12/map', ['map/map.997.4010.xml']),
        ('share/pyx12/map', ['map/map.xsd']),
        ('share/pyx12/map', ['map/maps.xml']),
        ('share/pyx12/map', ['map/test.xml']),
        ('share/pyx12/map', ['map/x12.control.00401.xml'])
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

