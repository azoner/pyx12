/*
######################################################################
# Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

$Id$
*/

/* pyx12 package exception classes */
#include <string>

namespace Pyx12 {
    /* Class for XML Reader errors */
    class XML_Reader_Error {
    public:
        XML_Reader_Error();
    };

    /* Base class for X12N format errors*/
    class x12Error {
    public:
        x12Error();
    };

    /* Errors in the ISA or IEA segments */
    class ISAError: public x12Error {
    public:
        ISAError();
    };

    /* Errors in the GS or GE segments */
    class GSError: public x12Error {
    public:
        GSError();
    };

    /* Errors in the ST or SE segments */
    class STError: public x12Error {
    public:
        STError();
    };

    /* Base class for WEDI errors in this module*/
    class WEDIError {
    public:
        WEDIError();
    };

    class WEDI1Error: public WEDIError {
    public:
        WEDI1Error();
    };

    class WEDI2Error: public WEDIError {
    public:
        WEDI2Error();
    };

    class WEDI3Error: public WEDIError {
    public:
        WEDI3Error();
    };

    class WEDI4Error: public WEDIError {
    public:
        WEDI4Error();
    };

    class WEDI5Error: public WEDIError {
    public:
        WEDI5Error();
    };

    class WEDI6Error: public WEDIError {
    public:
        WEDI6Error();
    };

    /* Base class for translation engine errors */
    class EngineError {
    public:
        EngineError(std::string err_str_);
    private:
        std::string err_str;
    };

    /* Pop a HL level */
    class HL_Loop_Pop: public EngineError {
    public:
        HL_Loop_Pop();
    };

    /* Iterator is out of bounds*/
    class IterOutOfBounds {
    public:
        IterOutOfBounds();
    };

    /* Iterator is Complete */
    class IterDone{
    public:
        IterDone();
    };
}            
