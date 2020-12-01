<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ext="http://exslt.org/common" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei ext" version="2.0">

    <xsl:template match="tei:ref">
        <xsl:choose>
            <xsl:when test="starts-with(@target, 'http')">
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="@target"/>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </a>
            </xsl:when>
            <xsl:when test="starts-with(@target, '#')">
                <a>
                    <xsl:attribute name="href">
                        <xsl:variable name="targetRef" select="substring-after(@target, '#')"/>
                        <!-- The following performs poorly if more than a few look-ups are needed -->
                        <!--<xsl:variable name="targetNode" select="$concordance/index/text/ref[@id=$targetRef]"/>-->   
                        <!-- Key provides more constant performance. Some time is needed to build the index, though -->
                        <xsl:variable name="targetNode" select="key('concordance_key',$targetRef,$concordance)"/>                        
                        <xsl:variable name="parentText" select="$targetNode/parent::*"/>
                        <xsl:value-of select="concat('/',$parentText/@id, $targetNode/@target)"/>
                    </xsl:attribute>
                    <xsl:if test="tei:reg">
                        <xsl:attribute name="title">
                            <xsl:value-of select="normalize-space(tei:reg)"/>
                        </xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates select="tei:orig"/>
                    <!--<xsl:apply-templates/>-->
                </a>
                <!--<xsl:text> </xsl:text>-->
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="ref-identifier">
                    <xsl:text>Note</xsl:text>
                    <xsl:number count="tei:ref" level="any" from="tei:text" format="1"/>
                </xsl:variable>
                <span class="realnote" id="notelink{$ref-identifier}" onclick="toggle({$ref-identifier});">
                    <sup>
                        <a href="notelink{@target}">*</a>
                    </sup>
                </span>
                <span class="notecontents" id="{$ref-identifier}" style="display: none;">
                    <xsl:apply-templates/>
                    <xsl:apply-templates select="@target"/>
                </span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="refN">
        <xsl:number from="tei:text" level="any" format="1"/>
    </xsl:template>
    <xsl:template match="tei:orig">
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>