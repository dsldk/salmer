<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs tei" version="2.0">
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
		    <xsl:variable name="concordance" select="/db/apps/salmer/concordance.xml"/>
		    <a>
                   <xsl:attribute name="href">
                       <xsl:variable name="targetId" select="substring-after(@target,'#')"/>
                       <xsl:value-of select="concat($concordance/index/title[ref/@id=$targetId]/@id,$concordance/index/title/ref [@id=$targetId]/@target)"/>
                    </xsl:attribute>
                    <!-- TODO: Old code, remove when the new one works.
                    <xsl:attribute name="href">
                        <xsl:text>?ref=</xsl:text>
                        <xsl:value-of select="substring-after(@target,'#')"/>
		    </xsl:attribute>
                    -->
                    <xsl:if test="tei:reg">
                        <xsl:attribute name="title">
                            <xsl:value-of select="tei:reg"/>
                        </xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates select="tei:orig"/>
                    </a>
                <xsl:text> </xsl:text>
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
</xsl:stylesheet><!-- ancestor::tei:note[@place!=right] -->
