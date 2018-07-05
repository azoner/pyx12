<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="segment[@xid='ISA']/pos"><pos>010</pos></xsl:template>
  <xsl:template match="loop[@xid='GS']/pos"><pos>020</pos></xsl:template>
  <xsl:template match="segment[@xid='TA1']/pos"><pos>020</pos></xsl:template>
  <xsl:template match="segment[@xid='IEA']/pos"><pos>030</pos></xsl:template>
 
  <xsl:template match="segment[@xid='GS']/pos"><pos>010</pos></xsl:template>
  <xsl:template match="loop[@xid='ST']/pos"><pos>020</pos></xsl:template>
  <xsl:template match="segment[@xid='GE']/pos"><pos>030</pos></xsl:template>
 
  <xsl:template match="loop[@xid='HEADER']/pos"><pos>010</pos></xsl:template>
  <xsl:template match="loop[@xid='DETAIL']/pos"><pos>020</pos></xsl:template>
  <xsl:template match="loop[@xid='FOOTER']/pos"><pos>030</pos></xsl:template>
 
</xsl:stylesheet>
