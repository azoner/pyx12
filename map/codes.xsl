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
	<link rel="stylesheet" type="text/css" href="codes.css" title="stylebasic"/>
	</head>
	<body>
	<xsl:apply-templates/>
	</body>
	</html>
  </xsl:template>

    <xsl:template match="codeset">
	<table>
	<thead>
        <th>Code ID</th>
        <th>Code Name</th>
        <th>Data Element</th>
	</thead>
	<tr>
        <td id="{@id}"><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="name"/></td>
	    <xsl:apply-templates select="data_ele"/>
	</tr>
	</table>
	<table>
	<xsl:apply-templates select="version"/>
	</table>
    <p/>
    </xsl:template>

    <xsl:template match="version">
	<tr>
	<td class="code">
        <xsl:for-each select="code">
	    <xsl:value-of select="."/><xsl:text> </xsl:text> 
        </xsl:for-each>
	</td>
	</tr>
    </xsl:template>

    <xsl:template match="codeset/data_ele">
        <td><a href="dataele.html#{.}"><xsl:value-of select="."/></a></td>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
