<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- Remove data_type, min_len, and max_len from element nodes -->

<xsl:output method="xml" indent="yes"/>

  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="element/data_type"/>
  <xsl:template match="element/min_len"/>
  <xsl:template match="element/max_len"/>
 
</xsl:stylesheet>
