#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import sys
import time
import json
import argparse
import textwrap
from datetime import datetime, timedelta

from lxml import etree as ET

import plumber
import pipeline_xml
import articlemeta as art_meta

from SolrAPI import Solr
from xylose.scielodocument import Article


URL_SOLR = "http://homolog.search.scielo.org:8080/solr/scielo-articles"


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
                        help='index articles from specific date. YYYY-MM-DD')

    parser.add_argument('-u', '--until',
                        dest='until_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        nargs='?',
                        help='index articles until this specific date. YYYY-MM-DD (default today)',
                        default=datetime.now())

    parser.add_argument('-c', '--collection',
                        dest='collection',
                        default=None,
                        help='use the acronym of the collection eg.: spa, scl, col.')

    parser.add_argument('-i', '--issn',
                        dest='issn',
                        default=None,
                        help='journal issn')

    parser.add_argument('-d', '--delete',
                        dest='delete',
                        default=None,
                        help='delete query ex.: q=*:* (Lucene Syntax)')

    parser.add_argument('-r', '--range',
                        type=int,
                        dest='chunk_range',
                        default=1000,
                        help='range of chenks, send to solr, default:1000')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='version: 0.2')

    def __init__(self):

        self.solr = Solr(URL_SOLR, timeout=10)

        self.args = self.parser.parse_args()

        if self.args.period:
            self.args.from_date = datetime.now() - timedelta(days=self.args.period)

    def _format_date(self, date):
        """
        Convert datetime.datetime to str return: ``2000-05-12``.

        :param datetime: bult-in datetime object

        :returns: str
        """
        if not date:
            return None

        return date.strftime('%Y-%m-%d')

    def chunks(self, _list, step):
        """
        Yield successive n-sized chunks from list.

        :param _list: python object list
        :param step: block of the list
        """

        for i in xrange(0, len(_list), step):
            yield _list[i:i+step]

    def pipeline_to_xml(self, list_dict):
        """
        Pipeline to tranform a dictionary to XML format

        :param list_dict: List of dictionary content key tronsform in a XML.
        """

        ppl = plumber.Pipeline(pipeline_xml.SetupDocumentPipe(),
                               pipeline_xml.XMLDocumentIDPipe(),
                               pipeline_xml.XMLDOIPipe(),
                               pipeline_xml.XMLCollectionPipe(),
                               pipeline_xml.XMLKnowledgeAreaPipe(),
                               pipeline_xml.XMLCenterPipe(),
                               pipeline_xml.XMLDocumentTypePipe(),
                               pipeline_xml.XMLURPipe(),
                               pipeline_xml.XMLAuthorsPipe(),
                               pipeline_xml.XMLTitlePipe(),
                               pipeline_xml.XMLPagesPipe(),
                               pipeline_xml.XMLWOKCIPipe(),
                               pipeline_xml.XMLWOKSCPipe(),
                               pipeline_xml.XMLIssueLabelPipe(),
                               pipeline_xml.XMLJournalTitlePipe(),
                               pipeline_xml.XMLJournalAbbrevTitlePipe(),
                               pipeline_xml.XMLAvailableLanguagesPipe(),
                               # pipeline_xml.XMLFulltextsPipe(),
                               pipeline_xml.XMLPublicationDatePipe(),
                               pipeline_xml.XMLAbstractPipe(),
                               pipeline_xml.XMLAffiliationCountryPipe(),
                               pipeline_xml.XMLAffiliationInstitutionPipe(),
                               pipeline_xml.XMLSponsorPipe(),
                               pipeline_xml.XMLTearDownPipe())

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
                                               _from=self._format_date(self.args.from_date),
                                               _until=self._format_date(self.args.until_date))

            list_ids = [ident for ident in art_ids]

            chunk_list = self.chunks(list_ids, self.args.chunk_range)

            print('Indexing {0} article(s), please wait, it`s may take a while...'.format(len(list_ids)))

            for chunk in chunk_list:

                list_article = []

                for ident in chunk:
                    list_article.append(json.loads(art_meta.get_article(*ident)))

                self.solr.update(self.pipeline_to_xml(list_article), commit=True)

        else:
            self.solr.delete(self.args.delete, commit=True)


def main():

    # Start time
    start = time.time()

    # run the process
    UpdateSearch().run()

    # End Time
    end = time.time()

    print("Duration {0} seconds.".format(end-start))


if __name__ == "__main__":

    # command line
    sys.exit(main() or 0)
