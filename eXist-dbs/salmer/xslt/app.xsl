<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
    <xsl:template match="tei:app[tei:lem]">
        <xsl:variable name="identifier">
            <xsl:text>App</xsl:text>
            <xsl:number count="tei:app[tei:lem]" level="any" from="tei:div"/>
        </xsl:variable>
        <xsl:apply-templates select="tei:lem"/>
        <span class="notelink" id="notelink{$identifier}" onclick="toggle({$identifier});">
            <sup>[<xsl:call-template name="appN"/>]</sup>
        </span>
        <xsl:text> </xsl:text>
        <span class="appnotecontents" id="{$identifier}" style="display: none;">
            <xsl:apply-templates select="tei:lem"/>
            <xsl:text>] </xsl:text>
            <xsl:text>  </xsl:text>
            <xsl:apply-templates select="tei:rdg"/>
            <xsl:text> </xsl:text>
        </span>
    </xsl:template>
    <xsl:template name="appN">
        <xsl:number count="tei:app[tei:lem]" level="any" from="tei:div"/>
    </xsl:template>
    <xsl:template match="tei:app[@type]"/>
    <xsl:template match="tei:rdg">
        <!--<xsl:apply-templates select="text()"/>-->
        <xsl:apply-templates/>
        <xsl:text> </xsl:text>
        <xsl:if test="@wit">
            <em>
                <!-- Since values in the must be prefixed with a # 
                 we use tokenize() to obtain the substring after # -->
                <xsl:value-of select="@wit/tokenize(., '#')"/>
            </em>
        </xsl:if>
        <xsl:if test="tei:note">
            <xsl:text>, </xsl:text>
            <xsl:apply-templates select="tei:note"/>
        </xsl:if>
        <xsl:choose>
            <xsl:when test="tei:ex">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:when test="@wit"/>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>