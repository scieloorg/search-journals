# coding: utf-8
import unittest
import xml.etree.ElementTree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

import pipeline_xml


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_setuppipe_element_name(self):

        data = [self._article_meta, None]

        xmlarticle = pipeline_xml.SetupDocument()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<doc />', ET.tostring(xml))

    def test_xml_document_id_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.DocumentID()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="id"]').text

        self.assertEqual(u'S0034-89102010000400007-scl', result)

    def test_xml_document_collection_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Collection()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="in"]').text

        self.assertEqual(u'scl', result)

    def test_xml_document_knowledge_area_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.KnowledgeArea()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ac"]').text

        self.assertEqual(u'Health Sciences', result)

    def test_xml_document_doi_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}, 'doi': '10.1590/S0036-36342011000900009'})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.DOI()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="doi"]').text

        self.assertEqual(u'10.1590/S0036-36342011000900009', result)

    def test_xml_document_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.DOI()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="doi"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_knowledge_area_multiple_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v441': [{'_': 'Health Sciences'}, {'_': 'Human Sciences'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.KnowledgeArea()

        raw, xml = xmlarticle.transform(data)

        result = ', '.join([ac.text for ac in xml.findall('./field[@name="ac"]')])

        self.assertEqual(u'Health Sciences, Human Sciences', result)

    def test_xml_document_knowledge_area_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.KnowledgeArea()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ac"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_xml_document_type_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.DocumentType()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="type"]').text

        self.assertEqual(u'research-article', result)

    def test_xml_document_ur_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.URL()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ur"]').text

        self.assertEqual(u'S0034-89102010000400007', result)

    def test_xml_document_authors_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Authors()
        raw, xml = xmlarticle.transform(data)

        result = '; '.join([ac.text for ac in xml.findall('./field[@name="au"]')])

        self.assertEqual(u'Mariangela Leal, Cherchiglia; Elaine Leandro, Machado; Daniele Ara\xfajo Campo, Szuster; Eli Iola Gurgel, Andrade; Francisco de Assis, Ac\xfarcio; Waleska Teixeira, Caiaffa; Ricardo, Sesso; Augusto A, Guerra Junior; Odilon Vanni de, Queiroz; Isabel Cristina, Gomes', result)

    def test_xml_document_authors_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Authors()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="au"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_original_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.OriginalTitle()
        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ti"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_original_title_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.OriginalTitle()
        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ti"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_titles_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Titles()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ti_pt"]').text[0:20]
        self.assertEqual(u'Perfil epidemiológic', result)

        result = xml.find('./field[@name="ti_en"]').text[0:20]
        self.assertEqual(u'Epidemiological prof', result)

        result = xml.find('./field[@name="ti_es"]').text[0:20]
        self.assertEqual(u'Perfil epidemiológic', result)

    def test_xml_document_titles_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Titles()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ti"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_pages_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Pages()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="pg"]').text

        self.assertEqual(u'639-649', result)

    def test_xml_document_pages_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Pages()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="pg"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_wok_citation_index_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.WOKCI()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_citation_index"]')])

        self.assertEqual(u'SCIE, SSCI', result)

    def test_xml_document_wok_citation_index_AHCI_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v853': [{'_': 'A&HCI'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.WOKCI()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_citation_index"]')])

        self.assertEqual(u'AHCI', result)

    def test_xml_document_wok_citation_index_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.WOKCI()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="wok_citation_index"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_wok_subject_categories_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.WOKSC()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_subject_categories"]')])

        self.assertEqual(u'PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH', result)

    def test_xml_document_multiple_wok_subject_categories_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v854': [{'_': 'Cat 1'}, {'_': 'Cat 2'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.WOKSC()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_subject_categories"]')])

        self.assertEqual(u'Cat 1, Cat 2', result)

    def test_xml_document_wok_subject_categories_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('add')
        pxml.append(ET.Element('doc'))

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.WOKSC()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="wok_subject_categories"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_journal_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.JournalTitle()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="journal_title"]').text

        self.assertEqual(u'Revista de Saúde Pública', result)

    def test_xml_document_journal_abbrev_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.JournalAbbrevTitle()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ta"]').text

        self.assertEqual(u'Rev. Saúde Pública', result)

    def test_xml_document_available_languages_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.AvailableLanguages()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="la"]').text

        self.assertEqual(u'pt', result)

    def test_xml_document_available_languages_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.AvailableLanguages()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="la"]').text

        self.assertEqual(u'pt', result)

    def test_xml_document_fulltexts_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        self._article_meta.data['fulltexts'] = {
            'pdf': {
                'en': 'url_pdf_en',
            },
            'html': {
                'en': 'url_html_en',
            },
        }
        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Fulltexts()
        raw, xml = xmlarticle.transform(data)

        result_pdf = xml.find('./field[@name="fulltext_pdf_en"]').text
        result_html = xml.find('./field[@name="fulltext_html_en"]').text

        self.assertEqual(u'url_pdf_en', result_pdf)
        self.assertEqual(u'url_html_en', result_html)

    def test_xml_document_available_languages_plus_fulltexts_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        self._article_meta.data['fulltexts'] = {
            'pdf': {
                'en': 'url_pdf_en',
            },
            'html': {
                'en': 'url_html_en',
            },
        }
        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.AvailableLanguages()
        raw, xml = xmlarticle.transform(data)

        result = sorted([i.text for i in xml.findall('./field[@name="la"]')])

        self.assertEqual([u'en', u'pt'], result)

    def test_xml_document_publication_date_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.PublicationDate()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="da"]').text

        self.assertEqual(u'2010-08', result)

    def test_xml_document_abstract_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Abstract()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ab_pt"]').text[0:20]
        self.assertEqual(u'OBJETIVO: Descrever ', result)

        result = xml.find('./field[@name="ab_en"]').text[0:20]
        self.assertEqual(u'OBJECTIVE: To descri', result)

        result = xml.find('./field[@name="ab_es"]').text[0:20]
        self.assertEqual(u'OBJETIVO: Describir ', result)

    def test_xml_document_affiliation_country_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.AffiliationCountry()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="aff_country"]')]

        self.assertEqual(['BRAZIL'], result)

    def test_xml_document_affiliation_country_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.AffiliationCountry()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="aff_country"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_affiliation_institution_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.AffiliationInstitution()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="aff_institution"]')]

        self.assertEqual(
            sorted([u'Universidade Federal de Minas Gerais', u'Universidade Federal de São Paulo']),
            sorted(result)
        )

    def test_xml_document_affiliation_institution_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.AffiliationInstitution()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="aff_institution"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_sponsor_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Sponsor()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="sponsor"]')]

        self.assertEqual([u'Fundação de Amparo à Pesquisa do Estado de Minas Gerais', u'Ministério da Saúde', u'Conselho Nacional de Desenvolvimento Científico e Tecnológico'], result)

    def test_xml_document_sponsor_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Sponsor()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="sponsor"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_journal_title_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {"v100": [{"_": "Revista de Sa\u00fade P\u00fablica"}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.JournalTitle()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="journal"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_journal_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Journal()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="journal"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_volume_pipe(self):

        fakexylosearticle = Article({'article': {"v31": [{"_": "37"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Volume()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="volume"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_journal_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Volume()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="volune"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_supplement_volume_pipe(self):

        fakexylosearticle = Article({'article': {"v131": [{"_": "suppl. 2"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.SupplementVolume()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="supplement_volume"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_supplement_volume_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.SupplementVolume()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="supplement_volume"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_issue_pipe(self):

        fakexylosearticle = Article({'article': {"v32": [{"_": "23"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Issue()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="issue"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_issue_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.Issue()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="issue"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_supplement_issue_pipe(self):

        fakexylosearticle = Article({'article': {"v132": [{"_": "suppl. issue 3"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.SupplementIssue()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="supplement_issue"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_supplement_issue_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.SupplementIssue()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="supplement_issue"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_start_page_pipe(self):

        fakexylosearticle = Article({'article': {"v14": [{"l": "649", "_": "", "f": "639"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.StartPage()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="start_page"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_start_page_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.StartPage()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="start_page"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_end_page_pipe(self):

        fakexylosearticle = Article({'article': {"v14": [{"l": "649", "_": "", "f": "639"}]}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.EndPage()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="end_page"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_end_page_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.EndPage()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="end_page"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
