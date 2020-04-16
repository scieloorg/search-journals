# coding: utf-8
from lxml import etree as ET
from sanity_checker import SanityChecker as sc

import plumber


class AnalyticAuthors(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.analytic_authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for author in raw.analytic_authors:
            field = ET.Element('field')
            name = []

            if 'surname' in author:
                name.append(author['surname'])

            if 'given_names' in author:
                name.append(author['given_names'])

            fullname = ', '.join(name)
            while fullname.endswith('.'):
                fullname = fullname[:-1]

            if fullname:
                field.text = fullname
                field.set('name', 'cit_ana_au')
                xml.find('.').append(field)

        return data


class Authors(plumber.Pipe):

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

            fullname = ', '.join(name)

            while fullname.endswith('.'):
                fullname = fullname[:-1]

            if fullname:
                field.text = fullname
                field.set('name', 'au')
                xml.find('.').append(field)

                sanity_level = sc.check_author_name(fullname)

                if sanity_level:
                    field = ET.Element('field')
                    field.text = str(sanity_level)
                    field.set('name', 'cit_au_quality_level')

                    xml.find('.').append(field)

        return data


class ExternalData(plumber.Pipe):

    def __init__(self, external_data, collection_acronym=None):
        self.external_data = external_data
        self.collection_acronym = collection_acronym

    def transform(self, data):
        raw, xml = data

        cit_id = raw.data['v880'][0]['_']

        if 'v992' in raw.data:
            collection = raw.data['v992'][0]['_']
        else:
            collection = self.collection_acronym

        cit_full_id = '{0}-{1}'.format(cit_id, collection)
        cit_metadata = self.external_data.get(cit_full_id, {'type': None})

        if cit_metadata['type'] == 'journal-article':
            was_normalized = False
            if 'container-title' in cit_metadata:
                first_journal_title = cit_metadata['container-title'][0]
                if first_journal_title:
                    field = ET.Element('field')
                    field.text = first_journal_title
                    field.set('name', 'cit_journal_title_canonical')

                    xml.find('.').append(field)

                    was_normalized = True

            if 'ISSN' in cit_metadata:
                for i in cit_metadata['ISSN']:
                    if i:
                        field = ET.Element('field')
                        field.text = i
                        field.set('name', 'cit_journal_issn_canonical')

                        xml.find('.').append(field)

                        was_normalized = True

            if 'BC1-ISSNS' in cit_metadata:
                for i in cit_metadata['BC1-ISSNS']:
                    if i:
                        field = ET.Element('field')
                        field.text = i
                        field.set('name', 'cit_journal_issn_normalized')

                        xml.find('.').append(field)

                        was_normalized = True

            if 'BC1-JOURNAL-TITLES' in cit_metadata:
                for i in cit_metadata['BC1-JOURNAL-TITLES']:
                    field = ET.Element('field')
                    field.text = i
                    field.set('name', 'cit_journal_title_normalized')

                    xml.find('.').append(field)

                    was_normalized = True

            if was_normalized:
                normalization_status = cit_metadata['normalization-status']

                field = ET.Element('field')
                field.text = normalization_status
                field.set('name', 'cit_normalization_status')

                xml.find('.').append(field)

        return data


class ChapterTitle(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.chapter_title:
            chapter_title = raw.chapter_title
            while chapter_title.endswith('.'):
                chapter_title = chapter_title[:-1]

            if chapter_title:
                field = ET.Element('field')
                field.text = chapter_title
                field.set('name', 'ti')

                xml.find('.').append(field)

                field = ET.Element('field')
                field.text = chapter_title
                field.set('name', 'cit_chapter_title')

                xml.find('.').append(field)

        return data


class Collection(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if 'v992' not in raw.data:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        collection = raw.data['v992'][0]['_']

        field = ET.Element('field')
        field.text = collection
        field.set('name', 'in')

        xml.find('.').append(field)

        return data


class DocumentFK(plumber.Pipe):

    def __init__(self, collection_acronym=None):
        self.collection_acronym = collection_acronym

    def precond(data):

        raw, xml = data

        if 'v880' not in raw.data:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')

        # Ignores the last five numbers; these are for reference ids
        cit_id = raw.data['v880'][0]['_'][:-5]

        if 'v992' in raw.data:
            collection = raw.data['v992'][0]['_']
        else:
            collection = self.collection_acronym

        if cit_id:
            field.text = '{0}-{1}'.format(cit_id, collection)
            field.set('name', 'document_fk')

            xml.find('.').append(field)

        return data


class DocumentID(plumber.Pipe):

    def __init__(self, collection_acronym=None):
        self.collection_acronym = collection_acronym

    def transform(self, data):
        raw, xml = data

        cit_id = raw.data['v880'][0]['_']

        if 'v992' in raw.data:
            collection = raw.data['v992'][0]['_']
        else:
            collection = self.collection_acronym

        field = ET.Element('field')
        field.text = '{0}-{1}'.format(cit_id, collection)
        field.set('name', 'id')

        xml.find('.').append(field)

        return data


class DOI(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.doi:
            field = ET.Element('field')
            field.text = raw.doi
            field.set('name', 'doi')

            xml.find('.').append(field)

        return data


class Edition(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.edition:
            field = ET.Element('field')
            field.text = raw.edition
            field.set('name', 'cit_edition')

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


class Entity(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = 'citation'
        field.set('name', 'entity')

        xml.find('.').append(field)

        return data


class IndexNumber(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = str(raw.index_number)
        field.set('name', 'cit_index_number')

        xml.find('.').append(field)

        return data


class Institutions(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.institutions:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for institution in raw.institutions:
            inst = institution
            while inst.endswith('.'):
                inst = inst[:-1]

            if inst:
                field = ET.Element('field')
                field.text = inst
                field.set('name', 'cit_inst')

                xml.find('.').append(field)

        return data


class ISBN(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.isbn:
            field = ET.Element('field')
            field.text = raw.isbn
            field.set('name', 'cit_isbn')

            xml.find('.').append(field)

        return data


class ISSN(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issn:
            field = ET.Element('field')
            field.text = raw.issn
            field.set('name', 'cit_issn')

            xml.find('.').append(field)

        return data


class Issue(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue:
            field = ET.Element('field')
            field.text = raw.issue
            field.set('name', 'issue')

            xml.find('.').append(field)

        return data


class MonographicAuthors(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.monographic_authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for author in raw.monographic_authors:
            field = ET.Element('field')
            name = []

            if 'surname' in author:
                name.append(author['surname'])

            if 'given_names' in author:
                name.append(author['given_names'])

            fullname = ', '.join(name)

            while fullname.endswith('.'):
                fullname = fullname[:-1]

            if fullname:
                field.text = fullname
                field.set('name', 'cit_mon_au')
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


class PublicationDate(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.publication_date
        field.set('name', 'da')

        xml.find('.').append(field)

        sanity_level = sc.check_date(raw.publication_date)

        if sanity_level:
            field = ET.Element('field')
            field.text = str(sanity_level)
            field.set('name', 'cit_da_quality_level')

            xml.find('.').append(field)

        return data


class PublicationType(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.publication_type
        field.set('name', 'cit_type')

        xml.find('.').append(field)

        return data


class Publisher(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.publisher:

            publisher = raw.publisher
            while publisher.endswith('.'):
                publisher = publisher[:-1]

            if publisher:
                field = ET.Element('field')
                field.text = publisher
                field.set('name', 'cit_publisher')

                xml.find('.').append(field)

        return data


class PublisherAddress(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.publisher_address:
            publisher_address = raw.publisher_address
            while publisher_address.endswith('.'):
                publisher_address = publisher_address[:-1]

            if publisher_address:
                field = ET.Element('field')
                field.text = raw.publisher_address
                field.set('name', 'cit_publisher_address')

                xml.find('.').append(field)

        return data


class Serie(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.serie:
            field = ET.Element('field')
            field.text = raw.serie
            field.set('name', 'cit_serie')
            xml.find('.').append(field)

        return data


class SetupDocument(plumber.Pipe):

    def transform(self, data):
        xml = ET.Element('doc')

        return data, xml


class Source(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.source:
            source = raw.source
            while source.endswith('.'):
                source = source[:-1]

            if source:
                field = ET.Element('field')
                field.text = source
                if raw.publication_type == 'article':
                    field.set('name', 'cit_journal_title')
                else:
                    field.set('name', 'cit_source')

                xml.find('.').append(field)

                if raw.publication_type == 'book' and source:
                    field = ET.Element('field')
                    field.text = source
                    field.set('name', 'ti')

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


class TearDown(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        return xml


class Title(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        cit_title = raw.title()

        while cit_title.endswith('.'):
            cit_title = cit_title[:-1]

        if cit_title:
            field = ET.Element('field')
            field.text = cit_title
            field.set('name', 'ti')

            xml.find('.').append(field)

        return data


class Volume(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.volume:
            field = ET.Element('field')
            field.text = raw.volume
            field.set('name', 'volume')

            xml.find('.').append(field)

        return data
