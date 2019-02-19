from lxml import etree


def xpath_strtodoc(_, arg):
    """
        This function was used as xslt namespace extension for xslt parsing.
        It transformas a given xml string into xml document for xslt/xpath function
        usage inside of anther xslt.

        Usage inside of XSLT:

                      <xsl:stylesheet version="1.0"  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                       xmlns:exslt="http://exslt.org/common"
                                       xmlns:utils="http://bugsutils.de/">
                      <xsl:output method="xml" omit-xml-declaration="yes"/>


                      <xsl:param name="x1" />
                      <xsl:param name="x2" />

                      <xsl:variable name="xml1" select="utils:strtodoc($x1)" />
                      <xsl:variable name="xml2" select="utils:strtodoc($x2)" />

                      <xsl:template match="/">
                            <root>
                                <x1fromxslt>
                                    <xsl:for-each select="$xml1//*">
                                        <node><xsl:value-of select="name()" /></node>
                                    </xsl:for-each>
                                    <xsl:value-of disable-output-escaping="yes" select="$x1" />
                                </x1fromxslt>
                                <x2fromxslt>
                                    <xsl:for-each select="$xml2//*">
                                        <node><xsl:value-of select="name()" /> </node>
                                    </xsl:for-each>
                                    <xsl:value-of disable-output-escaping="yes" select="$x2" />
                                </x2fromxslt>
                            </root>
                      </xsl:template>

                    </xsl:stylesheet>

        :return: etree.XML
    """
    return etree.XML(arg)


def prepareNS():
    """
        This function will register additional namespaces. You must only call it once, but it has no effect if you do
        it more.

        :return: None
    """
    ns = etree.FunctionNamespace('http://bugsutils.de/')
    ns['strtodoc'] = xpath_strtodoc
    ns = etree.FunctionNamespace('http://www.wxwindows.org/wxxrc')
