<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:l">
        <xsl:variable name="line-nr">
            <xsl:number level="any" from="tei:div"/>
        </xsl:variable>
        <xsl:for-each select=".">
            <tr>
                <td>
                    <xsl:attribute name="id">
                        <xsl:value-of select="$line-nr + (number($line-index) - 1)"/>
                    </xsl:attribute>
                    <xsl:if test="($line-nr + (number($line-index) - 1)) mod $interval = 0">
                        <xsl:value-of select="$line-nr + (number($line-index) - 1)"/> 
                    </xsl:if>
                </td>
                <td>
                    <xsl:if test="$line-nr = '1'">
                        <xsl:attribute name="class">first-line</xsl:attribute>
                    </xsl:if>
                    <span class="verse">
                        <xsl:apply-templates/>
                    </span>
                </td>
            </tr>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>