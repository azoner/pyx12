<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:strip-space elements="*" />

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop[@type!='']">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="@xid"/></xsl:attribute>
      <xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="pos"><xsl:value-of select="child::pos"/></xsl:attribute>
      <xsl:attribute name="repeat"><xsl:value-of select="child::repeat"/></xsl:attribute>
      <xsl:attribute name="name"><xsl:value-of select="child::name"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="loop">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="@xid"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="pos"><xsl:value-of select="child::pos"/></xsl:attribute>
      <xsl:attribute name="repeat"><xsl:value-of select="child::repeat"/></xsl:attribute>
      <xsl:attribute name="name"><xsl:value-of select="child::name"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="loop/id"/>
  <xsl:template match="loop/pos"/>
  <xsl:template match="loop/usage"/>
  <xsl:template match="loop/repeat"/>
  <xsl:template match="loop/name"/>
 
  <xsl:template match="segment">
    <xsl:copy>
      <xsl:attribute name="xid"><xsl:value-of select="@xid"/></xsl:attribute>
      <xsl:attribute name="pos"><xsl:value-of select="child::pos"/></xsl:attribute>
      <xsl:attribute name="usage"><xsl:value-of select="child::usage"/></xsl:attribute>
      <xsl:attribute name="max_use"><xsl:value-of select="child::max_use"/></xsl:attribute>
      <xsl:attribute name="name"><xsl:value-of select="child::name"/></xsl:attribute>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="segment/id"/>
  <xsl:template match="segment/pos"/>
  <xsl:template match="segment/usage"/>
  <xsl:template match="segment/max_use"/>
  <xsl:template match="segment/name"/>

  <xsl:template match="element" />
  <xsl:template match="composite" />
  <xsl:template match="comment()" />
</xsl:stylesheet>
