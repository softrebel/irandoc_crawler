from src.lang import LANGS
from src.utils import *
DB_NAME='tmudb.sqlite'


BASE_API_URL='https://ganj.irandoc.ac.ir/api/v1'
RESOURCES={
    'search':'search/main',
    'articles':'articles',
    'abstract':'articles/{uuid}/show_abstract',
    'tags':'articles/{uuid}/show_tags',
    'additional_fields':'articles/{uuid}/show_additional_fields',
}
RESULTS_PER_PAGE={
    25:1,
    50:2,
    75:3,
    100:4
}




QUERY_PARAMS={
    "basicscope":5,
    "fulltext_status":1,
    "keywords":"",
    'results_per_page':RESULTS_PER_PAGE[25],
    'sort_by':1,
    'year_from':0,
    'year_to':1400,
    'page':1
}


ARTICLES=[]

LOCALE='fa'
LANG=LANGS[LOCALE]

SUPPORTED_EXTENSIONS={
    'csv':to_csv,
    'json':to_json
}


SLEEP_RANGE=(1,3)