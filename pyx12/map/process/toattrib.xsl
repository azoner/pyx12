<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop">
    <loop>
      <xsl:attribute name="id"><xsl:value-of select="child::id"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="seq"><xsl:value-of select="child::seq"/></xsl:attribute>
      <xsl:attribute name="pos"><xsl:value-of select="child::pos"/></xsl:attribute>
      <xsl:attribute name="repeat"><xsl:value-of select="child::repeat"/></xsl:attribute>
      <xsl:attribute name="type"><xsl:value-of select="@type[@type='explicit']"/></xsl:attribute>
      <xsl:apply-templates/>
    </loop>
  </xsl:template>
  
  <xsl:template match="loop/id"/>
  <xsl:template match="loop/usage"/>
  <xsl:template match="loop/seq"/>
  <xsl:template match="loop/pos"/>
  <xsl:template match="loop/repeat"/>

  <xsl:template match="segment">
    <segment>
      <xsl:attribute name="id"><xsl:value-of select="child::id"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="pos"><xsl:value-of select="child::pos"/></xsl:attribute>
      <xsl:attribute name="max_use"><xsl:value-of select="child::max_use"/></xsl:attribute>
      <xsl:apply-templates/>
    </segment>
  </xsl:template>
  
  <xsl:template match="segment/id"/>
  <xsl:template match="segment/usage"/>
  <xsl:template match="segment/pos"/>
  <xsl:template match="segment/max_use"/>

  <xsl:template match="element">
    <element>
      <xsl:attribute name="refdes"><xsl:value-of select="child::refdes"/></xsl:attribute>
      <xsl:attribute name="seq"><xsl:value-of select="child::seq"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="data_type"><xsl:value-of select="child::data_type"/></xsl:attribute>
      <xsl:attribute name="min_len"><xsl:value-of select="child::min_len"/></xsl:attribute>
      <xsl:attribute name="max_len"><xsl:value-of select="child::max_len"/></xsl:attribute>
      <xsl:attribute name="data_ele"><xsl:value-of select="child::data_ele"/></xsl:attribute>
      <xsl:apply-templates/>
    </element>
  </xsl:template>
  
  <xsl:template match="element/refdes"/>
  <xsl:template match="element/seq"/>
  <xsl:template match="element/usage"/>
  <xsl:template match="element/data_type"/>
  <xsl:template match="element/min_len"/>
  <xsl:template match="element/max_len"/>
  <xsl:template match="element/data_ele"/>

</xsl:stylesheet>
