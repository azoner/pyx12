#    $Id$
#    This file is part of the pyX12 project.
#
#    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
#		John Holland <jholland@kazoocmh.org> <john@zoner.org>
#
#    All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification, 
#	are permitted provided that the following conditions are met:
#
#	1. Redistributions of source code must retain the above copyright notice, this list 
#	   of conditions and the following disclaimer. 
#	
#	2. Redistributions in binary form must reproduce the above copyright notice, this 
#	   list of conditions and the following disclaimer in the documentation and/or other 
#	   materials provided with the distribution. 
#	
#	3. The name of the author may not be used to endorse or promote products derived 
#	   from this software without specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
#	WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#	MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
#	EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#	EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
#	OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
#	THE POSSIBILITY OF SUCH DAMAGE.

"""pyx12 package exception classes.
"""

class XML_Reader_Error(Exception):
    """Class for XML Reader errors."""

class x12Error(Exception):
    """Base class for X12N format errors."""

class ISAError(x12Error):
    """Errors in the ISA or IEA segements."""

class GSError(x12Error):
    """Errors in the GS or GE segements."""

class STError(x12Error):
    """Errors in the ST or SE segements."""

class WEDIError(Exception):
    """Base class for WEDI errors in this module."""

class WEDI1Error(WEDIError): pass
class WEDI2Error(WEDIError): pass
class WEDI3Error(WEDIError): pass
class WEDI4Error(WEDIError): pass
class WEDI5Error(WEDIError): pass
class WEDI6Error(WEDIError): pass

class EngineError(Exception): 
    """Base class for translation engine errors."""
class HL_Loop_Pop(EngineError):
    """Pop a HL level"""
