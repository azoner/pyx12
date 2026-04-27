# Pyx12

[![Build Status](https://github.com/azoner/pyx12/actions/workflows/main.yml/badge.svg)](https://github.com/azoner/pyx12/actions/workflows/main.yml)


Pyx12 is a HIPAA X12 document validator and converter.  It parses an ANSI X12N data file and validates it against a representation of the Implementation Guidelines for a HIPAA transaction.  By default, it creates a 997 response for 4010 and a 999 response for 5010. It can create an html representation of the X12 document or can translate to and from an XML representation of the data file. 

# Usage

As a command line X12 validator

    x12valid.exe <filename>

To fix common X12 structural errors

    x12norm.exe --fix --eol <filename>

# Code Examples

    Iterate over a loop.  Alter children. Show changes
```python
    src = pyx12.x12context.X12ContextReader(param, errh, fd_in)
    for datatree in src.iter_segments('2300'):
        # do something with a 2300 claim loop
        # we have access to the 2300 loop and all its children
        for loop2400 in datatree.select('2400'):
            print(loop2400.get_value('SV101'))
            # update something
            loop2400.set_value('SV102', 'xx')
            # delete something
            if loop2400.exists('PWK'):
                loop2400.delete('PWK')
        # iterate over all the child segments
        for seg_node in datatree.iterate_segments():
            print(seg_node.format())
```

# Install

    uv pip install pyx12

# Licensing

Pyx12 uses a BSD license. The full license text is included with the source code for the package. 
