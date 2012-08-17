# Pyx12

Pyx12 is a HIPAA X12 document validator and converter.  It parses an ANSI X12N data file and validates it against a representation of the Implementation Guidelines for a HIPAA transaction.  By default, it creates a 997 response for 4010 and a 999 response for 5010. It can create an html representation of the X12 document or can translate to and from an XML representation of the data file. 

The Pyx12 project home is <http://sourceforge.net/projects/pyx12/>

# Install

## Prerequisites

Get setuptools <http://pypi.python.org/pypi/setuptools/>

Get pip <http://www.pip-installer.org/en/latest/installing.html>

## Install system-wide

    pip install pyx12

## Install in a virtual environment

    virtualenv my_venv
    pip -E my_venv install pyx12

# Licensing

Pyx12 has a BSD license. The full license text is included with the source code for the package. 
