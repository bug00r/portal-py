import unittest
from portal_src.bin.utils.xml.resource import XmlResource, XmlDocument
from pathlib import Path


class TestXmlUtils(unittest.TestCase):

    def test_read_xml_success(self):
        path = Path(__file__).parent
        resource = XmlResource(path, "test")
        result = resource.xml()
        print("\nfound xml:")
        print(result)

    def test_read_xml_and_create_tree(self):
        path = Path(__file__).parent
        resource = XmlResource(path, "test")
        result = resource.xml()
        xmlDoc = XmlDocument(result)
        doc = xmlDoc.doc()
        print("\ndoc:")
        print(doc)
        result = doc.xpath('//blabla')
        for e in result:
            print(e.tag)