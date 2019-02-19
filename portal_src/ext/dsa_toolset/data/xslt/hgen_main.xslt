<xsl:stylesheet version="1.0"
                   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                   xmlns:exslt="http://exslt.org/common"
                   xmlns:utils="http://bugsutils.de/"
                   xmlns:xrc="http://www.wxwindows.org/wxxrc">
    <xsl:output method="xml" omit-xml-declaration="yes"/>


    <xsl:param name="x1" />
    <xsl:param name="x2" />

    <xsl:variable name="xml1" select="utils:strtodoc($x1)" />
    <xsl:variable name="xml2" select="utils:strtodoc($x2)" />

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="//xrc:content" >
        <xsl:if test="../@name = 'char_list'">
            <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                    <item>Test1</item>
                    <item>Test2</item>
                    <item>Test3</item>
            </xsl:copy>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>