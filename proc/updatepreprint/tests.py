# coding: utf-8
import unittest
from lxml import etree as ET
import json
import os

import pipeline_xml


namespaces = {}
namespaces['dc'] = 'http://www.openarchives.org/OAI/2.0/provenance'

for namespace_id, namespace_link in namespaces.items():
    ET.register_namespace(namespace_id, namespace_link)


class UpdatePrePrintTests(unittest.TestCase):

    def setUp(self):
        pass


class TestAuthors(unittest.TestCase):


    def test_transform(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
        <metadata>
            <dc:creator>Trentin,Robson Gonçalves</dc:creator>
            <dc:creator>Modolo,Alcir José</dc:creator>
            <dc:creator>Vargas,Thiago de Oliveira</dc:creator>
            <dc:creator>Campos,José Ricardo da Rocha</dc:creator>
            <dc:creator>Adami,Paulo Fernando</dc:creator>
            <dc:creator>Baesso,Murilo Mesquita</dc:creator>
        </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Authors().transform(data)
        self.assertEqual(
            [
                "Trentin,Robson Gonçalves",
                "Modolo,Alcir José",
                "Vargas,Thiago de Oliveira",
                "Campos,José Ricardo da Rocha",
                "Adami,Paulo Fernando",
                "Baesso,Murilo Mesquita",
            ],
            [node.text for node in xml.findall(".//field[@name='au']")]
        )