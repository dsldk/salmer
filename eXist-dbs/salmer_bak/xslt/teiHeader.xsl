<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:teiHeader">
        <div class="metadata" id="metadata-section">
            <h1>Om denne udgave</h1>
            <div>
                <p>
                    <strong>Titel: </strong>
                    <xsl:value-of select="//tei:titleStmt/tei:title"/>
                </p>
                <xsl:if test="//tei:titleStmt/tei:author[text() != 'empty']">
                    <p>
                        <strong>Forfatter: </strong>
                        <xsl:value-of select="//tei:titleStmt/tei:author"/>
                    </p>
                </xsl:if>
                <xsl:if test="//tei:profileDesc/tei:abstract[tei:ab/text() != 'empty']">
                    <p>
                        <strong>Resume: </strong>
                        <xsl:apply-templates select="//tei:profileDesc/tei:abstract"/>
                    </p>
                </xsl:if>
                <p>
                    <xsl:choose>
                        <xsl:when test="count(//tei:titleStmt/tei:editor) gt 1">
                            <strong>Redaktører: </strong>
                        </xsl:when>
                        <xsl:otherwise>
                            <strong>Redaktør: </strong>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:for-each select="//tei:titleStmt/tei:editor">
                        <xsl:value-of select="tei:name//tei:forename"/>
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="tei:name//tei:surname"/>
                        <xsl:if test="position() != last()">, </xsl:if>
                        <xsl:if test="position() = last() and child::node() != 'empty'">. </xsl:if>
                    </xsl:for-each>
                    <!--<xsl:value-of
                                                select="tei:teiHeader//tei:editor/tei:name/@xml:id"
                                            />-->
                </p>
                <!--<p> Dokumentets historik: </p>-->
            </div>
            <div>
                <!--<xsl:apply-templates select="tei:encodingDesc"/>-->
            </div>
            <div>
                <!--<xsl:apply-templates select="tei:profileDesc"/>-->
            </div>
            <div>
                <xsl:apply-templates select="tei:fileDesc/tei:sourceDesc"/>
            </div>
            <div>
                <xsl:if test="tei:fileDesc/tei:publicationStmt/tei:publisher[//text() != 'empty']">
                    <p>
                        <strong>Udgiver: </strong><xsl:apply-templates select="tei:fileDesc/tei:publicationStmt/tei:publisher"/>, <xsl:value-of select="tei:fileDesc/tei:publicationStmt/tei:pubPlace"/>, <xsl:value-of select="tei:fileDesc/tei:publicationStmt/tei:date"/>
                    </p>
                </xsl:if>
            </div>
            <div>
<!--                <xsl:if test="//tei:titleStmt/tei:funder/tei:ref[text() != 'empty']">-->
                    <xsl:if test="//tei:titleStmt/tei:funder[tei:ref | text() != 'empty']">
                    <p>
                        <strong>Fremstillet med støtte fra: </strong>
                    </p>
                    <ul style="list-style: none;">
                        <xsl:for-each select="//tei:titleStmt/tei:funder">
                            <li>
                                <xsl:apply-templates select="."/>
                            </li>
                        </xsl:for-each>
                    </ul>
                </xsl:if>
            </div>
            
        </div>
    </xsl:template>
</xsl:stylesheet>