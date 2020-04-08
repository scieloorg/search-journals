# coding: utf-8
import unittest
from lxml import etree as ET

import pipeline_xml


namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'xmlns': 'http://www.openarchives.org/OAI/2.0/',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
              'oai': 'http://www.openarchives.org/OAI/2.0/'}


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
                <oai_dc:dc
                    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:creator>Trentin,Robson Gonçalves</dc:creator>
                    <dc:creator>Modolo,Alcir José</dc:creator>
                    <dc:creator>Vargas,Thiago de Oliveira</dc:creator>
                    <dc:creator>Campos,José Ricardo da Rocha</dc:creator>
                    <dc:creator>Adami,Paulo Fernando</dc:creator>
                    <dc:creator>Baesso,Murilo Mesquita</dc:creator>
                </oai_dc:dc>
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


class TestTitles(unittest.TestCase):

    def test_transform(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
            <metadata>
                <oai_dc:dc
                    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:title xml:lang="en-US">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:title>
                    <dc:title xml:lang="es-ES">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:title>
                    <dc:title xml:lang="pt-BR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:title>
                    <dc:title xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:title>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Authors().transform(data)
        self.assertIsNone(xml.find(".//field[@name='ti_en']"))
        self.assertIsNone(xml.find(".//field[@name='ti_es']"))
        self.assertIsNone(xml.find(".//field[@name='ti_pt']"))
        self.assertIsNone(xml.find(".//field[@name='ti_fr']"))
