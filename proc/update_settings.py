
IDENTIFIERS_ENDPOINT = 'http://200.136.72.162:7000/api/v1/article/identifiers'

ARTICLE_ENDPOINT = 'http://200.136.72.162:7000/api/v1/article'

SOLR_INDEX_URL =  'http://localhost:8080/solr/scielo-articles'

IDENTIFIERS_LIMIT = 1000

try:
    from update_settings_local import *
except ImportError:
    pass