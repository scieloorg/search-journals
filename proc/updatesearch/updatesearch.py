#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import os
import sys
import time
import json
import argparse
import logging
import logging.config
import textwrap
import itertools
from datetime import datetime, timedelta

from lxml import etree as ET

import plumber
import pipeline_xml, citation_pipeline_xml
from articlemeta.client import ThriftClient
from copy import deepcopy

from SolrAPI import Solr

import zipfile


logger = logging.getLogger('updatesearch')

ALLOWED_COLLECTION = [
    'scl',
    'arg',
    'cub',
    'esp',
    'sss',
    'spa',
    'chl',
    'mex',
    'prt',
    'ecu',
    'cri',
    'sza',
    'col',
    'per',
    'ven',
    'ury',
    'bol',
    'par'
]


class UpdateSearch(object):
    """
    Process to get article in article meta and index in Solr.
    """

    usage = """\
    Process to index article to SciELO Solr.

    This process collects articles in the Article meta using thrift and index
    in SciELO Solr.

    With this process it is possible to process all the article or some specific
    by collection, issn from date to until another date and a period like 7 days.
    """

    parser = argparse.ArgumentParser(textwrap.dedent(usage))

    parser.add_argument('-p', '--period',
                        type=int,
                        help='index articles from specific period, use number of days.')

    parser.add_argument('-f', '--from',
                        dest='from_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        nargs='?',
                        help='index articles from specific date. YYYY-MM-DD.')

    parser.add_argument('-u', '--until',
                        dest='until_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        nargs='?',
                        help='index articles until this specific date. YYYY-MM-DD (default today).',
                        default=datetime.now())

    parser.add_argument('-c', '--collection',
                        dest='collection',
                        default=None,
                        help='use the acronym of the collection eg.: spa, scl, col.')

    parser.add_argument('-i', '--issn',
                        dest='issn',
                        default=None,
                        help='journal issn.')

    parser.add_argument('-d', '--delete',
                        dest='delete',
                        default=None,
                        help='delete query ex.: q=*:* (Lucene Syntax).')

    parser.add_argument('-s', '--sanitization',
                        dest='sanitization',
                        default=False,
                        action='store_true',
                        help='Remove objects from the index that are no longer present in the database.')

    parser.add_argument('-url', '--url',
                        dest='solr_url',
                        help='Solr RESTFul URL, processing try to get the variable from environment ``SOLR_URL`` otherwise use --url to set the url(preferable).')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='version: 0.2')

    parser.add_argument('-m', '--metadata',
                        dest='file_crossref',
                        help='json zipped file containing metadata gathered from the CrossRef service'
                        )

    def __init__(self):

        self.args = self.parser.parse_args()

        solr_url = os.environ.get('SOLR_URL')

        if not solr_url and not self.args.solr_url:
            raise argparse.ArgumentTypeError('--url or ``SOLR_URL`` enviroment variable must be the set, use --help.')

        if not solr_url:
            self.solr = Solr(self.args.solr_url, timeout=10)
        else:
            self.solr = Solr(solr_url, timeout=10)

        if self.args.period:
            self.args.from_date = datetime.now() - timedelta(days=self.args.period)

        if self.args.file_crossref:
            self.crossref = self.load_zipped_external_data(self.args.file_crossref)

    def format_date(self, date):
        """
        Convert datetime.datetime to str return: ``2000-05-12``.

        :param datetime: bult-in datetime object

        :returns: str
        """
        if not date:
            return None

        return date.strftime('%Y-%m-%d')

    def load_zipped_external_data(self, zipped_external_data):
        """
        Lê arquivo com dados extras e normalizados de citações.
        Chave de cada registro é o id da citação.
        Valor de cada registro é o conjunto de campos extras e normalizados da citação.
        
        :param zipped_external_data: dados normalizados em formato zip

        :returns: dict
        """
        inner_file_name = zipped_external_data.split('/')[-1].split('.zip')[0]
        with zipfile.ZipFile(zipped_external_data).open(inner_file_name) as zf:
            return json.loads(zf.read()).get('metadata', {})

    def pipeline_to_xml(self, article, external_metadata=None):
        """
        Pipeline to tranform a dictionary to XML format

        :param list_dict: List of dictionary content key tronsform in a XML.
        """

        ppl = plumber.Pipeline(
            # Conjunto de pipes criador de artigo (<doc> artigo, entity: document)
            pipeline_xml.SetupDocument(),
            pipeline_xml.DocumentID(),
            pipeline_xml.Entity(name='document'),
            pipeline_xml.DOI(),
            pipeline_xml.Collection(),
            pipeline_xml.DocumentType(),
            pipeline_xml.URL(),
            pipeline_xml.Authors(),
            pipeline_xml.Titles(),
            pipeline_xml.OriginalTitle(),
            pipeline_xml.Pages(),
            pipeline_xml.WOKCI(),
            pipeline_xml.WOKSC(),
            pipeline_xml.JournalAbbrevTitle(),
            pipeline_xml.JournalAbbrevTitle(field_name='super_ta'),
            pipeline_xml.Languages(),
            pipeline_xml.AvailableLanguages(),
            pipeline_xml.Fulltexts(),
            pipeline_xml.PublicationDate(),
            pipeline_xml.SciELOPublicationDate(),
            pipeline_xml.SciELOProcessingDate(),
            pipeline_xml.Abstract(),
            pipeline_xml.AffiliationCountry(),
            pipeline_xml.AffiliationInstitution(),
            pipeline_xml.Sponsor(),
            pipeline_xml.Volume(),
            pipeline_xml.SupplementVolume(),
            pipeline_xml.Issue(),
            pipeline_xml.SupplementIssue(),
            pipeline_xml.ElocationPage(),
            pipeline_xml.StartPage(),
            pipeline_xml.EndPage(),
            pipeline_xml.JournalTitle(),
            pipeline_xml.IsCitable(),
            pipeline_xml.Permission(),
            pipeline_xml.Keywords(),
            pipeline_xml.JournalISSNs(),
            pipeline_xml.SubjectAreas(),
            # pipeline_xml.ReceivedCitations(),
        )

        xmls = ppl.run([article])

        # Constrói elementos <doc> para as referências citadas (<doc>s citação, entities 'citation')
        # Obtem elementos estrangeiros das referências citadas (para usar no <doc> artigo)
        cit_xmls, citations_fk = self.get_xmls_citations(article, external_metadata)

        # Cria elemento raiz
        add = ET.Element('add')

        # Adiciona <doc>s citação na raiz
        for cit_xml in cit_xmls:
            add.append(cit_xml)

        # Adiciona no <doc> artigo as informações estrangeiras das referências citadas
        for r, xml in xmls:
            for tag in xml:
                citations_fk.find('.').append(tag)

        # Adiciona <doc> artigo na raiz
        add.append(citations_fk)

        return ET.tostring(add, encoding="utf-8", method="xml")

    def get_xmls_citations(self, document, external_metadata):
        """
        Pipeline para transformar citações em documentos Solr.
        Gera um <doc> citação para cada citação. Povoa esses <doc>s com dados das citações e do artigo citante.
        Extrai campos estrangeiros das referências citadas para povoar <doc> artigo.

        :param document: Article
        :param external_metadata: dict de dados extras e normalizados das citações

        :return citations_xmls: <doc>s das citações
        :return citations_fk: campos estrangeiros das citações
        """

        # Pipeline para adicionar no <doc> citation dados da referência citada
        ppl_citation = plumber.Pipeline(
            # Dados da referência citada
            citation_pipeline_xml.SetupDocument(),
            pipeline_xml.Entity(name='citation'),
            citation_pipeline_xml.DocumentID(),
            citation_pipeline_xml.IndexNumber(),
            citation_pipeline_xml.DOI(),
            citation_pipeline_xml.PublicationType(),
            citation_pipeline_xml.Authors(),
            citation_pipeline_xml.AnalyticAuthors(),
            citation_pipeline_xml.MonographicAuthors(),
            citation_pipeline_xml.PublicationDate(),
            citation_pipeline_xml.Institutions(),
            citation_pipeline_xml.Publisher(),
            citation_pipeline_xml.PublisherAddress(),
            citation_pipeline_xml.Pages(),
            citation_pipeline_xml.StartPage(),
            citation_pipeline_xml.EndPage(),
            citation_pipeline_xml.Title(),
            citation_pipeline_xml.Source(),
            citation_pipeline_xml.Serie(),
            citation_pipeline_xml.ChapterTitle(),
            citation_pipeline_xml.ISBN(),
            citation_pipeline_xml.ISSN(),
            citation_pipeline_xml.Issue(),
            citation_pipeline_xml.Volume(),
            citation_pipeline_xml.Edition(),

            # Pipe para dicionar no <doc> citation dados normalizados do dicionário external_metadata
            citation_pipeline_xml.ExternalData(external_metadata),

            # Pipe para adicionar <doc> citation o id do artigo citante
            citation_pipeline_xml.DocumentFK(),

            # Pipe para adicionar no <doc> citation a coleção do artigo citante
            citation_pipeline_xml.Collection()
        )

        # Pipeline para adicionar no <doc> citation os autores e periódico do documento citante
        ppl_doc_fk = plumber.Pipeline(
            pipeline_xml.SetupDocument(),

            # Pipe para adicionar autores do artigo citante
            pipeline_xml.Authors(field_name='document_fk_au'),

            # Pipe para adicionar títulos do periódico do artigo citante
            pipeline_xml.JournalTitle(field_name="document_fk_ta"),
            pipeline_xml.JournalAbbrevTitle(field_name="document_fk_ta")
        )

        # Pipeline para adicionar no <doc> do artigo dados das referências citadas
        ppl_citations_fk = plumber.Pipeline(
            pipeline_xml.SetupDocument(),

            # Pipe para adicionar os ids das referências citadas
            pipeline_xml.CitationFK(),

            # Pipe para adicionar os nomes dos autores das referências citadas
            pipeline_xml.CitationFKAuthors(),

            # Pipe para adicionar os títulos extras e normalizados dos periódicos das referências citadas
            pipeline_xml.CitationFKJournalsExternalData(external_metadata),

            # Pipe para adicionar os títulos dos periódicos das referências citadas
            pipeline_xml.CitationFKJournals()
        )

        citations_xmls = []

        # Cria tags de dados básicos do artigo a serem inseridas nos documentos do tipo citação
        doc_basic_xml = ET.Element('doc')
        doc_raw_xml = ppl_doc_fk.run([document])
        for r, xml in doc_raw_xml:
            for tag in xml:
                doc_basic_xml.find('.').append(tag)

        # Cria documentos para as citações
        if document.citations:
            for cit in document.citations:
                cit_root = ET.Element('doc')
                if cit.publication_type in pipeline_xml.CITATION_ALLOWED_TYPES:
                    cit_raw_xml = ppl_citation.run([cit])
                    # Adiciona tags da citação
                    for r, tags in cit_raw_xml:
                        for tag in tags:
                            cit_root.append(tag)

                    # Adiciona tags do documento citante
                    for tag in deepcopy(doc_basic_xml):
                        cit_root.append(tag)

                    citations_xmls.append(cit_root)

        # Cria tags de dados estrangeiros das citações a serem inseridas no documento citante
        citations_fk = ET.Element('doc')
        fk_raw_xml = ppl_citations_fk.run([document])
        for r, tags in fk_raw_xml:
            for tag in tags:
                citations_fk.find('.').append(tag)

        return citations_xmls, citations_fk

    def run(self):
        """
        Run the process for update article in Solr.
        """

        art_meta = ThriftClient()

        if self.args.delete:

            self.solr.delete(self.args.delete, commit=True)

        elif self.args.sanitization:

            # set of index ids
            ind_ids = set()

            # set of articlemeta ids
            art_ids = set()

            # all ids in index
            list_ids = json.loads(self.solr.select(
                                    {'q': '*:*', 'fl': 'id', 'rows': 1000000}))['response']['docs']

            for id in list_ids:
                ind_ids.add(id['id'])

            # all ids in articlemeta
            for item in art_meta.documents(only_identifiers=True):
                if item.collection not in ALLOWED_COLLECTION:
                    continue
                art_ids.add('%s-%s' % (item.code, item.collection))

            # Ids to remove
            remove_ids = ind_ids - art_ids

            for id in remove_ids:
                self.solr.delete('id:%s' % id, commit=True)

            logger.info("List of removed ids: %s" % remove_ids)

        else:

            # Get article identifiers

            logger.info("Indexing in {0}".format(self.solr.url))

            for document in art_meta.documents(
                collection=self.args.collection,
                issn=self.args.issn,
                from_date=self.format_date(self.args.from_date),
                until_date=self.format_date(self.args.until_date)
            ):
                # Verifica se dados normalizados foram carregados
                if self.args.file_crossref:
                    external_metadata = self.crossref
                else:
                    external_metadata = {}

                try:
                    xml = self.pipeline_to_xml(document, external_metadata)
                    self.solr.update(xml, commit=True)
                except ValueError as e:
                    logger.error("ValueError: {0}".format(e))
                    logger.exception(e)
                    continue
                except Exception as e:
                    logger.error("Error: {0}".format(e))
                    logger.exception(e)
                    continue

        # optimize the index
        self.solr.commit()
        self.solr.optimize()


def main():

    try:
        # set log
        logging.config.fileConfig('logging.conf')

        # Start time
        start = time.time()

        # run the process
        UpdateSearch().run()

        # End Time
        end = time.time()

        print("Duration {0} seconds.".format(end-start))

    except KeyboardInterrupt:
        logger.critical("Interrupt by user")

if __name__ == "__main__":

    # command line
    sys.exit(main() or 0)
