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
        <td><strong><xsl:value-of select="@xid"/> - <xsl:value-of select="name"/></strong></td>
	<td colspan="2"></td>
        <td><xsl:value-of select="count"/></td>
	</tr>
	<xsl:apply-templates/>
	</table>
	</td></tr>
    </xsl:template>


    <xsl:template match="segment">
	<div class="segment">
        <xsl:value-of select="@xid"/>-
        <xsl:value-of select="name"/><xsl:text>    </xsl:text>
        <span class="syntax"><xsl:for-each select="syntax"><xsl:value-of select="."/><xsl:text> </xsl:text></xsl:for-each></span>
	</div>
	<table>
	<xsl:apply-templates/>
	</table>
	<p></p>
    </xsl:template>

    <xsl:template match="element">
	<tr class="element">
        <td  style="width: 10%"><xsl:value-of select="seq"/></td>
        <xsl:apply-templates select="data_ele"/>
        <td style="width: 30%"><xsl:value-of select="name"/></td>
        <td style="width: 10%"><xsl:value-of select="usage"/></td>
        <td style="width: 10%"><xsl:value-of select="refdes"/></td>
	</tr>
	<!-- <xsl:apply-templates select="valid_codes"/> -->
	<xsl:apply-templates select="valid_codes"/>
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
	<td colspan="6"></td>
	    <td><xsl:value-of select="."/></td>
	</tr>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="valid_codes">
	<tr>
	<td colspan="1"></td>
	<td class="code" colspan="5">
	<xsl:apply-templates select="@external"/>
        <xsl:for-each select="code">
	    <!-- <xsl:sort select="code" lang="en" order="ascending" case-order="upper-first"/> -->
	    <xsl:value-of select="."/><xsl:text> </xsl:text> 
        </xsl:for-each>
	</td>
	</tr>
    </xsl:template>

    <xsl:template match="@external">
	<xsl:text>External Source: </xsl:text>
	<a href="codes.html#{.}"><xsl:value-of select="."/></a>
	<xsl:text> </xsl:text>
    </xsl:template>

    <xsl:template match="element/data_ele">
        <td style="width: 10%"><a href="dataele.html#{.}"><xsl:value-of select="."/></a></td>
    </xsl:template>

    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
