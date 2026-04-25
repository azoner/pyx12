<?xml version="1.0"?>
<!-- 
######################################################################
# Copyright (c) 2001-2007 Kalamazoo Community Mental Health Services,
#   John Holland <jholland@kazoocmh.org> <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html"/>

  <xsl:template match="/">
	<html>
	<head>
	<title>X12 Data Elements</title>
	<link rel="stylesheet" type="text/css" href="dataele.css" title="stylebasic"/>
	</head>
	<body>
	<table>
    <thead>
        <th>Data Element Number</th>
        <th>Data Type</th>
        <th>Minimum Length</th>
        <th>Maximum Length</th>
        <th>Data Element Name</th>
    </thead>
	<xsl:apply-templates/>
	</table>
	</body>
	</html>
  </xsl:template>

    <xsl:template match="data_ele">
	<tr class="element" id="{@ele_num}">
        <td><xsl:value-of select="@ele_num"/></td>
        <td><xsl:value-of select="@data_type"/></td>
        <td><xsl:value-of select="@min_len"/></td>
        <td><xsl:value-of select="@max_len"/></td>
        <td><xsl:value-of select="@name"/></td>
	</tr>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
