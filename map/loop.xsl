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


  <xsl:template match="/">
	<html>
	<head>
	<title><xsl:value-of select="/map/transaction/name"/></title>
	<link rel="stylesheet" type="text/css" href="loop.css" title="stylebasic"/>
	</head>
	<body>
	<xsl:apply-templates/>
	</body>
	</html>
  </xsl:template>


  <xsl:output method="html"/>

  <xsl:template match="/map/transaction">
	<h2><xsl:value-of select="name"/></h2>
        <table>
	<xsl:apply-templates/>
	</table>
  </xsl:template>

    <xsl:template match="loop">
    	<tr><td colspan="4">
	<table>
	<tr class="loop">
        <td><xsl:value-of select="pos"/></td>
        <td><strong><xsl:value-of select="@xid"/> - <xsl:value-of select="name"/></strong></td>
        <!-- <td><xsl:value-of select="count"/></td> -->
	</tr>
	<xsl:apply-templates/>
	</table>
	</td></tr>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
