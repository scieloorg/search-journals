#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import json
import time
import gevent
import urllib2
import argparse
import itertools
import gevent.monkey

import articlemeta

# change to gevent.socket.socket
gevent.monkey.patch_socket()


class UpdateCitation(object):

    def __init__(self, curl, surl):
        self.curl = curl
        self.surl = surl

    def fetch(self, id):
        resp = urllib2.urlopen(self.curl + 'api/v1/pid/?q=%s&metaonly=true' % id).read()
        return id, resp

    def update(self, id, citations):
        req = urllib2.Request(url='%s/update?wt=json' % self.surl,
                              data='{"add":{ "doc":{"id" : "%s", "total_received":{"set":"%s"}}}}' % (id, citations))
        req.add_header('Content-type', 'application/json')

        return urllib2.urlopen(req).read()

    def commit(self):
        return urllib2.urlopen('%s/update?commit=true' % self.surl).read()

    def get_data(self, id, resp):
        cit = json.loads(resp)

        return '%s-%s' % (id, cit['article']['collection']), cit['article']['total_received']

    def run(self, itens=10, limit=10):
        print('Update citation %s' % self.surl)

        offset = 0

        print('Get all ids of articlemeta...')

        ids = [id for id in articlemeta.get_identifiers(limit=10000,
                                                        offset_range=10000,
                                                        onlyid=True)]
        while True:

            id_slice = itertools.islice(ids, offset, limit)

            print('From %d to %d' % (offset, limit))

            fjobs = [gevent.spawn(self.fetch, id) for id in id_slice if id]

            if not fjobs:
                break

            gevent.joinall(fjobs)

            for job in fjobs:
                job_list = []
                if job.value:
                    id, total_received = self.get_data(*job.value)
                    job_list.append(gevent.spawn(self.update, id, total_received))
                    print(id, total_received)

            gevent.joinall(job_list)

            offset += itens
            limit += itens

            gevent.sleep(0)

        self.commit()


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

    args = parser.parse_args()

    start = time.time()
    UpdateCitation(args.citation_url, args.search_url).run(itens=10, limit=10)
    end = time.time()

    print('Duration: %d' (end-start))


if __name__ == '__main__':
    main()
