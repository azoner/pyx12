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


  <xsl:template match="/">
	<html>
	<head>
	<title><xsl:value-of select="/map/transaction/name"/></title>
	<link rel="stylesheet" type="text/css" href="seg.css" title="stylebasic"/>
	</head>
	<body>
	<xsl:apply-templates/>
	</body>
	</html>
  </xsl:template>


  <xsl:output method="html"/>

  <xsl:template match="/map/transaction1">
	<h2><xsl:value-of select="name"/></h2>
        <table>
	<xsl:apply-templates/>
	</table>
  </xsl:template>

    <xsl:template match="loop1">
    	<tr><td colspan="4">
	<table>
	<tr class="loop">
	<td colspan="2"></td>
        <td><strong><xsl:value-of select="id"/> - <xsl:value-of select="name"/></strong></td>
	<td colspan="2"></td>
        <td><xsl:value-of select="count"/></td>
	</tr>
	<xsl:apply-templates/>
	</table>
	</td></tr>
    </xsl:template>


    <xsl:template match="segment">
	<div class="segment">
        <xsl:value-of select="id"/>-
        <xsl:value-of select="name"/>
	</div>
	<table>
	<xsl:apply-templates/>
	</table>
	<p></p>
    </xsl:template>

    <xsl:template match="element">
	<tr class="element">
        <td><xsl:value-of select="usage"/></td>
        <td><xsl:value-of select="refdes"/></td>
        <td><xsl:value-of select="data_ele"/></td>
        <td style="width: 30%"><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="req_des"/></td>
        <td><xsl:value-of select="data_type"/><xsl:text> </xsl:text><xsl:value-of select="format"/></td>
        <td><xsl:value-of select="min_len"/>/<xsl:value-of select="max_len"/></td>
	</tr>
	<!-- <xsl:apply-templates select="valid_codes"/> -->
	<xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="composite">
	<tr class="composite">
        <td><xsl:value-of select="usage"/></td>
        <td><xsl:value-of select="refdes"/></td>
        <td><xsl:value-of select="data_ele"/></td>
        <td><xsl:value-of select="name"/></td>
        <td colspan="3"><xsl:value-of select="req_des"/></td>
	</tr>
	<xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="valid_codes1">
        <xsl:for-each select="code">
	<tr class="codes">
	<td colspan="4"></td>
	    <td><xsl:value-of select="."/></td>
	<td colspan="2"></td>
	</tr>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="valid_codes">
	<tr>
	<td colspan="3"></td>
	<td class="code">
	<xsl:apply-templates select="@external"/>
        <xsl:for-each select="code">
	    <xsl:value-of select="."/><xsl:text> </xsl:text> 
        </xsl:for-each>
	</td>
	<td colspan="3"></td>
	</tr>
    </xsl:template>

    <xsl:template match="@external">
	<xsl:text>External Source: </xsl:text><xsl:value-of select="."/><xsl:text> </xsl:text>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
