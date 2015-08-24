#!/usr/bin/python
# coding: utf-8

import os
import logging

import thriftpy
from thriftpy.rpc import make_client

logger = logging.getLogger(__name__)

articlemeta_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'thrift/articlemeta.thrift'))

client = make_client(articlemeta_thrift.ArticleMeta, 'articlemeta.scielo.org', 11720)


def get_identifiers(collection=None, issn=None, _from=None, _until=None,
                    limit=1000, offset_range=1000, onlyid=False):

    """
    Get all identifiers by Article Meta Thrift

    :param _from: inicial date
    :param _until: final date
    :param collection: it`s acronym of collection, ex.: scl, cub, mex, ury
    :param limit: limit of the slice
    :param offset_range: paging through RCP result, default:1000
    :param onlyid: default=False returns only SciELO ID

    :returns: return a generator with a tuple ``(collection, PID)`` or just ``PID``
    ex.: (mex, S0036-36342014000100009)
    """

    offset = 0

    logger.debug('Get all identifiers from Article Meta, please wait... this while take while!')

    while True:
        idents = client.get_article_identifiers(collection, issn, _from, _until,
                                                limit, offset)

        if not idents:
            raise StopIteration

        for ident in idents:
            logger.debug('code: %s collection: %s' %
                         (ident.code, ident.collection))

            if onlyid:
                yield ident.code
            else:
                yield (ident.collection, ident.code)

        offset += offset_range


def get_article(code, collection):
    """
    Get article meta data by code and collection

    :param code: SciELO PID(Publisher Identifier)
    :param collection: collection acronym, ex.: scl, cub, mex, ury

    :returns: JSON (Java Script Object Notation)
    """
    logger.debug('Get article with code: %s by collection %s' % (code, collection))

    return client.get_article(collection, code, True)