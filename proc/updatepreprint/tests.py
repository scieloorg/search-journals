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


# <field name="id">art-S0102-695X2015000100053-scl</field>
class TestDocumentID(unittest.TestCase):

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
                    <dc:identifier>https://preprints.scielo.org/index.php/scielo/preprint/view/7</dc:identifier>
                    <dc:identifier>10.1590/scielopreprints.7</dc:identifier>OK
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.DocumentID().transform(data)
        self.assertEqual(xml.find(".//field[@name='id']").text, '10.1590/scielopreprints.7')


# <field name="ur">art-S1980-993X2015000200234</field>
class TestURL(unittest.TestCase):

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
                    <dc:identifier>https://preprints.scielo.org/index.php/scielo/preprint/view/7</dc:identifier>
                    <dc:identifier>10.1590/scielopreprints.7</dc:identifier>OK
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.URL().transform(data)
        self.assertEqual(
            xml.find(".//field[@name='ur']").text,
            "https://preprints.scielo.org/index.php/scielo/preprint/view/7"
        )


# <field name="au">Marcelo dos Santos, Targa</field>
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


# <field name="ti_*">Benefits and legacy of the water crisis in Brazil</field>
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


# <field name="doi">10.1590/S0102-67202014000200011</field>
class TestDOI(unittest.TestCase):

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
                    <dc:identifier>https://preprints.scielo.org/index.php/scielo/preprint/view/7</dc:identifier>
                    <dc:identifier>10.1590/scielopreprints.7</dc:identifier>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.DOI().transform(data)
        self.assertEqual(
            xml.find(".//field[@name='doi']").text,
            '10.1590/scielopreprints.7')


# <field name="la">en</field>
class TestLanguages(unittest.TestCase):

    def test_transform_returns_pt(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
            <metadata>
                <oai_dc:dc
                    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:language>por</dc:language>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Languages().transform(data)
        self.assertEqual(xml.find(".//field[@name='la']").text, "pt")

    def test_transform_returns_en(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
            <metadata>
                <oai_dc:dc
                    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:language>eng</dc:language>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Languages().transform(data)
        self.assertEqual(xml.find(".//field[@name='la']").text, "en")

    def test_transform_returns_es(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
            <metadata>
                <oai_dc:dc
                    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                    xmlns:dc="http://purl.org/dc/elements/1.1/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
                    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                    <dc:language>spa</dc:language>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Languages().transform(data)
        self.assertEqual(xml.find(".//field[@name='la']").text, "es")


# <field name="fulltext_pdf_pt">http://www.scielo.br/pdf/ambiagua/v10n2/1980-993X-ambiagua-10-02-00234.pdf</field>
# <field name="fulltext_pdf_pt">http://www.scielo.br/scielo.php?script=sci_abstract&pid=S0102-67202014000200138&lng=en&nrm=iso&tlng=pt</field>
class TestFulltexts(unittest.TestCase):

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
                    <dc:identifier>https://preprints.scielo.org/index.php/scielo/preprint/view/7</dc:identifier>
                    <dc:identifier>10.1590/scielopreprints.7</dc:identifier>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Fulltexts().transform(data)

        self.assertEqual(
            xml.find(".//field[@name='fulltext_html_en']").text,
            'https://preprints.scielo.org/index.php/scielo/preprint/view/7')


# <field name="da">2015-06</field>
class TestPublicationDate(unittest.TestCase):

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
                    <dc:date>2020-03-20</dc:date>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.PublicationDate().transform(data)
        self.assertEqual(xml.find(".//field[@name='da']").text, "2020-03-20")


# <field name="ab_*">In this editorial, we reflect on the benefits and legacy of the water crisis....</field>
class TestAbstract(unittest.TestCase):

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
                    <dc:description xml:lang="es-ES">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:description>
                    <dc:description xml:lang="pt-BR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:description>
                    <dc:description xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:description>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Abstract().transform(data)

        self.assertIsNotNone(xml.find(".//field[@name='ab_es']"))
        self.assertIsNotNone(xml.find(".//field[@name='ab_pt']"))
        self.assertIsNotNone(xml.find(".//field[@name='ab_fr']"))


# <field name="keyword_*"></field>
class TestKeywords(unittest.TestCase):

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
                    <dc:subject xml:lang="es-ES">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="es-ES">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="pt-BR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="es-ES">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="pt-BR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                    <dc:subject xml:lang="fr-FR">COVID-19 in Brazil: advantages of a socialized unified health system and preparation to contain cases</dc:subject>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Keywords().transform(data)
        self.assertEqual(3, len(xml.findall(".//field[@name='keyword_es']")))
        self.assertEqual(2, len(xml.findall(".//field[@name='keyword_pt']")))
        self.assertEqual(4, len(xml.findall(".//field[@name='keyword_fr']")))


# <field name="is_citable">is_true</field>
class TestIsCitable(unittest.TestCase):
    def test_transform(self):
        text = """<root xmlns:dc="http://www.openarchives.org/OAI/2.0/provenance">
        <record>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.IsCitable().transform(data)
        self.assertEqual("is_true", xml.find(".//field[@name='is_citable']").text)


# <field name="use_license"></field>
# <field name="use_license_text"></field>
# <field name="use_license_uri"></field>
class TestPermission(unittest.TestCase):
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
                    <dc:rights xml:lang="pt-BR">Copyright (c) 2020 Julio Croda, Wanderson Kleber de  Oliveira, Rodrigo Lins  Frutuoso, Luiz Henrique  Mandetta, Djane Clarys  Baia-da-Silva, José Diego  Brito-Sousa, Wuelton Marcelo  Monteiro, Marcus Vinícius Guimarães  Lacerda</dc:rights>
                    <dc:rights xml:lang="pt-BR">https://creativecommons.org/licenses/by/4.0</dc:rights>
                </oai_dc:dc>
            </metadata>
        </record>
        </root>
        """
        xml = ET.Element("doc")
        raw = ET.fromstring(text)
        data = raw, xml
        raw, xml = pipeline_xml.Permission().transform(data)
        self.assertEqual(
            xml.find(".//field[@name='use_license']").text,
            "https://creativecommons.org/licenses/by/4.0"
        )
        self.assertEqual(
            xml.find(".//field[@name='use_license_text']").text,
            "Copyright (c) 2020 Julio Croda, Wanderson Kleber de  Oliveira, Rodrigo Lins  Frutuoso, Luiz Henrique  Mandetta, Djane Clarys  Baia-da-Silva, José Diego  Brito-Sousa, Wuelton Marcelo  Monteiro, Marcus Vinícius Guimarães  Lacerda",
        )
        self.assertEqual(
            xml.find(".//field[@name='use_license_uri']").text,
            "https://creativecommons.org/licenses/by/4.0"
        )
