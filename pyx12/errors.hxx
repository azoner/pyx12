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
#include <exception>

namespace Pyx12 {
    /* Class for XML Reader errors */
    class XML_Reader_Error : std::exception {
    public:
        XML_Reader_Error(whatString) {};
    };

    /* Base class for X12N format errors*/
    class x12Error {
    public:
        x12Error();
    };

    /* Errors in the GS or GE segments */
    class GSError: public x12Error {
    public:
        GSError();
    };

    /* Base class for translation engine errors */
    class EngineError {
    public:
        EngineError(std::string err_str_);
    private:
        std::string err_str;
    };

    /* Iterator is out of bounds*/
    class IterOutOfBounds {
    public:
        IterOutOfBounds();
    };

    /* Iterator is Complete */
    class IterDone {
    public:
        IterDone();
    };
}            
