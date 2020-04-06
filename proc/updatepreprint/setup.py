#!/usr/bin/env python
import os
from setuptools import setup

setup(
    name="UpdateSearch",
    version='1.1.2',
    description="Process article to Solr",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    url="https://github.com/scieloorg/search-journals/tree/beta/proc/updatesolr",
    keywords='solr api lucene scielo',
    maintainer_email='atta.jamil@gmail.com',
    classifiers=[
        "Topic :: System",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
    ],
    test_suite='tests'
)
