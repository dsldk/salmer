<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:persName[ancestor::tei:p and @type='fictional']">
        <xsl:variable name="note-identifier">
            <xsl:text>Note</xsl:text>
            <xsl:number count="tei:persName" level="any" from="tei:text" format="i"/>
        </xsl:variable>
        <span class="notelink" id="fictionalpersNamelink{$note-identifier}" onclick="toggle({$note-identifier});">
            <span class="fictionalpersName">
                <xsl:value-of select="."/>
            </span>
            <sup>[<xsl:call-template name="fictionalpersNameN"/>]</sup>
        </span>
        <span class="fictionalpersNamecontents" id="{$note-identifier}" style="display: none;">
            <xsl:apply-templates select="@key"/>
        </span>
    </xsl:template>
    <xsl:template name="fictionalpersNameN">
        <xsl:number from="tei:text" level="any" format="i"/>
    </xsl:template>
    <xsl:template match="tei:persName[ancestor::tei:p and not(@type)]">
        <xsl:variable name="note-identifier">
            <xsl:text>Note</xsl:text>
            <xsl:number count="tei:persName" level="any" from="tei:text" format="I"/>
        </xsl:variable>
        <span class="notelink" id="persNamelink{$note-identifier}" onclick="toggle({$note-identifier});">
            <span class="persName">
                <!--<xsl:value-of select="."/>-->
                <xsl:apply-templates/>
            </span>
            <sup>[<xsl:call-template name="persNameN"/>]</sup>
        </span>
        <span class="persNamecontents" id="{$note-identifier}" style="display: none;">
            <xsl:apply-templates select="@key"/>
        </span>
    </xsl:template>
    <xsl:template name="persNameN">
        <xsl:number from="tei:text" level="any" format="I"/>
    </xsl:template>
</xsl:stylesheet>