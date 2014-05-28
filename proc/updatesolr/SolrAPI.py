#!coding: utf-8

import requests
import lxml.etree as etree

class Solr(object):
    """
    Python implementation of the main operation in the Solr API Rest
    """

    def __init__(self, url, timeout=5):
        """
        Create an instance of Solr class.

        :param url: endpoint of Solr
        :param log: dependence injection python built-in logging
        :param timeout: Time for any request, default: 5 seconds
        """
        self.url = url
        self.timeout = timeout

    def select(self, params, format='json'):
        """
        Search Solr, return URL and JSON response.

        :param params: Dictionary parameters to Solr
        :param format: Format of return send to Solr, default=json
        """
        params['wt'] = format

        response = requests.get(self.url + '/select?', params=params, timeout=self.timeout)

        return response.text

    def delete(self, query, commit=False):
        """
        Delete documents matching `query` from Solr.

        :param query: Solr query string, see: https://wiki.apache.org/solr/SolrQuerySyntax
        :param commit: Boolean to carry out the operation
        :param return: Return an int Solr status about the operation or -1 if
                       HTTP status is diferent from 200
        """
        params = {}

        if commit:
            params['commit'] = 'true'

        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        data = '<delete><query>{0}</query></delete>'.format(query)

        response = requests.post(self.url + '/update?', params=params,
                                headers=headers, data=data, timeout=self.timeout)

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
        :param return: Return an int Solr status about the operation or -1 if
                       HTTP status is diferent from 200
        """
        params = {}
        if commit:
            params['commit'] = 'true'

        data = add_xml.encode('utf-8')
        headers = {'Content-Type': 'text/xml; charset=utf-8'}

        response = requests.post(self.url + '/update?', params=params,
                                 headers=headers, data=data, timeout=self.timeout)

        if response.status_code == 200:
            return int(etree.XML(response.text.encode('utf-8')).findtext('lst/int'))
        else:
            return -1

    def commit(self, waitsearcher=False):
        """
        Commit uncommitted changes to Solr immediately, without waiting.

        :param waitsearcher: Boolean wait or not the Solr to execute
        :param return: Return an int Solr status about the operation or -1 if
                       HTTP status is diferent from 200
        """

        data = '<commit waitSearcher="' + str(waitsearcher).lower() + '"/>'
        headers = {'Content-Type': 'text/xml; charset=utf-8'}

        response = requests.post(self.url + '/update?', headers=headers,
                                 data=data, timeout=self.timeout)

        if response.status_code == 200:
            return int(etree.XML(response.text.encode('utf-8')).findtext('lst/int'))
        else:
            return -1
