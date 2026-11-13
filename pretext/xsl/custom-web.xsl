<?xml version="1.0" encoding="UTF-8"?>
<!--
  Custom HTML stylesheet for the IMS book.

  Why this exists: every <part> in this book has an <introduction>.
  PreTeXt's HTML conversion treats a part as a summary (intermediate) page,
  and when building the "next" link it descends into the part's first child.
  That child is the <introduction>, but PreTeXt's rule for introductions that
  get their own page (DIVISION-COMPANION) leaves out <part>, so it logs

    PTX:ERROR: descending into first node of an intermediate page (introduction)
    that is non-structural

  for every part.  The introduction is shown on the part's own page, so the
  correct "next" link from a part page is simply its first chapter.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="./core/pretext-html.xsl"/>

  <xsl:template match="part" mode="next-linear-url">
    <xsl:choose>
      <xsl:when test="chapter">
        <xsl:apply-templates select="chapter[1]" mode="url"/>
      </xsl:when>
      <xsl:otherwise>
        <!-- no chapters: go sideways, as the generic template would -->
        <xsl:apply-templates select="." mode="next-sideways-url"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
