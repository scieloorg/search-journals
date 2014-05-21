#!/usr/bin/python
#coding: utf-8

import json
import utils
import logging
import requests
import argparse
import logging.config
import lxml.etree as etree

from datetime import datetime, timedelta

class Solr(object):

    def __init__(self, url, log, timeout=5):
        """
        Create an instance of Solr class.

        :param url: endpoint of Solr
        :param log: dependence injection python built-in logging
        :param timeout: Time for any request, default: 5 seconds
        """
        self.url = url
        self.log = log
        self.timeout = timeout

    def select(self, params, format='json'):
        """
        Search Solr, return URL and JSON response.

        :param params: Dictionary parameters to Solr
        :param format: Format of return send to Solr, default=json
        """
        params['wt'] = format

        try:
            response = requests.get(self.url + '/select?', params=params, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            self.log.critical('Connection error: {0}'.format(e) )
        else:
            return response.text

    def delete(self, query, commit=False):
        """
        Delete documents matching `query` from Solr.

        :param query: Solr query string, see: https://wiki.apache.org/solr/SolrQuerySyntax
        :param commit: Boolean to carry out the operation
        :param return: Return an int Solr status about the operation
        """
        params = {}
        if commit:
            params['commit'] = 'true'

        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        data = '<delete><query>{0}</query></delete>'.format(query)

        try:
            response = requests.post(self.url + '/update?', params=params,
                                    headers=headers, data=data, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            self.log.critical('Connection error: {0}'.format(e) )
        else:
            if response.status_code == 200:
                return int(etree.XML(response.text.encode('utf-8')).findtext('lst/int'))
            else:
                return -1

    def update(self, add_xml, commit=False):
        """
        Post list of docs to Solr.

        :param commit: Boolean to carry out the operation
        :param add_xml: XML send to Solr, ex.:
            <add>
              <doc>
                <field name="id">XXX</field>
                <field name="field_name">YYY</field>
              </doc>
            </add>
        :param return: Return an int Solr status about the operation
        """
        params = {}
        if commit:
            params['commit'] = 'true'

        data = add_xml.encode('utf-8')
        headers = {'Content-Type': 'text/xml; charset=utf-8'}

        try:
            response = requests.post(self.url + '/update?', params=params,
                                     headers=headers, data=data, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            self.log.critical('Connection error: {0}'.format(e) )
        else:
            if response.status_code == 200:
                return int(etree.XML(response.text.encode('utf-8')).findtext('lst/int'))
            else:
                return -1

    def commit(self, waitsearcher=False):
        """
        Commit uncommitted changes to Solr immediately, without waiting.

        :param waitsearcher: Boolean wait or not the Solr to execute
        :param return: Return an int Solr status about the operation
        """

        data = '<commit waitSearcher="' + str(waitsearcher).lower() + '"/>'
        headers = {'Content-Type': 'text/xml; charset=utf-8'}

        try:
            response = requests.post(self.url + '/update?', headers=headers,
                                     data=data, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            self.log.critical('Connection error: {0}'.format(e) )
        else:
            if response.status_code == 200:
                return int(etree.XML(response.text.encode('utf-8')).findtext('lst/int'))
            else:
                return -1


def get_identifiers_list(from_date, until_date, offset):

    ids_api_url = '{0}?from={1}&until={2}&offset={3}'.format(settings['endpoints']['identifiers'],
                                                      from_date, until_date, offset)

    log.debug('URL used for retrieve id list: {0}'.format(ids_api_url))

    try:
        response = requests.get(ids_api_url)
    except requests.exceptions.RequestException as e:
        log.critical('Connection error: {0}'.format(e))
    else:
        response_json = json.loads(response.text)
        return response_json['meta']['total'], list(response_json['objects'])


def main(settings, *args, **xargs):

    solr = Solr(settings['endpoints']['solr'], log, timeout=int(settings['request']['timeout']))

    from_date  = datetime.now()
    until_date = datetime.now()

    parser = argparse.ArgumentParser(description='Script to update Solr')

    parser.add_argument('--period',
                        type=int,
                        help='index articles from specific period, use number of days.')

    parser.add_argument('--from',
                        dest='from_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        nargs='?',
                        help='index articles from specific date. YYYY-MM-DD')

    parser.add_argument('--until',
                        dest='until_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        nargs='?',
                        help='index articles until this specific date. YYYY-MM-DD (default today)',
                        default=datetime.now())

    parser.add_argument('--debug',
                        action='store_true',
                        help='execute the script in DEBUG mode (don\'t update the index)')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 0.1')

    args = parser.parse_args()


    if args.from_date:
        from_date = args.from_date

    if args.until_date:
        until_date = args.until_date

    if args.period:
        from_date -= timedelta(days=args.period)

    from_date = from_date.strftime("%Y-%m-%d")
    until_date = until_date.strftime("%Y-%m-%d")

    if args.debug:
        log.setLevel(logging.DEBUG)

    log.info('Start update solr index script with params from={0} and until={1}'.format(from_date,
        until_date))

    offset = 0
    total_ids = 0
    fail_list = []
    while True:
        try:
            total_ids, article_list = get_identifiers_list(from_date, until_date, offset)

            if len(article_list) == 0:
                break;

            log.info('Indexing {0} of {1} articles'.format(len(article_list), total_ids))

            offset += int(settings['params']['limit_offset'])

            for article in article_list:

                article_code = str(article['code']);

                xmliahx_api_url = '{0}?code={1}&format=xmliahx'.format(settings['endpoints']['article'],
                                                                       article_code)
                log.debug('URL used for retrieve solr xml of article {0}'.format(xmliahx_api_url))

                try:
                    response = requests.get(xmliahx_api_url)
                except requests.exceptions.RequestException as e:
                    log.critical('Connection error: {0}'.format(e) )
                    fail_list.append(article_code)
                else:
                    article_solr_xml = response.text

                    log.info('Indexing article {0}'.format(article_code))

                    if not args.debug:
                        status = solr.update(article_solr_xml)

                        if status != 0:
                            log.error('Unable to index article {0}, status code:{1}'.format(article_code, status) )
                            fail_list.append(article_code)
        except Exception as e:
            log.critical('Unexpected error: {0}'.format(e))

    if fail_list:
        log.warning('Unable to index the following articles {0}'.format(fail_list))

    log.info('Index complete! Indexed {0} of {1} articles, {2} fails.'.format(
                                                int(total_ids) - len(fail_list),
                                                total_ids,
                                                len(fail_list)))

    if args.debug:
        log.info('USING DEBUG MODE. SOLR INDEX NOT UPDATED.')
    else:
        status = solr.commit()
        if status != 0:
            log.warning('Commit command at Solr index fail. Please check and execute commit at index. ')
        else:
            log.info('Commit command at Solr index successfully executed!')

    log.info('End of update solr index script.')


if __name__ == "__main__":

    # config app file
    config = utils.Configuration.from_env()
    settings = dict(config.items())

    # config logger file
    logging.config.fileConfig('logging.conf')

    # create logger
    log = logging.getLogger('update_solr')

    # execute update solr script
    main(settings)
