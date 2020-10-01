<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:param name="line-index" select="line-index"/>
    <xsl:param name="pb-index" select="pb-index"/>
    <xsl:param name="interval" select="5" as="xs:integer"/>
    <xsl:param name="facs"/>
    <xsl:param name="n"/>
    <xsl:include href="dsl-basis/byline.xsl"/>
    <xsl:include href="dsl-basis/damage.xsl"/>
    <xsl:include href="dsl-basis/div.xsl"/>
    <xsl:include href="dsl-basis/docAuthor.xsl"/>
    <xsl:include href="dsl-basis/docImprint.xsl"/>
    <xsl:include href="dsl-basis/docTitle.xsl"/>
    <xsl:include href="dsl-basis/epigraph.xsl"/>
    <xsl:include href="dsl-basis/emph.xsl"/>
    <!-- disable <xsl:include href="dsl-basis/figure.xsl"/>-->
    <xsl:include href="dsl-basis/front.xsl"/>
    <xsl:include href="dsl-basis/gap.xsl"/>
    <xsl:include href="dsl-basis/history.xsl"/>
    <xsl:include href="dsl-basis/imprimatur.xsl"/>
    <xsl:include href="dsl-basis/item.xsl"/>
    <xsl:include href="dsl-basis/l.xsl"/>
    <xsl:include href="dsl-basis/list.xsl"/>
    <xsl:include href="dsl-basis/lg.xsl"/>
    <xsl:include href="dsl-basis/lb.xsl"/>
    <xsl:include href="dsl-basis/listWit.xsl"/>
    <xsl:include href="dsl-basis/msDesc.xsl"/>
    <xsl:include href="dsl-basis/msIdentifier.xsl"/>
    <xsl:include href="dsl-basis/objectDesc.xsl"/>
    <xsl:include href="dsl-basis/p.xsl"/>
    <xsl:include href="dsl-basis/physDesc.xsl"/>
    <xsl:include href="dsl-basis/q.xsl"/>
    <xsl:include href="dsl-basis/signed.xsl"/>
    <xsl:include href="dsl-basis/sourceDesc.xsl"/>
    <xsl:include href="dsl-basis/sp.xsl"/>
    <xsl:include href="dsl-basis/speaker.xsl"/>
    <xsl:include href="dsl-basis/stage.xsl"/>
    <xsl:include href="dsl-basis/supplied.xsl"/>
    <xsl:include href="dsl-basis/supportDesc.xsl"/>
    <xsl:include href="dsl-basis/support.xsl"/>
    <xsl:include href="dsl-basis/titlePage.xsl"/>
    <xsl:include href="dsl-basis/witness.xsl"/>
    <xsl:include href="app.xsl"/>
    <xsl:include href="bibl.xsl"/>
    <xsl:include href="c.xsl"/>
    <!--<xsl:include href="cell.xsl"/>-->
    <xsl:include href="ex.xsl"/>
    <xsl:include href="head.xsl"/>
    <xsl:include href="hi.xsl"/>
    <xsl:include href="notatedMusic.xsl"/>
    <xsl:include href="note.xsl"/>
    <xsl:include href="pb.xsl"/>
    <xsl:include href="persName.xsl"/>
    <xsl:include href="placeName.xsl"/>
    <xsl:include href="ref.xsl"/>
    <!--<xsl:include href="row.xsl"/>-->
    <xsl:include href="dsl-basis/table.xsl"/>
    <xsl:include href="teiHeader.xsl"/>
    <xsl:include href="w.xsl"/>
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:preserve-space elements="tei:p tei:q"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
        <xsl:value-of select="$pb-index"/>
        <!-- footer below this point -->
        <!--<div class="col-md-12">
            <div class="document-footer">
                <hr/>
                <p class="cite">
                    <strong>Citér denne tekst: </strong> tekstnet.dk, 
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>, online siden: <xsl:value-of select="tei:teiHeader//tei:publicationStmt/tei:date"/>, besøgt:
                    <xsl:value-of select="current-date()"/>, URL:
                    https://tekstnet.dk/<xsl:value-of select="tei:teiHeader//tei:publicationStmt/tei:idno[@type]"/>
                </p>
                <xsl:variable name="id" select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                <p class="contact">
                    <strong>Rapportér et problem </strong>
                    <span class="artikelkilde">vedr. <a class="fejlrapport" target="_blank" href="mailto:smn@dsl.dk?subject=Ang.%20tekstnet.dk%20nr.%20{$id}" title="Send os en mail hvis du opdager en fejl. Spørgsmål besvares desværre ikke.">tekstnet.dk <xsl:value-of select="$id"/>
                    </a>
                    </span>
                </p>
                <hr/>
            </div>
        </div>-->
    </xsl:template>
</xsl:stylesheet>