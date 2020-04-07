#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import os
import sys
import time
import argparse
import logging
import logging.config
import textwrap
from datetime import datetime, timedelta

from lxml import etree as ET

import plumber
import pipeline_xml
from sickle import Sickle

from SolrAPI import Solr

logger = logging.getLogger('updatepreprint')


class UpdatePreprint(object):
    """
    Process to get article in Pre-Print Server and index in Solr.
    """

    usage = """\
    Process to index Pre-Prints articles to SciELO Solr.
    """

    parser = argparse.ArgumentParser(textwrap.dedent(usage))

    parser.add_argument('-p', '--period',
                        type=int,
                        help='index articles from specific period, use number of hours.')

    parser.add_argument('-d', '--delete',
                        dest='delete',
                        help='delete query ex.: q=type:"preprint (Lucene Syntax).')

    parser.add_argument('-solr_url', '--solr_url',
                        dest='solr_url',
                        help='Solr RESTFul URL, processing try to get the variable from environment ``SOLR_URL`` otherwise use --solr_url to set the solr_url (preferable).')

    parser.add_argument('-oai_url', '--oai_url',
                        dest='oai_url',
                        default="https://preprints.scielo.org/index.php/scielo/oai",
                        help='OAI URL, processing try to get the variable from environment ``OAI_URL`` otherwise use --oai_url to set the oai_url (preferable).')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='version: 0.1-beta')

    def __init__(self):

        self.args = self.parser.parse_args()

        solr_url = os.environ.get('SOLR_URL')
        oai_url = os.environ.get('OAI_URL')

        if not solr_url and not self.args.solr_url:
            raise argparse.ArgumentTypeError('--solr_url or ``SOLR_URL`` enviroment variable must be the set, use --help.')

        if not oai_url and not self.args.oai_url:
            raise argparse.ArgumentTypeError('--oai_url or ``OAI_URL`` enviroment variable must be the set, use --help.')

        if not solr_url:
            self.solr = Solr(self.args.solr_url, timeout=10)
        else:
            self.solr = Solr(solr_url, timeout=10)

        if self.args.period:
            self.from_date = datetime.now() - timedelta(hours=self.args.period)

    def pipeline_to_xml(self, article):
        """
        Pipeline to tranform a dictionary to XML format

        :param list_dict: List of dictionary content key tronsform in a XML.
        """

        ppl = plumber.Pipeline(
            pipeline_xml.SetupDocument(),
            pipeline_xml.Example(),
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
        Run the process for update Pre-prints in Solr.
        """

        if self.args.delete:

            self.solr.delete(self.args.delete, commit=True)

        else:

            logger.info("Indexing in {0}".format(self.solr.url))

            sickle = Sickle(self.args.oai_url)

            records = sickle.ListRecords(**{
                                        'metadataPrefix': 'oai_dc',
                                        'from': self.from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                                        })

            for record in records:

                try:
                    xml = self.pipeline_to_xml(record)
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
        UpdatePreprint().run()

        # End Time
        end = time.time()

        print("Duration {0} seconds.".format(end-start))

    except KeyboardInterrupt:
        logger.critical("Interrupt by user")

if __name__ == "__main__":

    # command line
    sys.exit(main() or 0)
