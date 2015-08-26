#!/usr/bin/python
# coding: utf-8

import os
import json
import time
import gevent
import urllib2
import argparse
import itertools
import logging
import logging.config
import gevent.monkey

import articlemeta

# change to gevent.socket.socket
gevent.monkey.patch_socket()

# config logger file
logging.config.fileConfig(os.path.join(os.path.dirname(
                          os.path.abspath(__file__)), 'logging.conf'))

# set logger
logger = logging.getLogger('updatecitation')


class UpdateCitation(object):

    def __init__(self, curl, surl, collection):
        self.curl = curl
        self.surl = surl
        self.collection = collection

    def fetch(self, id):
        resp = urllib2.urlopen(self.curl + 'api/v1/pid/?q=%s' % id).read()
        return id, resp

    def update(self, id, citations):
        data = '{"add":{ "doc":{"id" : "%s", "total_received":{"set":"%s"}}}}' % (id, citations)

        req = urllib2.Request(url='%s/update?wt=json' % self.surl, data=data)
        req.add_header('Content-type', 'application/json')

        return urllib2.urlopen(req).read()

    def commit(self):
        return urllib2.urlopen('%s/update?commit=true' % self.surl).read()

    def optimize(self):
        return urllib2.urlopen('%s/update?optimize=true' % self.surl).read()

    def get_data(self, id, resp):
        cit = json.loads(resp)

        return '%s-%s' % (id, cit['article']['collection']), cit['article']['total_received']

    def run(self, itens=10, limit=10):
        logger.info('Update citation %s' % self.surl)

        offset = 0

        logger.info('Get all ids of articlemeta...')

        ids = [id for id in articlemeta.get_identifiers(collection=self.collection,
                                                        limit=10000,
                                                        offset_range=10000,
                                                        onlyid=True)]
        while True:

            id_slice = itertools.islice(ids, offset, limit)

            logger.info('From %d to %d' % (offset, limit))

            fjobs = [gevent.spawn(self.fetch, id) for id in id_slice if id]

            if not fjobs:
                break

            gevent.joinall(fjobs)

            for job in fjobs:
                job_list = []
                if job.value:
                    id, total_received = self.get_data(*job.value)
                    job_list.append(gevent.spawn(self.update, id, total_received))
                    logger.info('%s, %s' % (id, total_received))

            gevent.joinall(job_list)

            offset += itens
            limit += itens

            gevent.sleep(0)

        logger.info(self.commit())
        logger.info(self.optimize())


def main():
    parser = argparse.ArgumentParser(
        description="Update the search engine with the score of citation"
    )

    parser.add_argument(
        '--citation_url',
        '-curl',
        default='http://citedby.scielo.org/',
        help='URL of Citedby, default: http://citedby.scielo.org/'
    )

    parser.add_argument(
        '--search_url',
        '-surl',
        default='http://node1-search.scielo.org:8080/solr/scielo-articles',
        help='URL Sorl'
    )

    parser.add_argument(
        '-c',
        '--collection',
        dest='collection',
        default=None,
        help='use the acronym of the collection eg.: spa, scl, col.'
    )

    args = parser.parse_args()

    start = time.time()
    UpdateCitation(args.citation_url,
                   args.search_url,
                   args.collection).run(itens=10, limit=10)
    end = time.time()

    logger.info('Duration: %s' % str(end-start))


if __name__ == '__main__':
    main()
