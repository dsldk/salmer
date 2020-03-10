<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:placeName[ancestor::tei:p]">
        <xsl:variable name="note-identifier">
            <xsl:text>Note</xsl:text>
            <xsl:number count="tei:placeName" level="any" from="tei:text" format="a"/>
        </xsl:variable>
        <span class="notelink" id="placeNamelink{$note-identifier}" onclick="toggle({$note-identifier});">
            <span class="placeName">
                <xsl:value-of select="."/>
            </span>
            <sup>[<xsl:call-template name="placeNameN"/>]</sup>
        </span>
        <span class="placeNamecontents" id="{$note-identifier}" style="display: none;">
            <xsl:apply-templates select="@key"/>
        </span>
    </xsl:template>
    <xsl:template name="placeNameN">
        <xsl:number from="tei:text" level="any" format="a"/>
    </xsl:template>
</xsl:stylesheet>