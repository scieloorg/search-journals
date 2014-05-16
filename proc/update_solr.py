#!/usr/bin/python

import sys
import argparse
import logging
import json
import urllib2

import lxml.etree as etree
from datetime import datetime, timedelta
from urllib2 import URLError, HTTPError
from update_settings import *

class Solr(object):
    """Simple abstraction layer around Apache Solr"""

    def __init__(self, url):
        self.url = url

    def select(self, params):
        """Search Solr, return URL and JSON response."""
        params['wt'] = 'json'
        url = self.url + '/select?' + urllib.urlencode(params)
        conn = '{}'
        try:
            conn = urllib2.urlopen(url)
        except URLError as e:
            log_conection_exception(e, url)

        return url, json.load(conn)

    def delete(self, query, commit=False):
        """Delete documents matching `query` from Solr, return (URL, status)"""
        params = {}
        if commit:
            params['commit'] = 'true'
        url = self.url + '/update?' + urllib.urlencode(params)
        status = '-1'

        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data('<delete><query>{0}</query></delete>'.format(query))
        try:
            response = urllib2.urlopen(request).read()
            status = etree.XML(response).findtext('lst/int')
        except URLError as e:
            log_conection_exception(e, url)

        return url, status

    def update(self, add_xml, commitwithin=None):
        """Post list of docs to Solr, return URL and status.
        Opptionall tell Solr to "commitwithin" that many milliseconds."""
        url = self.url + '/update'
        status = '-1'

        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data(add_xml)
        try:
            response = urllib2.urlopen(request).read()
            status = etree.XML(response).findtext('lst/int')
        except URLError as e:
            log_conection_exception(e, url)            

        return url, status

    def commit(self, waitsearcher=False):
        """Commit uncommitted changes to Solr immediately, without waiting."""
        commit_xml = etree.Element('commit')        
        commit_xml.set('waitSearcher', str(waitsearcher).lower())
        url = self.url + '/update'
        status = '-1'
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'text/xml; charset=utf-8')
        request.add_data(etree.tostring(commit_xml, pretty_print=True))
        try:
            response = urllib2.urlopen(request).read()
            status = etree.XML(response).findtext('lst/int')
        except URLError as e:
            log_conection_exception(e, url)

        return url, status


def main():

    # solr object 
    solr = Solr(SOLR_INDEX_URL)

    # set initial values to from and until dates
    from_date  = datetime.now()
    until_date = datetime.now()

    # parser of command line arguments
    parser = argparse.ArgumentParser(description='Update Solr index')

    parser.add_argument('--period', type=str, required=True, 
                           help='index articles from specific period (use: week, month, year or custom). For custom inform --from and --until' )

    parser.add_argument('--from', dest='from_date', type=mkdate, nargs='?', 
                           help='index articles from specific date. YYYY-MM-DD')
 
    parser.add_argument('--until', dest='until_date', type=mkdate, nargs='?', 
                           help='index articles until this specific date. YYYY-MM-DD (default today)',
                           default=datetime.now())

    parser.add_argument('--debug', action='store_true', 
                           help='execute the script in DEBUG mode (don\'t update the index)')
                           
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')    

    args = parser.parse_args()

    if args.period == 'week':
        from_date -= timedelta(days=7)
    elif args.period == 'month':
        from_date -= timedelta(days=30)
    elif args.period == 'year':
        from_date -= timedelta(days=365)
    else:
        if not args.from_date:
            print 'For custom date range please inform at least --from parameters. Use -h for help.'
            sys.exit()
        else:
            from_date = args.from_date
            until_date = args.until_date

    from_date = from_date.strftime("%Y-%m-%d")
    until_date = until_date.strftime("%Y-%m-%d")

    # check for debug mode and reset log level at console logger
    if args.debug:
        ch.setLevel(logging.DEBUG)

    log.info('Start update solr index script with params from={0} and until={1}'.format(from_date, 
        until_date))

    offset = 0
    total_ids = -1    
    fail_update_list = []
    while True:

        (total_ids, article_list) = get_identifiers_list(from_date, until_date, offset)
        if len(article_list) == 0:
            break;

        log.info('Indexing {0} of {1} articles'.format(len(article_list), total_ids))
        offset += IDENTIFIERS_LIMIT        

        # process articles list
        for article in article_list:

            article_code = str(article['code']);
            
            xmliahx_api_url = '{0}?code={1}&format=xmliahx'.format(ARTICLE_ENDPOINT, 
                article_code)
            log.debug('URL used for retrieve solr xml of article {0}'.format(xmliahx_api_url))
            # get xml of article in Solr format
            try:
                xmliahx_response = urllib2.urlopen(xmliahx_api_url)            
                article_solr_xml = xmliahx_response.read()
            except URLError as e:
                log_conection_exception(e, xmliahx_api_url)
                fail_update_list.append(article_code)
                # if is a network connection error stop processing
                if hasattr(e, 'reason'):
                    sys.exit()
                
            else:
                # index article xml
                log.info('Indexing article {0}'.format(article_code))
                # if is in debug mode solr index is not update
                if not args.debug:
                    update_url, update_status = solr.update(article_solr_xml)
                
                    if update_status != '0':
                        log.error('Unable to index article {0}, status code:{1}'.format(article_code, update_status) )
                        fail_update_list.append(article_code)
                

    if fail_update_list:    
        log.warning('Unable to index the following articles {0}'.format(fail_update_list))

    # summary information
    total_fail = len(fail_update_list)
    total_indexed = int(total_ids) - total_fail

    log.info('Index complete! Indexed {0} of {1} articles, {2} fails.'.format(total_indexed, total_ids, total_fail))
    if args.debug:
        log.info('USING DEBUG MODE. SOLR INDEX NOT UPDATED.')
    else:
        (url, commit_status) = solr.commit()
        if commit_status != '0':
            log.warning('Commit command at Solr index fail. Please check and execute commit at index. ')
        else:
            log.info('Commit command at Solr index successfully executed!')

    log.info('End of update solr index script.')

def get_identifiers_list(from_date, until_date, offset):
    article_list = []
    total_ids = 0

    ids_api_url = '{0}?from={1}&until={2}&offset={3}'.format(IDENTIFIERS_ENDPOINT, 
            from_date, until_date, offset)

    log.debug('URL used for retrieve id list: {0}'.format(ids_api_url))

    try:
        id_response = urllib2.urlopen(ids_api_url)
        id_response_json = json.load(id_response)
        article_list = id_response_json['objects']
        total_ids = id_response_json['meta']['total']
    except URLError as e:
        log_conection_exception(e, ids_api_url)
        sys.exit()

    return total_ids, article_list
    

#  handle log of connection issues
def log_conection_exception(e, url):
    if hasattr(e, 'reason'):
        log.critical('Connection error: {0} ({1})'.format(e.reason, url) )
    elif hasattr(e, 'code'):
        log.critical('Request error: {0} ({1})'.format(e.code, url) )


# auxiliary function used at argument parser for convert string to date
def mkdate(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d')


if __name__ == "__main__":
    # create logger
    log = logging.getLogger('update_solr') 
    log.setLevel(logging.DEBUG)   

    # console log
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    # file log
    fh = logging.FileHandler('update_solr.log')
    fh.setLevel(logging.INFO)
    # create a formatter and set the formatter for the handler.
    frmt_con  = logging.Formatter('[%(levelname)-8s]  %(message)s')
    frmt_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(frmt_con)
    fh.setFormatter(frmt_file)

    # add handlers to the logger
    log.addHandler(ch)
    log.addHandler(fh)

    # execute update solr script
    main()
