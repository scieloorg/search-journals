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
import articlemeta as art_meta

from SolrAPI import Solr
from xylose.scielodocument import Article

logger = logging.getLogger('updatesearch')


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

    parser.add_argument('-r', '--range',
                        type=int,
                        dest='chunk_range',
                        default=1000,
                        help='range of chunks, send to solr, default:1000.')

    parser.add_argument('-url', '--url',
                        dest='solr_url',
                        help='Solr RESTFul URL, processing try to get the variable from environment ``SOLR_URL`` otherwise use --url to set the url(preferable).')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='version: 0.2')

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

    def format_date(self, date):
        """
        Convert datetime.datetime to str return: ``2000-05-12``.

        :param datetime: bult-in datetime object

        :returns: str
        """
        if not date:
            return None

        return date.strftime('%Y-%m-%d')

    def pipeline_to_xml(self, list_dict):
        """
        Pipeline to tranform a dictionary to XML format

        :param list_dict: List of dictionary content key tronsform in a XML.
        """

        ppl = plumber.Pipeline(pipeline_xml.SetupDocument(),
                               pipeline_xml.DocumentID(),
                               pipeline_xml.DOI(),
                               pipeline_xml.Collection(),
                               pipeline_xml.KnowledgeArea(),
                               pipeline_xml.DocumentType(),
                               pipeline_xml.URL(),
                               pipeline_xml.Authors(),
                               pipeline_xml.Titles(),
                               pipeline_xml.OriginalTitle(),
                               pipeline_xml.Pages(),
                               pipeline_xml.WOKCI(),
                               pipeline_xml.WOKSC(),
                               pipeline_xml.JournalAbbrevTitle(),
                               pipeline_xml.AvailableLanguages(),
                               pipeline_xml.Fulltexts(),
                               pipeline_xml.PublicationDate(),
                               pipeline_xml.Abstract(),
                               pipeline_xml.AffiliationCountry(),
                               pipeline_xml.AffiliationInstitution(),
                               pipeline_xml.Sponsor(),
                               pipeline_xml.Volume(),
                               pipeline_xml.SupplementVolume(),
                               pipeline_xml.Issue(),
                               pipeline_xml.SupplementIssue(),
                               pipeline_xml.StartPage(),
                               pipeline_xml.EndPage(),
                               pipeline_xml.JournalTitle(),
                               pipeline_xml.TearDown())

        xmls = ppl.run([Article(article) for article in list_dict])

        # Add root document
        add = ET.Element('add')

        for xml in xmls:
            add.append(xml)

        return ET.tostring(add, encoding="utf-8", method="xml")

    def run(self):
        """
        Run the process for update article in Solr.
        """

        if not self.args.delete:

            # Get article identifiers
            art_ids = art_meta.get_identifiers(collection=self.args.collection,
                                               issn=self.args.issn,
                                               _from=self.format_date(self.args.from_date),
                                               _until=self.format_date(self.args.until_date))

            logger.info("Indexing in {0}".format(self.solr.url))

            count = 0
            while True:
                try:
                    lst_ids = list(itertools.islice(art_ids, 0, self.args.chunk_range))

                    if not lst_ids:
                        break

                    list_article = []

                    for ident in lst_ids:
                        list_article.append(json.loads(art_meta.get_article(*ident)))

                    self.solr.update(self.pipeline_to_xml(list_article), commit=True)

                    count += len(list_article)

                    logger.info("Updated {0} articles".format(count))

                except ValueError as e:
                    logger.error("Error: {0}".format(e))
                    continue
                except Exception as e:
                    logger.error("Error: {0}".format(e))
                    sys.exit(0)
        else:

            self.solr.delete(self.args.delete, commit=True)

        # optimize the index
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
