#!/usr/bin/python
#coding: utf-8

import json
import utils
import logging
import requests
import argparse
import logging.config

from datetime import datetime, timedelta

from SolrAPI import Solr

def commit(solr, debug=False):

    if debug:
        log.info('USING DEBUG MODE. SOLR INDEX NOT UPDATED.')
    else:
        status = solr.commit()
        if status != 0:
            log.warning('Commit command at Solr index fail. Please check and execute commit at index. ')
        else:
            log.info('Commit command at Solr index successfully executed!')


def summary(total, fail_list, debug=False):

    if fail_list:
        log.warning('Unable to index the following articles {0}'.format(fail_list))

    if not debug:
        log.info('Index complete! Indexed {0} of {1} articles, {2} fails.'.format(
            int(total) - len(fail_list), total, len(fail_list)))

    log.info('End of update solr index script.')


def get_identifiers(from_date, until_date, collection, offset):

    if not collection:
        ident_url = '{0}?from={1}&until={2}&offset={3}'.format(
            settings['endpoints']['identifiers'], from_date, until_date, offset)
    else:
        ident_url = '{0}?from={1}&until={2}&collection={3}&offset={4}'.format(
            settings['endpoints']['identifiers'], from_date, until_date, collection, offset)

    log.debug('URL used for retrieve id list: {0}'.format(ident_url))

    try:
        response = requests.get(ident_url)
    except requests.exceptions.RequestException as e:
        log.critical('Connection error: {0}'.format(e))
    else:
        response_json = json.loads(response.text)
        return response_json['meta']['total'], list(response_json['objects'])


def main(settings, *args, **xargs):

    solr = Solr(settings['endpoints']['solr'], timeout=int(settings['request']['timeout']))

    from_date  = datetime.now()
    until_date = datetime.now()

    parser = argparse.ArgumentParser(description='Script to update Solr')

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

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='execute the script in DEBUG mode (don\'t update the index)')

    parser.add_argument('-v', '--version',
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

    log.info('Start update solr index script with params from={0} and until={1}'.format(
        from_date,until_date))

    total = 0
    offset = 0
    fail_list = []
    sum_processed = 0
    while True:
        try:
            total, article_lst = get_identifiers(from_date, until_date,
                args.collection, offset)

            if len(article_lst) == 0:
                break;

            sum_processed += len(article_lst)

            log.info('Indexing {0} of {1} articles'.format(sum_processed, total))

            offset += int(settings['params']['limit_offset'])

            for article in article_lst:

                article_code = str(article['code']);

                code_url = '{0}?code={1}&format=xmliahx'.format(
                    settings['endpoints']['article'], article_code)

                log.debug('URL used for retrieve solr xml of article {0}'.format(code_url))

                try:
                    response = requests.get(code_url)
                except requests.exceptions.RequestException as e:
                    log.critical('Connection error: {0}'.format(e))
                    fail_list.append(article_code)
                else:
                    solr_xml = response.text

                    log.info('Indexing article {0}'.format(article_code))

                    if not args.debug:
                        status = solr.update(solr_xml)

                        if status != 0:
                            log.error('Unable to index article {0}, code:{1}'.format(
                                article_code, status))
                            fail_list.append(article_code)

            #commit on any offset cycle
            commit(solr, debug=args.debug)
        except Exception as e:
            log.critical('Unexpected error: {0}'.format(e))

    summary(total, fail_list, args.debug)


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
