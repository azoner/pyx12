<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='ISA']">
    <xsl:copy>
    <xsl:attribute name="xid">ISA_LOOP</xsl:attribute>
    <xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='GS']">
    <xsl:copy>
    <xsl:attribute name="xid">GS_LOOP</xsl:attribute>
    <xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@xid='ST']">
    <xsl:copy>
    <xsl:attribute name="xid">ST_LOOP</xsl:attribute>
    <xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
