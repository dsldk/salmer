<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:bibl[ancestor::tei:p]">
        <xsl:variable name="note-identifier">
            <xsl:text>Note</xsl:text>
            <xsl:number count="tei:bibl" level="any" from="tei:text" format="0001"/>
        </xsl:variable>
        <span class="notelink" id="bibllink{$note-identifier}" onclick="toggle({$note-identifier});">
            <span class="bibl">
                <xsl:apply-templates/>
                <!--<xsl:value-of select="."/>-->
            </span>
            <sup>[<xsl:call-template name="biblN"/>]</sup>
        </span>
        <span class="biblcontents" id="{$note-identifier}" style="display: none;">
            <xsl:apply-templates select="@n"/>
        </span>
    </xsl:template>
    <xsl:template name="biblN">
        <xsl:number from="tei:text" level="any" format="0001"/>
    </xsl:template>
</xsl:stylesheet>