#!/bin/sh
# Index shell script


./index.sh xml/scielo_articles.xml localhost solr/scielo-articles

./commit.sh localhost solr/scielo-articles
