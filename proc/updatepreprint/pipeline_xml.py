# coding: utf-8
from lxml import etree as ET

import plumber

from langcodes import standardize_tag

"""
Full example output of this pipeline:

    <doc>
        <field name="id">art-S0102-695X2015000100053-scl</field>
        <field name="journal_title">Revista Ambiente & Água</field>
        <field name="in">scl</field>
        <field name="ac">Agricultural Sciences</field>
        <field name="type">editorial</field>
        <field name="ur">art-S1980-993X2015000200234</field>
        <field name="au">Marcelo dos Santos, Targa</field>
        <field name="ti_*">Benefits and legacy of the water crisis in Brazil</field>
        <field name="pg">234-239</field>
        <field name="doi">10.1590/S0102-67202014000200011</field>
        <field name="wok_citation_index">SCIE</field>
        <field name="volume">48</field>
        <field name="supplement_volume">48</field>
        <field name="issue">7</field>
        <field name="supplement_issue">suppl. 2</field>
        <field name="start_page">216</field>
        <field name="end_page">218</field>
        <field name="ta">Rev. Ambient. Água</field>
        <field name="la">en</field>
        <field name="fulltext_pdf_pt">http://www.scielo.br/pdf/ambiagua/v10n2/1980-993X-ambiagua-10-02-00234.pdf</field>
        <field name="fulltext_pdf_pt">http://www.scielo.br/scielo.php?script=sci_abstract&pid=S0102-67202014000200138&lng=en&nrm=iso&tlng=pt</field>
        <field name="da">2015-06</field>
        <field name="ab_*">In this editorial, we reflect on the benefits and legacy of the water crisis....</field>
        <field name="aff_country">Brasil</field>
        <field name="aff_institution">usp</field>
        <field name="sponsor">CNPQ</field>
    </doc>
"""

ns = {'dc': 'http://purl.org/dc/elements/1.1/',
      'xmlns': 'http://www.openarchives.org/OAI/2.0/',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      'oai': 'http://www.openarchives.org/OAI/2.0/'}


class SetupDocument(plumber.Pipe):

    def transform(self, data):
        xml = ET.Element('doc')

        return data, xml


# <field name="id">art-S0102-695X2015000100053-scl</field>
class DocumentID(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:identifier"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:identifier"
        raw, xml = data

        for identifier in raw.findall(xpath, namespaces=ns):
            if not identifier.text.startswith('http'):
                field = ET.Element('field')
                field.text = identifier.text
                field.set('name', 'id')
                xml.find('.').append(field)

        return data


# <field name="ur" type="string" indexed="false" stored="true" multiValued="true"/>
class URL(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:identifier"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:identifier"
        raw, xml = data

        for url in raw.findall(xpath, namespaces=ns):
            if url.text.startswith('http'):
                field = ET.Element('field')
                field.text = url.text
                field.set('name', 'ur')
                xml.find('.').append(field)

        return data


# <field name="doi">10.1590/S0102-67202014000200011</field>
class DOI(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:identifier"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:identifier"
        raw, xml = data

        for doi in raw.findall(xpath, namespaces=ns):
            if not doi.text.startswith('http'):
                field = ET.Element('field')
                field.text = doi.text
                field.set('name', 'doi')
                xml.find('.').append(field)

        return data


class Languages(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:language"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:language"
        raw, xml = data

        for lang in raw.findall(xpath, namespaces=ns):
            field = ET.Element('field')

            field.text = standardize_tag(lang.text)
            field.set('name', 'la')
            xml.find('.').append(field)

        return data


# <field name="fulltext_pdf_pt">http://www.scielo.br/pdf/ambiagua/v10n2/1980-993X-ambiagua-10-02-00234.pdf</field>
class Fulltexts(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:identifier"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:identifier"
        raw, xml = data

        for url in raw.findall(xpath, namespaces=ns):
            if url.text.startswith('http'):
                for lang in raw.findall(".//dc:language", namespaces=ns):
                    field = ET.Element('field')
                    field.text = url.text
                    field.set('name', 'fulltext_html_%s' % standardize_tag(lang.text))
                    xml.find('.').append(field)
        return data


# <field name="da" type="string" indexed="true" stored="true" multiValued="false"/>
class PublicationDate(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:date"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        xpath = ".//dc:date"
        raw, xml = data

        for date in raw.findall(xpath, namespaces=ns):
            field = ET.Element('field')
            field.text = date.text
            field.set('name', 'da')
            xml.find('.').append(field)
        return data


# <field name="ab" type="text" indexed="true" stored="false" multiValued="true"/>
class Abstract(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:description"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        xpath = ".//dc:description"

        for item in raw.findall(xpath, namespaces=ns):
            lang = item.get('{http://www.w3.org/XML/1998/namespace}lang')
            if "-" in lang:
                lang = lang.split("-")[0]
            field = ET.Element('field')
            field.text = item.text
            field.set('name', 'ab_{}'.format(lang))
            xml.find('.').append(field)
        return data


# <dynamicField name="keyword_*"  type="text" indexed="false" stored="true"  multiValued="true"/>
class Keywords(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:subject"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        xpath = ".//dc:subject"

        for item in raw.findall(xpath, namespaces=ns):
            lang = item.get('{http://www.w3.org/XML/1998/namespace}lang')
            field = ET.Element('field')
            field.text = item.text
            field.set('name', 'keyword_{}'.format(standardize_tag(lang[0:2])))
            xml.find('.').append(field)
        return data


# <field name="is_citable"  type="string" indexed="true" stored="true"  multiValued="false"/>
class IsCitable(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        field = ET.Element('field')
        field.text = "is_true"
        field.set('name', 'is_citable')
        xml.find('.').append(field)
        return data


# <field name="use_license"  type="string" indexed="true" stored="true"  multiValued="false"/>
class Permission(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:rights"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        xpath = ".//dc:rights"

        for item in raw.findall(xpath, namespaces=ns):
            if not item.text.startswith('http'):
                field = ET.Element('field')
                field.text = item.text
                field.set('name', 'use_license_text')
                xml.find('.').append(field)
            else:
                field = ET.Element('field')
                field.text = item.text
                field.set('name', 'use_license_uri')
                xml.find('.').append(field)
                field = ET.Element('field')
                field.text = item.text
                field.set('name', 'use_license_ur')
                xml.find('.').append(field)
        return data


# <field name="in">preprint</field>
class Collection(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        field = ET.Element('field')
        field.text = "preprint"
        field.set('name', 'in')
        xml.find('.').append(field)
        return data


# <field name="type">research-article</field>
class DocumentType(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        field = ET.Element('field')
        field.text = 'research-article'
        field.set('name', 'type')
        xml.find('.').append(field)
        return data


# <field name="au">Marcelo dos Santos, Targa</field>
class Authors(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:creator"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        xpath = ".//dc:creator"

        for author in raw.findall(xpath, namespaces=ns):
            field = ET.Element('field')
            field.text = author.text
            field.set('name', 'au')
            xml.find('.').append(field)
        return data


# <field name="ti_*">Benefits and legacy of the water crisis in Brazil</field>
class Titles(plumber.Pipe):

    def precond(data):
        xpath = ".//dc:title"
        raw, xml = data

        if not raw.findall(xpath, namespaces=ns):
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        xpath = ".//dc:title"

        for item in raw.findall(xpath, namespaces=ns):
            lang = item.get('{http://www.w3.org/XML/1998/namespace}lang')
            if "-" in lang:
                lang = lang.split("-")[0]
            field = ET.Element('field')
            field.text = item.text
            field.set('name', 'ti_{}'.format(lang))
            xml.find('.').append(field)
        return data


class TearDown(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        return xml
