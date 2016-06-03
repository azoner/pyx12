from setuptools import setup

# from pyx12.version import __version__


long_description = """Pyx12 is a HIPAA X12 document validator and converter. It parses an ANSI X12N data file and
validates it against a representation of the Implementation Guidelines for a HIPAA transaction. By default, it
creates a 997 response for 4010 and a 999 response for 5010. It can create an html representation of the X12
document or can translate to and from an XML representation of the data file."""

setup(
    name="pyx12",
    version="2.3.1",
    long_description=long_description,
    license='BSD',
    description="HIPAA X12 validator, parser and converter",
    keywords='x12 hipaa healthcare edi',
    author="John Holland",
    author_email="john.holland@swmbh.org",
    url="http://github.com/azoner/pyx12",
    platforms='All',
    packages=['pyx12', 'pyx12.scripts'],
    package_data={
        '': ['*.xml', '*.md'],
        'pyx12': ['map/*.xml', 'map/*.xsd'],
    },
    #data_files=[('config', ['bin/pyx12.conf.xml.sample'])],
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
    test_suite="pyx12.test",
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
