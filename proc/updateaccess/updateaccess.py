#!/usr/bin/python
# coding: utf-8

import os
import json
import time
import logging
import urllib2
import argparse
import logging.config

import thriftpy
from thriftpy.rpc import make_client

import articlemeta

access_stats_thrift = thriftpy.load(
    os.path.dirname(__file__)+'thrift/access_stats.thrift',
    module_name='access_stats_thrift'
)

client = make_client(access_stats_thrift.AccessStats, 'ratchet.scielo.org', 11640)


# config logger file
logging.config.fileConfig(os.path.join(os.path.dirname(
                          os.path.abspath(__file__)), 'logging.conf'))

# set logger
logger = logging.getLogger('updateaccess')


class UpdateAccess(object):

    def __init__(self, url, collection):
        self.url = url
        self.collection = collection

    def update(self, code, total):
        data = '{"add":{ "doc":{"id" : "%s", "total_access":{"set":"%s"}}}}' % (code, int(total))
        logger.info(data)

        req = urllib2.Request(url='%s/update?wt=json' % self.url, data=data)
        req.add_header('Content-type', 'application/json')

        return urllib2.urlopen(req).read()

    def commit(self):
        return urllib2.urlopen('%s/update?commit=true' % self.url).read()

    def optimize(self):
        return urllib2.urlopen('%s/update?optimize=true' % self.url).read()

    def run(self):
        logger.info('Update access on search %s' % self.url)

        logger.info('Get all ids of articlemeta...')

        ids = articlemeta.get_identifiers(collection=self.collection,
                                          limit=10000,
                                          offset_range=10000,
                                          onlyid=False)

        for col, code in ids:

            try:
                doc = client.document(code, col)
            except access_stats_thrift.ServerError as e:
                logger.error('The doc %s-%s cant be updated' % (code, col))
                logger.error('Error: %s' % e.message)
            else:
                jdoc = json.loads(doc)
                logger.info(self.update('%s-%s' % (code, col), jdoc['access_total']['value']))

        logger.info(self.commit())
        logger.info(self.optimize())


def main():
    parser = argparse.ArgumentParser(
        description="Update access stats on search engine"
    )

    parser.add_argument(
        '--url',
        '-u',
        default='http://node1-search.scielo.org:8080/solr/scielo-articles',
        help='URL Sorl'
    )

    parser.add_argument('-c', '--collection',
                        dest='collection',
                        default=None,
                        help='use the acronym of the collection eg.: spa, scl, col.')

    args = parser.parse_args()

    start = time.time()
    UpdateAccess(args.url, args.collection).run()
    end = time.time()

    logger.info('Duration: %s' % str(end-start))


if __name__ == '__main__':
    main()
