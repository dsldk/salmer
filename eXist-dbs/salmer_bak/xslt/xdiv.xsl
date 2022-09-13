<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:div">
        <div>
            <table>
                <xsl:apply-templates select="tei:head[@type = 'original'] | tei:lg | tei:p | tei:table"/>
            </table>
        </div>
    </xsl:template>
</xsl:stylesheet>