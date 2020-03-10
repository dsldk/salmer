<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:ref[ancestor::tei:p][@type='note']">
        <xsl:variable name="ref-identifier">
            <xsl:text>Note</xsl:text>
            <xsl:number count="tei:ref" level="any" from="tei:text" format="1"/>
        </xsl:variable>
        <span class="realnote" id="notelink{$ref-identifier}" onclick="toggle({$ref-identifier});">
            <span class="annotation-marker">
                <a href="notelink{@target}">⁕</a>
            </span>
        </span>
        <span class="notecontents" id="{$ref-identifier}" style="display: none;">
            <xsl:apply-templates/>
            <xsl:apply-templates select="@target"/>
        </span>
    </xsl:template>
    <xsl:template match="tei:ref[ancestor::tei:p][@type='variant']">
        <xsl:variable name="ref-identifier">
            <xsl:text>Variant</xsl:text>
            <xsl:number count="tei:ref" level="any" from="tei:text" format="1"/>
        </xsl:variable>
        <span class="variant" id="variantlink{$ref-identifier}" onclick="toggle({$ref-identifier});">
            <span class="annotation-marker">
                <a href="variantlink{@target}">‡</a>
            </span>
        </span>
        <span class="variantcontents" id="{$ref-identifier}" style="display: none;">
            <xsl:apply-templates/>
            <xsl:apply-templates select="@target"/>
        </span>
    </xsl:template>
    <xsl:template name="refN">
        <xsl:number from="tei:text" level="any" format="1"/>
    </xsl:template>
</xsl:stylesheet>