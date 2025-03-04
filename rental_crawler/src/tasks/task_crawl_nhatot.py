from constant import CRAWL_QUEUE_NAME, LIMIT_CRAWL
from commons import celery_app
from etl import NhatotCrawlerETL

etl_crawler = NhatotCrawlerETL()


@celery_app.task(queue=CRAWL_QUEUE_NAME)
def crawl_posts_by_api_url(url: str, limit: int = LIMIT_CRAWL):
    etl_crawler.crawl_posts_by_url_api(url, limit)
