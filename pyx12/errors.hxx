/*
    $Id$
    This file is part of the pyX12 project.

    Copyright (c) 2001-2004 Kalamazoo Community Mental Health Services,
               John Holland <jholland@kazoocmh.org> <john@zoner.org>

    All rights reserved.

       Redistribution and use in source and binary forms, with or without
       modification, are permitted provided that the following conditions are
       met:

       1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer. 
       
       2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution. 
       
       3. The name of the author may not be used to endorse or promote
       products derived from this software without specific prior written
       permission. 

       THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
       IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
       WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
       DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
       INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
       (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
       SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
       HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
       STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
       IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
       POSSIBILITY OF SUCH DAMAGE.
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
