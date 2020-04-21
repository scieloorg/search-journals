# coding: utf-8
from lxml import etree as ET

import plumber
from citedby import client


CITEDBY = client.ThriftClient(domain='citedby.scielo.org:11610')

CITABLE_DOCUMENT_TYPES = (
    u'article-commentary',
    u'brief-report',
    u'case-report',
    u'rapid-communication',
    u'research-article',
    u'review-article'
)

CITATION_ALLOWED_TYPES = (
    u'article',
    u'book'
)


class SetupDocument(plumber.Pipe):

    def transform(self, data):
        xml = ET.Element('doc')

        return data, xml


class SubjectAreas(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.journal.subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        if len(raw.journal.subject_areas) > 2:

            field = ET.Element('field')
            field.text = 'multidisciplinary'
            field.set('name', 'subject_area')
            xml.find('.').append(field)

            return data


        for subject_area in raw.journal.subject_areas:
            field = ET.Element('field')
            field.text = subject_area
            field.set('name', 'subject_area')

            xml.find('.').append(field)

        return data


class Keywords(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.keywords():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for language, keywords in raw.keywords().items():
            for keyword in keywords:
                field = ET.Element('field')
                field.text = keyword
                field.set('name', 'keyword_%s' % language)

                xml.find('.').append(field)

        return data


class IsCitable(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = 'is_true' if raw.document_type in CITABLE_DOCUMENT_TYPES else 'is_false'
        field.set('name', 'is_citable')

        xml.find('.').append(field)

        return data


class JournalISSNs(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        issns = set()
        if raw.electronic_issn:
            issns.add(raw.journal.electronic_issn)

        if raw.print_issn:
            issns.add(raw.journal.print_issn)

        issns.add(raw.journal.scielo_issn)

        for issn in issns:
            field = ET.Element('field')
            field.text = issn
            field.set('name', 'issn')

            xml.find('.').append(field)

        return data


class DocumentID(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = '{0}-{1}'.format(raw.publisher_id, raw.collection_acronym)
        field.set('name', 'id')

        xml.find('.').append(field)

        return data


class Entity(plumber.Pipe):

    def __init__(self, name='document'):
        self.name = name

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = self.name
        field.set('name', 'entity')

        xml.find('.').append(field)

        return data


class JournalTitle(plumber.Pipe):

    def __init__(self, field_name='journal_title'):
        self.field_name = field_name

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.journal.title
        field.set('name', self.field_name)

        xml.find('.').append(field)

        return data


class Permission(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.permissions:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.permissions.get('id', '')
        field.set('name', 'use_license')
        xml.append(field)

        if raw.permissions.get('text', None):
            field = ET.Element('field')
            field.text = raw.permissions.get('text', '')
            field.set('name', 'use_license_text')
            xml.append(field)

        if raw.permissions.get('url', None):
            field = ET.Element('field')
            field.text = raw.permissions.get('url', '')
            field.set('name', 'use_license_uri')
            xml.append(field)

        return data


class Collection(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.collection_acronym
        field.set('name', 'in')

        xml.find('.').append(field)

        return data


class DocumentType(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.document_type
        field.set('name', 'type')

        xml.find('.').append(field)

        return data


class URL(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = '{0}'.format(raw.publisher_id)
        field.set('name', 'ur')

        xml.find('.').append(field)

        return data


class Authors(plumber.Pipe):

    def __init__(self, field_name='au'):
        self.field_name = field_name

    def precond(data):
        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for author in raw.authors:
            field = ET.Element('field')
            name = []

            if 'surname' in author:
                name.append(author['surname'])

            if 'given_names' in author:
                name.append(author['given_names'])

            field.text = ', '.join(name)

            field.set('name', self.field_name)
            xml.find('.').append(field)

        return data


class OriginalTitle(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_title():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.original_title()
        field.set('name', 'ti')
        xml.find('.').append(field)

        return data


class Titles(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_title() and not raw.translated_titles():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.original_title()
        field.set('name', 'ti_%s' % raw.original_language())
        xml.find('.').append(field)

        if not raw.translated_titles():
            return data

        for language, title in raw.translated_titles().items():
            field = ET.Element('field')
            field.text = title
            field.set('name', 'ti_%s' % language)
            xml.find('.').append(field)

        return data


class Pages(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.start_page and not raw.end_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        pages = []

        if raw.start_page:
            pages.append(raw.start_page)

        if raw.end_page:
            pages.append(raw.end_page)

        field = ET.Element('field')
        field.text = '-'.join(pages)
        field.set('name', 'pg')
        xml.find('.').append(field)

        return data


class DOI(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.doi:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.doi
        field.set('name', 'doi')
        xml.find('.').append(field)

        return data


class WOKCI(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.journal.wos_citation_indexes:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for index in raw.journal.wos_citation_indexes:
            field = ET.Element('field')
            field.text = index.replace('&', '')
            field.set('name', 'wok_citation_index')
            xml.find('.').append(field)

        return data


class WOKSC(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.journal.wos_subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for index in raw.journal.wos_subject_areas:
            field = ET.Element('field')
            field.text = index
            field.set('name', 'wok_subject_categories')
            xml.find('.').append(field)

        return data


class Volume(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue.volume:
            field = ET.Element('field')
            field.text = raw.issue.volume
            field.set('name', 'volume')
            xml.find('.').append(field)

        return data


class SupplementVolume(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue.supplement_volume:
            field = ET.Element('field')
            field.text = raw.issue.supplement_volume
            field.set('name', 'supplement_volume')
            xml.find('.').append(field)

        return data


class Issue(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue.number:
            field = ET.Element('field')
            field.text = raw.issue.number
            field.set('name', 'issue')
            xml.find('.').append(field)

        return data


class SupplementIssue(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue.supplement_number:
            field = ET.Element('field')
            field.text = raw.issue.supplement_number
            field.set('name', 'supplement_issue')
            xml.find('.').append(field)

        return data


class ElocationPage(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.elocation:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.elocation
        field.set('name', 'elocation')
        xml.find('.').append(field)

        return data


class StartPage(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.start_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.start_page
        field.set('name', 'start_page')
        xml.find('.').append(field)

        return data


class EndPage(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.end_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.end_page
        field.set('name', 'end_page')
        xml.find('.').append(field)

        return data


class JournalAbbrevTitle(plumber.Pipe):

    def __init__(self, field_name='ta'):
        self.field_name = field_name

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.journal.abbreviated_title
        field.set('name', self.field_name)
        xml.find('.').append(field)

        return data


class Languages(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        langs = set([i for i in raw.languages()])
        langs.add(raw.original_language())

        for language in langs:
            field = ET.Element('field')
            field.text = language
            field.set('name', 'la')
            xml.find('.').append(field)

        return data


class AvailableLanguages(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        langs = set([i for i in raw.languages()])
        langs.add(raw.original_language())

        if raw.translated_abstracts():
            for lang in raw.translated_abstracts().keys():
                langs.add(lang)

        for language in langs:
            field = ET.Element('field')
            field.text = language
            field.set('name', 'available_languages')
            xml.find('.').append(field)

        return data


class Fulltexts(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.fulltexts():
            raise plumber.UnmetPrecondition()

    def transform(self, data):
        raw, xml = data

        ft = raw.fulltexts()

        # There is articles that does not have pdf
        if 'pdf' in ft:
            for language, url in ft['pdf'].items():

                field = ET.Element('field')
                field.text = url
                field.set('name', 'fulltext_pdf_%s' % language)
                xml.find('.').append(field)

        if 'html' in ft:
            for language, url in ft['html'].items():

                field = ET.Element('field')
                field.text = url
                field.set('name', 'fulltext_html_%s' % language)
                xml.find('.').append(field)

        return data


class PublicationDate(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.publication_date
        field.set('name', 'da')
        xml.find('.').append(field)

        return data


class SciELOPublicationDate(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.creation_date
        field.set('name', 'scielo_publication_date')
        xml.find('.').append(field)

        return data


class ReceivedCitations(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        result = CITEDBY.citedby_pid(raw.publisher_id, metaonly=True, from_heap=False)
        if result:
            tr = result.get('article', {'total_received': 0})['total_received']

            field = ET.Element('field')
            field.text = str(tr)
            field.set('name', 'total_received')

            xml.find('.').append(field)

        return data


class SciELOProcessingDate(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.processing_date
        field.set('name', 'scielo_processing_date')
        xml.find('.').append(field)

        return data


class Abstract(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.original_abstract() and not raw.translated_abstracts():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        if raw.original_abstract():
            field = ET.Element('field')
            field.text = raw.original_abstract()
            field.set('name', 'ab_%s' % raw.original_language())
            xml.find('.').append(field)

        if not raw.translated_abstracts():
            return data

        for language, abstract in raw.translated_abstracts().items():
            field = ET.Element('field')
            field.text = abstract
            field.set('name', 'ab_%s' % language)
            xml.find('.').append(field)

        return data


class AffiliationCountry(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.mixed_affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        countries = set()

        for affiliation in raw.mixed_affiliations:
            if 'country' in affiliation:
                countries.add(affiliation['country'])

        for country in countries:
            field = ET.Element('field')
            field.text = country.strip()
            field.set('name', 'aff_country')
            xml.find('.').append(field)

        return data


class AffiliationInstitution(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.mixed_affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        institutions = set()

        for affiliation in raw.mixed_affiliations:
            if 'institution' in affiliation:
                institutions.add(affiliation['institution'])

        for institution in institutions:
            field = ET.Element('field')
            field.text = institution.strip()
            field.set('name', 'aff_institution')
            xml.find('.').append(field)

        return data


class Sponsor(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.project_sponsor:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        sponsors = set()

        for sponsor in raw.project_sponsor:
            if 'orgname' in sponsor:
                sponsors.add(sponsor['orgname'])

        for sponsor in sponsors:
            field = ET.Element('field')
            field.text = sponsor
            field.set('name', 'sponsor')
            xml.find('.').append(field)

        return data


class CitationFKAuthors(plumber.Pipe):
    """
    Adiciona nome dos autores das referências citadas.
    """

    def precond(data):
        raw, xml = data
        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for cit in raw.citations:
            if cit.publication_type in CITATION_ALLOWED_TYPES:
                for author in cit.authors:
                    field = ET.Element('field')
                    name = []

                    if 'surname' in author:
                        name.append(author['surname'])

                    if 'given_names' in author:
                        name.append(author['given_names'])

                    field.text = ', '.join(name)

                    field.set('name', 'citation_fk_au')

                    xml.find('.').append(field)

        return data


class CitationFKJournalsExternalData(plumber.Pipe):
    "Adiciona títulos extras e normalizados dos periódicos das referências citadas."

    def precond(data):
        raw, xml = data
        if not raw.citations:
            raise plumber.UnmetPrecondition()

    def __init__(self, external_metadata):
        self.external_metadata = external_metadata

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        collection_acronym = raw.collection_acronym

        for cit in raw.citations:
            if cit.publication_type in CITATION_ALLOWED_TYPES:
                cit_id = cit.data['v880'][0]['_']
                cit_full_id = '{0}-{1}'.format(cit_id, collection_acronym)

                citation = self.external_metadata.get(cit_full_id)
                if citation:
                    citation_type = citation.get('type')
                    if citation_type == 'journal-article':
                        for ct in citation.get('container-title', []):
                            field = ET.Element('field')
                            field.text = ct
                            field.set('name', 'citation_fk_ta')

                            xml.find('.').append(field)

        return data


class CitationFKJournals(plumber.Pipe):
    """
    Adiciona títulos dos periódicos das referências citadas.
    """

    def precond(data):
        raw, xml = data
        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for cit in raw.citations:
            if cit.publication_type == 'article':
                if cit.source:
                    field = ET.Element('field')
                    field.text = cit.source
                    field.set('name', 'citation_fk_ta')

                    xml.find('.').append(field)

        return data


class CitationFK(plumber.Pipe):
    """
    Adiciona ids das referências citadas.
    """

    def precond(data):
        raw, xml = data
        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        collection_acronym = raw.collection_acronym

        for cit in raw.citations:
            if cit.publication_type in CITATION_ALLOWED_TYPES:

                # publisher id + 0{0,4} + index number
                cit_id = cit.data['v880'][0]['_']

                field = ET.Element('field')
                field.text = '{0}-{1}'.format(cit_id, collection_acronym)
                field.set('name', 'citation_fk')

                xml.find('.').append(field)

        return data


class TearDown(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        return xml
