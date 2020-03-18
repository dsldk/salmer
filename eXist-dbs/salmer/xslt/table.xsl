<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:table[@rend = 'reg']">
        <table>
            <xsl:apply-templates/>
        </table>
    </xsl:template>
</xsl:stylesheet>