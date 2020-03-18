<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:w">
        <xsl:choose>
            <xsl:when test="string(number(@lemma)) != 'NaN'">
                <a invalid_href="http://test.ordnet.dk/go/ordbog?query=%20&amp;entry_id={@lemma}" target="go" id="lemma-id{@lemma}" onclick="call_a_web_service(event, {@lemma});">
                    <xsl:apply-templates select="node()"/>
                </a>
                <!--<xsl:apply-templates />-->
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>