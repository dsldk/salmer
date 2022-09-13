<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:include href="app.xsl"/>
    <xsl:include href="bibl.xsl"/>
    <xsl:include href="byline.xsl"/>
    <xsl:include href="cit.xsl"/>
    <xsl:include href="damage.xsl"/>
    <xsl:include href="div.xsl"/>
    <xsl:include href="docAuthor.xsl"/>
    <xsl:include href="docImprint.xsl"/>
    <xsl:include href="docTitle.xsl"/>
    <xsl:include href="emph.xsl"/>
    <xsl:include href="epigraph.xsl"/>
    <xsl:include href="front.xsl"/>
    <xsl:include href="gap.xsl"/>
    <xsl:include href="head.xsl"/>
    <xsl:include href="hi.xsl"/>
    <xsl:include href="imprimatur.xsl"/>
    <xsl:include href="l.xsl"/>
    <xsl:include href="lb.xsl"/>
    <xsl:include href="lg.xsl"/>
    <xsl:include href="listWit.xsl"/>
    <xsl:include href="msDesc.xsl"/>
    <xsl:include href="msIdentifier.xsl"/>
    <xsl:include href="note.xsl"/>
    <xsl:include href="p.xsl"/>
    <xsl:include href="pb.xsl"/>
    <xsl:include href="persName.xsl"/>
    <xsl:include href="placeName.xsl"/>
    <xsl:include href="q.xsl"/>
    <xsl:include href="signed.xsl"/>
    <xsl:include href="sourceDesc.xsl"/>
    <xsl:include href="sp.xsl"/>
    <xsl:include href="speaker.xsl"/>
    <xsl:include href="stage.xsl"/>
    <xsl:include href="supplied.xsl"/>
    <xsl:include href="titlePage.xsl"/>
    <xsl:include href="witness.xsl"/>
    <!--<xsl:include href="title.xsl"/>-->
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
   <!-- <xsl:strip-space elements="*"/> -->
    <xsl:preserve-space elements="tei:p"/>
    <xsl:template match="/">
        <xsl:apply-templates select="tei:TEI"/>
    </xsl:template>
    <xsl:template match="tei:TEI">
        <html>
            <head>
                <title>
                    <xsl:value-of select="//teiHeader//tei:title"/>
                </title>
                <link>
                    <xsl:attribute name="rel">stylesheet</xsl:attribute>
                    <xsl:attribute name="href">../css/screen.css</xsl:attribute>
                    <xsl:attribute name="type">text/css</xsl:attribute>
                    <xsl:attribute name="media">screen</xsl:attribute>
                </link>
                <link>
                    <xsl:attribute name="rel">stylesheet</xsl:attribute>
                    <xsl:attribute name="href">../css/print.css</xsl:attribute>
                    <xsl:attribute name="type">text/css</xsl:attribute>
                    <xsl:attribute name="media">print</xsl:attribute>
                </link>
            </head>
            <body>
                <div class="content">
                    <div>
                        <h1>
                            <xsl:apply-templates select="tei:title"/>
                        </h1>
                    </div>
                    <div>
                        <xsl:apply-templates select="tei:teiHeader/tei:fileDesc/tei:sourceDesc"/>
                    </div>
                    <div>
                        <xsl:apply-templates select="tei:text"/>
                    </div>
                    <xsl:if test="//tei:app">
                        <div>
                            <h2>Kritisk apparat</h2>
                            <xsl:apply-templates select="//tei:app" mode="apparatusCriticus"/>
                        </div>
                    </xsl:if>
                    <xsl:if test="//tei:note">
                        <div>
                            <h2>Noter</h2>
                            <xsl:apply-templates select="//tei:note" mode="footnoteApparatus"/>
                        </div>
                    </xsl:if>
                    <!--<xsl:if test="//tei:note[@type='add']">
                    <div>
                        <h3>Kommentarer</h3>
                        <xsl:apply-templates select="//tei:note[@type='add']"/>
                    </div>
                </xsl:if>-->
                </div>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="tei:text">
        <xsl:choose>
            <xsl:when test="tei:front">
                <!--<div class="metadata">
                    <h4 class="caption">Front: </h4>-->
                <xsl:apply-templates/>
                <!--</div>-->
            </xsl:when>
            <xsl:otherwise>
                <h4>Front: n/a</h4>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
            <xsl:when test="tei:body">
                <xsl:apply-templates select="tei:body"/>
            </xsl:when>
            <xsl:otherwise>
                <h4>Text body: n/a</h4>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="tei:body">
        <!--<h2>Text body:</h2>-->
        <div class="body">
            <!--<span class="caption">Text body: </span>-->
            <xsl:apply-templates/>
        </div>
    </xsl:template>
</xsl:stylesheet>