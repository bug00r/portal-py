import unittest
from lxml import etree
from io import StringIO, BytesIO
from bin.utils.xslt_.utils import prepareNS
import sys
from pathlib import Path

class TestXmlUtils(unittest.TestCase):
    """
        This test uses an xslt parameter as xml injection and tried to convert
        xml parameter string into node set and work on it.
    """

    def test_xslt_document_include_string(self):
        xml_root = """<r>
                        <a>
                            <b></b>
                        </a>
                        <c />
                        <d a="11" ><e /></d>
                        <d a="12" ><e /></d>
                       </r>
                    """
        xml_1 = etree.XSLT.strparam("""<r1><y1 /><y1 /><y1 /></r1>""")
        xml_2 = etree.XSLT.strparam("""<r2><x2 /><y2 /><y2 /></r2>""")
        xslt_temp = '''<xsl:stylesheet version="1.0" 
                                       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                       xmlns:exslt="http://exslt.org/common"
                                       xmlns:utils="http://bugsutils.de/">
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
                    
                       <xsl:template match="//e" >
                            <xsl:if test="../@a = '12'">
                                    <xsl:copy>
                                    <xsl:apply-templates select="@*|node()"/>
                                    <content>
                                        <item>Test1</item>
                                        <item>Test2</item>
                                        <item>Test3</item>
                                    </content>
                                </xsl:copy>
                            </xsl:if>
                       </xsl:template>

                    </xsl:stylesheet>'''
        prepareNS()
        xml_ = etree.XML(xml_root)
        try:
            xslt = etree.XSLT(etree.XML(xslt_temp))
            result = xslt(xml_, x1=xml_1, x2=xml_2, profile_run=True)
            print(etree.tostring(result, pretty_print=True).decode("utf-8"))
            print(etree.tostring(result.xslt_profile, pretty_print=True).decode("utf-8"))
        except:
            print(sys.exc_info()[1])
            print(xslt.error_log)
            for error in xslt.error_log:
                print(error.message, error.line)

    def test_hgen_xslt(self):

        xml_1 = etree.XSLT.strparam("""<r1><y1 /><y1 /><y1 /></r1>""")
        xml_2 = etree.XSLT.strparam("""<r2><x2 /><y2 /><y2 /></r2>""")

        hgen_xslt = Path(__file__).parent / "hgen_main.xslt"
        hgen_xrc = Path(__file__).parent / "hgen_main_ui.xrc"

        with open(hgen_xslt.__str__()) as _file:
            hgen_xslt_val = etree.parse(BytesIO(_file.read().encode()))

        with open(hgen_xrc.__str__()) as _file:
            hgen_xrc_val = etree.parse(BytesIO(_file.read().encode()))

        prepareNS()
        try:
            xslt = etree.XSLT(hgen_xslt_val)
            result = xslt(hgen_xrc_val, x1=xml_1, x2=xml_2, profile_run=True)
            print(etree.tostring(result, pretty_print=True).decode("utf-8"))
            print(etree.tostring(result.xslt_profile, pretty_print=True).decode("utf-8"))
        except:
            print(sys.exc_info()[1])
            print(xslt.error_log)
            for error in xslt.error_log:
                print(error.message, error.line)