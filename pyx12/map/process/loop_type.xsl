<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='DETAIL']">
    <xsl:copy>
    <xsl:attribute name="xid">DETAIL</xsl:attribute>
    <xsl:attribute name="type">wrapper</xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='HEADER']">
    <xsl:copy>
    <xsl:attribute name="xid">HEADER</xsl:attribute>
    <xsl:attribute name="type">wrapper</xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='FOOTER']">
    <xsl:copy>
    <xsl:attribute name="xid">FOOTER</xsl:attribute>
    <xsl:attribute name="type">wrapper</xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
