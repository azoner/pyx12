pyx12-1.2.0 has been released

What's New:
===========
    Created DTD for the simple XML output form. Changed URL.

    Removed generation of DTD line for idtag and idtagqual XML output forms.
    
    Added a new XML output form: idtagqual.  This form appends the ID value to
    non-unique segment IDs
        
    Added draft map for Unsolicited 277: 277U.4010.X070.xml

    Base map_if segment children on dictionary - faster lookups

    Corrected validation bugs.
    
    Added more unit and functional tests.

    Altered segment interface.
    
    See CHANGELOG.txt for all changes.

What is Pyx12?
==============
    Pyx12 is a HIPAA X12 document validator and converter.  It parses an ANSI
    X12N data file and validates it against a representation of the
    Implementation Guidelines for a HIPAA transaction.  By default, it creates
    a 997 response. It can create an html representation of the X12 document
    or can translate to and from an XML representation of the data file. 

Where can I get it?
===================
    Pyx12 is available at http://sourceforge.net/projects/pyx12/
