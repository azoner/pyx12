pyx12-1.1.0 has been released

What's New:
===========
    Corrected a number of validation bugs.
    
    Added many unit and functional tests.

    xmlx12 - translate an XML document created with the x12_simple conversion 
    back to an X12 document:
    x12xml -Xsimple test.txt | xslt test.xsl | xmlx12 > output.txt

    x12norm - normalize an X12 document.  Create/strip end of line characters.

    Refactor interfaces.

What is Pyx12?
==============
    Pyx12 is a HIPAA X12 document validator and converter.  It parses an ANSI
    X12N data file and validates it against a map that represents the
    implementation Guidelines.  By default, it creates a 997 response and can
    create an html representation of the X12 document.  It can also translate
    to an XML representation of the data file. 

Where can I get it?
===================
    Pyx12 is available at http://sourceforge.net/projects/pyx12/
