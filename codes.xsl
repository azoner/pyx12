<?xml version="1.0"?>
<!-- 
    $Id$
    This file is part of the pyX12 project.

    Copyright (c) 2001, 2002 Kalamazoo Community Mental Health Services,
		John Holland <jholland@kazoocmh.org> <john@zoner.org>

    All rights reserved.

	Redistribution and use in source and binary forms, with or without modification, 
	are permitted provided that the following conditions are met:

	1. Redistributions of source code must retain the above copyright notice, this list 
	   of conditions and the following disclaimer. 
	
	2. Redistributions in binary form must reproduce the above copyright notice, this 
	   list of conditions and the following disclaimer in the documentation and/or other 
	   materials provided with the distribution. 
	
	3. The name of the author may not be used to endorse or promote products derived 
	   from this software without specific prior written permission. 

	THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
	WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
	MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
	EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
	EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
	OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
	THE POSSIBILITY OF SUCH DAMAGE.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html"/>

  <xsl:template match="/">
	<html>
	<head>
	<title>Codes</title>
	<link rel="stylesheet" type="text/css" href="seg.css" title="stylebasic"/>
	</head>
	<body>
	<xsl:apply-templates/>
	</body>
	</html>
  </xsl:template>

    <xsl:template match="codeset">
        <a name="{id}"></a>
	<table>
	<tr class="element">
        <td><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="data_ele"/></td>
	</tr>
	<xsl:apply-templates/>
	</table>
	<p></p>
    </xsl:template>

    <xsl:template match="valid_codes">
	<tr>
	<td colspan="1"></td>
	<td colspan="2" class="code">
        <xsl:for-each select="code">
	    <xsl:value-of select="."/><xsl:text> </xsl:text> 
        </xsl:for-each>
	</td>
	<td colspan="3"></td>
	</tr>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
