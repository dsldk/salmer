<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:include href="dsl-basis/byline.xsl"/>
    <xsl:include href="dsl-basis/damage.xsl"/>
    <xsl:include href="dsl-basis/docAuthor.xsl"/>
    <xsl:include href="dsl-basis/docImprint.xsl"/>
    <xsl:include href="dsl-basis/docTitle.xsl"/>
    <xsl:include href="dsl-basis/epigraph.xsl"/>
    <xsl:include href="dsl-basis/emph.xsl"/>
    <xsl:include href="dsl-basis/front.xsl"/>
    <xsl:include href="dsl-basis/gap.xsl"/>
    <xsl:include href="dsl-basis/head.xsl"/>
    <xsl:include href="dsl-basis/hi.xsl"/>
    <xsl:include href="dsl-basis/imprimatur.xsl"/>
    <xsl:include href="dsl-basis/l.xsl"/>
    <xsl:include href="dsl-basis/lb.xsl"/>
    <xsl:include href="dsl-basis/lg.xsl"/>
    <xsl:include href="dsl-basis/listWit.xsl"/>
    <xsl:include href="dsl-basis/msDesc.xsl"/>
    <xsl:include href="dsl-basis/msIdentifier.xsl"/>
    <xsl:include href="pb.xsl"/>
    <xsl:include href="dsl-basis/q.xsl"/>
    <xsl:include href="dsl-basis/signed.xsl"/>
    <xsl:include href="dsl-basis/sourceDesc.xsl"/>
    <xsl:include href="dsl-basis/sp.xsl"/>
    <xsl:include href="dsl-basis/speaker.xsl"/>
    <xsl:include href="dsl-basis/stage.xsl"/>
    <xsl:include href="dsl-basis/supplied.xsl"/>
    <xsl:include href="dsl-basis/titlePage.xsl"/>
    <xsl:include href="dsl-basis/witness.xsl"/>
    <xsl:include href="app.xsl"/>
    <xsl:include href="bibl.xsl"/>
    <xsl:include href="div.xsl"/>
    <xsl:include href="note.xsl"/>
    <xsl:include href="p.xsl"/>
    <xsl:include href="persName.xsl"/>
    <xsl:include href="placeName.xsl"/>
    <xsl:include href="ref.xsl"/>
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:preserve-space elements="tei:p tei:q"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>