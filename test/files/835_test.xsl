<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--
Stylesheet to alter pyx12 maps
Should use a match pattern starting with /transaction[@xid='xxx']// to ensure
the transform only modifies the intended map.
Applying the transform to another map should be a no-op.
-->

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <!--
  delete valid code
  alter valid code
  -->

  <!-- Alter usage -->
  <xsl:template match="/transaction[@xid='835']//loop[@xid='1000B']/usage">
    <usage>S</usage>
  </xsl:template>

  <!-- Add a valid code-->
  <xsl:template match="/transaction[@xid='835']//element[@xid='BPR01']/valid_codes">
    <valid_codes>
      <xsl:apply-templates select="code"/>
      <code>Z</code>
    </valid_codes>
  </xsl:template>

  <!-- Add a regex to an element-->
  <xsl:template match="/transaction[@xid='835']//element[@xid='CLP07']">
    <element xid="CLP07">
      <xsl:apply-templates/>
      <regex>[0-9]*</regex>
    </element>
  </xsl:template>

  <!-- Alter a valid code
  <xsl:template match="element[@xid='BPR04']/valid_codes/code['FWT']">
    <code>XXX</code>
  </xsl:template>
-->

</xsl:stylesheet>
