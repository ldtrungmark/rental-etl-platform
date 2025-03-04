MAX_RETRIES = 3
WAIT_TIME = 10
LIMIT_CRAWL = 100
CRAWL_QUEUE_NAME = 'rental_crawler'


class RequestMethod:
    GET = 'GET'
    POST = 'POST'


class MongoCollectionName:
    RAW_NHATOT_SEARCH_POSTS = 'raw_nhatot_search_posts'
    RAW_PHONGTRO123_SEARCH_POSTS = 'raw_phongtro123_search_posts'