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
    <xsl:attribute name="xid">ISA_LOOP</xsl:attribute>
  </xsl:template>
  
  <xsl:template match="loop[@xid='GS']">
    <xsl:attribute name="xid">GS_LOOP</xsl:attribute>
  </xsl:template>

  <xsl:template match="loop[@xid='ST']">
    <xsl:attribute name="xid">ST_LOOP</xsl:attribute>
  </xsl:template>
 
</xsl:stylesheet>
