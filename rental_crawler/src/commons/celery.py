from celery import Celery
from celery.schedules import crontab

from constant import CRAWL_QUEUE_NAME
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery(
    "rental_etl",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['tasks', 'crawlers', 'etl']
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
celery_app.conf.task_queues = {
    CRAWL_QUEUE_NAME: {"exchange": "crawler_exchange", "routing_key": "rental_etl"},
}

celery_app.conf.beat_schedule = {
    'crawl-posts-daily': {
        'task': 'tasks.task_crawl_nhatot.crawl_posts_by_api_url',
        'schedule': crontab(hour=0, minute=0), # daily
        'args': ('https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000&o=0&page=0&st=u%2Ch&limit=50&w=1&include_expired_ads=true&key_param_included=true')
    },
}