#!/usr/bin/env python
from setuptools import setup

setup(
    name="UpdatePrePrint",
    version='0.1-beta',
    description="Update Pre-Print articles to Solr",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    url="https://github.com/scieloorg/search-journals/tree/beta/proc/updatepreprint",
    keywords='solr api lucene scielo',
    maintainer_email='jamil.atta@scielo.org',
    classifiers=[
        "Topic :: System",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
    ],
    test_suite='tests'
)
