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
    <link rel="stylesheet" type="text/css" href="sum.css" title="stylebasic"/>
    <link rel="alternate stylesheet" href="plain.css" title="Plain" />
    <link rel="alternate stylesheet" href="none.css" title="No Style" />
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
            <td><strong><xsl:value-of select="pos"/></strong></td>
            <td></td>
            <td><strong><xsl:value-of select="@xid"/> - <xsl:value-of select="name"/></strong></td>
            <td colspan="2"></td>
            <td><xsl:value-of select="count"/></td>
            </tr>
            <xsl:apply-templates/>
        </table>
    </td></tr>
  </xsl:template>


    <xsl:template match="segment">
    <tr class="segment">
        <td><xsl:value-of select="pos"/></td>
        <td><xsl:value-of select="@xid"/></td>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="usage"/></td>
        <td><xsl:value-of select="max_use"/></td>
    <td></td>
    </tr>
    <xsl:apply-templates/>
    </xsl:template>


    <xsl:template match="text()|@*"/>

</xsl:stylesheet>
