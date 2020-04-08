# coding: utf-8
from lxml import etree as ET

import plumber

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


# <field name="journal_title">Revista Ambiente & Água</field>


# <field name="in">preprint</field>
class Collection(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        field = ET.Element('field')
        field.text = "preprint"
        field.set('name', 'in')
        xml.find('.').append(field)
        return data

# <field name="ac">Agricultural Sciences</field>


# <field name="type">research-article</field>
class DocumentType(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        field = ET.Element('field')
        field.text = 'research-article'
        field.set('name', 'type')
        xml.find('.').append(field)
        return data

# <field name="ur">art-S1980-993X2015000200234</field>


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

# <field name="pg">234-239</field>
# <field name="doi">10.1590/S0102-67202014000200011</field>
# <field name="wok_citation_index">SCIE</field>
# <field name="volume">48</field>
# <field name="supplement_volume">48</field>
# <field name="issue">7</field>
# <field name="supplement_issue">suppl. 2</field>
# <field name="start_page">216</field>
# <field name="end_page">218</field>
# <field name="ta">Rev. Ambient. Água</field>
# <field name="la">en</field>
# <field name="fulltext_pdf_pt">http://www.scielo.br/pdf/ambiagua/v10n2/1980-993X-ambiagua-10-02-00234.pdf</field>
# <field name="fulltext_pdf_pt">http://www.scielo.br/scielo.php?script=sci_abstract&pid=S0102-67202014000200138&lng=en&nrm=iso&tlng=pt</field>
# <field name="da">2015-06</field>
# <field name="ab_*">In this editorial, we reflect on the benefits and legacy of the water crisis....</field>


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

# <field name="aff_country">Brasil</field>
# <field name="aff_institution">usp</field>
# <field name="sponsor">CNPQ</field>


class TearDown(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        return xml
