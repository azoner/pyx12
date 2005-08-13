<?xml version="1.0"?>
<!-- 
######################################################################
# Copyright (c) 2001-2005 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id$
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
	<tr>
	<td colspan="1"></td>
	<td colspan="2" class="code">
        <xsl:for-each select="code">
	    <xsl:value-of select="."/><xsl:text> </xsl:text> 
        </xsl:for-each>
	</td>
	<td colspan="3"></td>
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
