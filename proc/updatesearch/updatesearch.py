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
import pipeline_xml
from articlemeta.client import ThriftClient

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
            self.crossref = self.load_zipped_metadata(self.args.file_crossref)

    def format_date(self, date):
        """
        Convert datetime.datetime to str return: ``2000-05-12``.

        :param datetime: bult-in datetime object

        :returns: str
        """
        if not date:
            return None

        return date.strftime('%Y-%m-%d')

    def load_zipped_metadata(self, zipped_metadata):
        inner_file_name = zipped_metadata.split('/')[-1].split('.zip')[0]
        with zipfile.ZipFile(zipped_metadata).open(inner_file_name) as zf:
            return json.loads(zf.read()).get('metadata', {})

    def pipeline_to_xml(self, article, external_metadata=None):
        """
        Pipeline to tranform a dictionary to XML format

        :param list_dict: List of dictionary content key tronsform in a XML.
        """

        ppl = plumber.Pipeline(
            pipeline_xml.SetupDocument(),
            pipeline_xml.DocumentID(),
            pipeline_xml.Entity(),
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

            # Citation IDs
            pipeline_xml.CitationFK(),

            # Citation Authors
            pipeline_xml.CitationFKAuthors(),

            # Citation Normalized Journals' Titles
            pipeline_xml.CitationFKJournalsExternalData(external_metadata),

            # Citation Journals' Titles
            pipeline_xml.CitationFKJournals(),

            # Pipeline Article.Citations
            pipeline_xml.CitationEntity(external_metadata),
            pipeline_xml.TearDown()
        )

        xmls = ppl.run([article])

        # Add root document
        add = ET.Element('add')

        for xml in xmls:
            add.append(xml)

        return ET.tostring(add, encoding="utf-8", method="xml")

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
                # Check if normalized metadata were loaded
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
