<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <!-- <xsl:template match="/transaction[@xid='835']/*/loop[@xid='1000B']/usage"> -->
  <!--
  add valid code
  delete valid code
  alter valid code
  -->

  <!-- Alter usage -->
  <xsl:template match="loop[@xid='1000B']/usage">
    <usage>S</usage>
  </xsl:template>

  <!-- Add a valid code-->
  <xsl:template match="element[@xid='BPR01']/valid_codes">
    <valid_codes>
      <xsl:apply-templates select="code"/>
      <code>Z</code>
    </valid_codes>
  </xsl:template>

  <!-- Alter a valid code
  <xsl:template match="element[@xid='BPR04']/valid_codes/code['FWT']">
    <code>XXX</code>
  </xsl:template>
-->

</xsl:stylesheet>
