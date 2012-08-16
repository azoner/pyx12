<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@type!='']">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="child::id"/></xsl:attribute>
      <xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy> <xsl:comment>End of <xsl:value-of select="child::id"/> loop</xsl:comment>
  </xsl:template>
  
  <xsl:template match="loop">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="child::id"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy> <xsl:comment>End of <xsl:value-of select="child::id"/> loop</xsl:comment>
  </xsl:template>

  <xsl:template match="loop/id"/>
  <xsl:template match="loop/pos"/>

  <xsl:template match="loop/seq">
    <pos><xsl:value-of select="."/></pos>
  </xsl:template>

  <xsl:template match="segment">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="child::id"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy> <xsl:comment>End of <xsl:value-of select="child::id"/> segment</xsl:comment>
  </xsl:template>

  <xsl:template match="segment/id"/>
 
  <xsl:template match="element">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="child::refdes"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="element/refdes"/>
 
</xsl:stylesheet>
