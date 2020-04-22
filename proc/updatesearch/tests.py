# coding: utf-8
import unittest
import xml.etree.ElementTree as ET
import json
import os

import plumber
from lxml import etree
from xylose.scielodocument import Article

import pipeline_xml
import updatesearch


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())

        self._article_meta = Article(self._raw_json)

    def test_xml_document_permission_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Permission()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="use_license"]').text
        result1 = xml.find('./field[@name="use_license_text"]').text
        result2 = xml.find('./field[@name="use_license_uri"]').text
        self.assertEqual(u'by-nc/4.0', result)
        self.assertEqual(u'This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.', result1)
        self.assertEqual(u'http://creativecommons.org/licenses/by-nc/4.0/', result2)

    def test_subject_areas(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.SubjectAreas()

        raw, xml = xmlarticle.transform(data)

        result = sorted([i.text for i in xml.findall('./field[@name="subject_area"]')])

        self.assertEqual([u'Health Sciences'], result)

    def test_without_subject_areas(self):

        pxml = ET.Element('doc')

        del(self._article_meta.data['title']['v441'])

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.SubjectAreas()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="subject_area"]')

        self.assertEqual(None, result)

    def test_keywords(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Keywords()

        raw, xml = xmlarticle.transform(data)

        result = sorted([i.text for i in xml.findall('./field[@name="keyword_pt"]')])

        self.assertEqual([u'Insuficiência Renal Crônica', u'Registros de Mortalidade', u'Sistemas de Informação Hospitalar', u'Terapia de Substituição Renal'], result)

    def test_without_keywords(self):

        pxml = ET.Element('doc')

        del(self._article_meta.data['article']['v85'])
        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.Keywords()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="keyword_pt"]')

        self.assertEqual(None, result)

    def test_setuppipe_element_name(self):

        data = [self._article_meta, None]

        xmlarticle = pipeline_xml.SetupDocument()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<doc />', ET.tostring(xml))

    def test_is_citable_false(self):

        pxml = ET.Element('doc')

        self._article_meta.data['article']['v71'] = [{'_': 'xx'}]
        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.IsCitable()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="is_citable"]').text

        self.assertEqual('is_false', result)

    def test_is_citable_true(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.IsCitable()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="is_citable"]').text

        self.assertEqual('is_true', result)

    def test_xmljournalissn(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.JournalISSNs()

        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="issn"]')]

        self.assertEqual(['0034-8910'], result)

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

        self.assertEqual(u'Cherchiglia, Mariangela Leal; Machado, Elaine Leandro; Szuster, Daniele Araújo Campo; Andrade, Eli Iola Gurgel; Acúrcio, Francisco de Assis; Caiaffa, Waleska Teixeira; Sesso, Ricardo; Guerra Junior, Augusto A; Queiroz, Odilon Vanni de; Gomes, Isabel Cristina', result)

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

        result = xml.findall('./field[@name="available_languages"]')

        self.assertEqual(['en', 'es', 'pt'], sorted([i.text for i in result]))

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

        result = sorted([i.text for i in xml.findall('./field[@name="available_languages"]')])

        self.assertEqual([u'en', u'es', u'pt'], result)

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

    def test_xml_volume_pipe(self):

        self._article_meta.data['issue']['issue'] = {"v31": [{"_": "37"}]}

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

    def test_xml_supplement_volume_pipe(self):

        self._article_meta.data['issue']['issue'] = {"v131": [{"_": "suppl. 2"}]}

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

        del(self._article_meta.data['issue']['issue']['v31'])

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

        del(self._article_meta.data['issue']['issue']['v32'])

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

        self._article_meta.data['issue']['issue'] = {"v132": [{"_": "suppl. issue 3"}]}

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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


        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

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

    def test_xml_citation_fk(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.CitationFK()
        raw, xml = xmlarticle.transform(data)

        expected_results = ['S0034-8910201000040000700001-scl','S0034-8910201000040000700002-scl','S0034-8910201000040000700003-scl','S0034-8910201000040000700004-scl','S0034-8910201000040000700005-scl','S0034-8910201000040000700006-scl','S0034-8910201000040000700007-scl','S0034-8910201000040000700008-scl','S0034-8910201000040000700009-scl','S0034-8910201000040000700010-scl','S0034-8910201000040000700011-scl','S0034-8910201000040000700012-scl','S0034-8910201000040000700013-scl','S0034-8910201000040000700014-scl','S0034-8910201000040000700015-scl','S0034-8910201000040000700016-scl','S0034-8910201000040000700017-scl','S0034-8910201000040000700018-scl','S0034-8910201000040000700019-scl','S0034-8910201000040000700020-scl','S0034-8910201000040000700021-scl','S0034-8910201000040000700022-scl','S0034-8910201000040000700023-scl']
        obtained_results = [x.text for x in xml.findall('./field[@name="citation_fk"]')]

        self.assertItemsEqual(expected_results, obtained_results)

    def test_xml_citation_fk_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.CitationFK()

        raw, xml = xmlarticle.transform(data)

        self.assertIsNone(xml.find('./field[name="citation_fk"]'))

    def test_xml_citation_fk_authors(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.CitationFKAuthors()
        raw, xml = xmlarticle.transform(data)

        expected_results = ['Bamgboye, EL','Bastos, MG','Carmo, WB','Abrita, RR','Almeida, EC','Mafra, D','Costa, DMN','Bello, AK','Nwankwo, E','El Nahas, AM','Bommer, J','Cherchiglia, ML','Guerra Jr, AA','Andrade, EIG','Machado, CJ','Ac\xc3\xbarcio, FA','Meira Jr, W','Cusumano, A','Garcia-Garcia, G','Di Gioia, C','Hermida, O','Lavorato, C','Carre\xc3\xb1o, CA','Grassmann, A','Gioberge, S','Moeller, S','Brown, G','Inrig, JK','Sun, JL','Yang, Q','Briley, LP','Szczech, LA','Jaar, BG','Coresh, J','Plantinga, LC','Fink, NE','Klag, MJ','Levey, AS','Mazzuchi, N','Fernandez-Cean, JM','Carbonell, E','Moura, L','Schmidt, MI','Duncan, BB','Rosa, RS','Malta, DC','Stevens, A','Oliveira, MB','Rom\xc3\xa3o Jr, JE','Zatz, R','Oniscu, GC','Schalkwijk, AA','Johnson, RJ','Brown, H','Forsythe, JL','Pisoni, RL','Young, EW','Dykstra, DM','Greenwood, RN','Hecking, E','Gillespie, B','Queiroz, OV','Guerra Jr, AA','Machado, CJ','Andrade, EIG','Meira Jr, W','Ac\xc3\xbarcio, FA','CG, Rabbat','KE, Thorpe','JD, Russell','DN, Churchill','Ravanan, R','Udayaraj, U','Bakran, A','Steenkamp, R','Williams, AJ','Ansell, D','Sesso, R','Lopes, AA','Thom\xc3\xa9, FS','Bevilacqua J, L','Rom\xc3\xa3o, JEJ','Lugon, J','Stack, AG','Stengel, B','Billon, S','Van Dijk, PC','Jager, KJ','Dekker, FW','Simpson, K','Travassos, C','Oliveira, EXG','Viacava, F','Vonesh, EF','Snyder, JJ','Foley, RN','Collins, AJ']
        obtained_results = [x.text.encode('utf-8') for x in xml.findall('./field[@name="citation_fk_au"]')]

        self.assertItemsEqual(expected_results, obtained_results)

    def test_xml_citation_fk_authors_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.CitationFKAuthors()

        raw, xml = xmlarticle.transform(data)

        self.assertIsNone(xml.find('./field[name="citation_fk_au"]'))

    def test_xml_citation_fk_journals(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.CitationFKJournals()
        raw, xml = xmlarticle.transform(data)

        expected_results = ['Ethn Dis.','J Bras Nefrol','Kidney Int Suppl.','Nephrol Dial Transplant.','Rev Bras Estud Pop','Ren Fail','Nephrol Dial Transplant.','Clin J Am Soc Nephrol.','Ann Intern Med.','Kidney Int Suppl.','Epidemiol Serv Saude.','Kidney Int Suppl.','BMJ','Kidney Int.','Epidemiol Serv Saude.','J Am Soc Nephrol','Nephrol Dial Transplant.','J Bras Nefrol.','J Am Soc Nephrol.','Nephrol Dial Transplant.','Cienc Saude Coletiva.','Kidney Int Suppl.']
        obtained_results = [x.text for x in xml.findall('./field[@name="citation_fk_ta"]')]

        self.assertItemsEqual(expected_results, obtained_results)

    def test_xml_citation_fk_journals_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = pipeline_xml.CitationFKJournals()

        raw, xml = xmlarticle.transform(data)

        self.assertIsNone(xml.find('./field[name="citation_fk_ta"]'))

    def test_xml_citation_fk_journals_external_data(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = pipeline_xml.CitationFKJournalsExternalData({})
        raw, xml = xmlarticle.transform(data)

        expected_results = []
        obtained_results = [x.text for x in xml.findall('./field[@name="citation_fk_ta"]')]

        self.assertItemsEqual(expected_results, obtained_results)

    def test_add_fields_to_doc(self):
        # É preciso setar a variável de ambiente SOLR_URL=http://127.0.0.1/solr
        us = updatesearch.UpdateSearch()

        ppl = plumber.Pipeline(
            pipeline_xml.SetupDocument(),
            pipeline_xml.DocumentID(),
            pipeline_xml.Entity(name='document'),
            pipeline_xml.DOI(),
            pipeline_xml.Collection(),
            pipeline_xml.DocumentType(),
            pipeline_xml.URL()
        )

        obtained_doc = ET.Element('testAddFieldsToDoc')
        pipeline_results = ppl.run([self._article_meta])

        us.add_fields_to_doc(pipeline_results, obtained_doc)

        expected_doc = '<testAddFieldsToDoc><field name="id">S0034-89102010000400007-scl</field><field ' \
                       'name="entity">document</field><field name="doi">10.1590/S0034-89102010000400007</field><field ' \
                       'name="in">scl</field><field name="type">research-article</field><field ' \
                       'name="ur">S0034-89102010000400007</field></testAddFieldsToDoc>'

        self.assertEqual(ET.tostring(obtained_doc), expected_doc)
