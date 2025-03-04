from functools import cached_property
import time

from constant import LIMIT_CRAWL, MongoCollectionName
from commons import logger, notify
from database import mongodb
from crawlers.nhatot.crawler import NhatotCrawler


class NhatotCrawlerETL:
    @cached_property
    def nhatot_crawler(self):
        return NhatotCrawler()

    def get_posts_by_url_search(self, url: str, page_num: int, filter_by: int=None) -> int:
        """Get posts by url search and save raw data to MongoDB.

        Args:
            url (str): Url search.
            page_num (int): Page number.
            filter_by (int, optional): Filter by. Defaults to None.

        Returns:
            list: List of posts.
        """

        logger.info(f"Crawling posts from={url} with page={page_num}, filter={filter_by}")

        posts = self.nhatot_crawler.get_posts_by_url_search(url, page_num, filter_by)
        logger.info(f"Crawled {len(posts)} posts on page {page_num}")
        if not posts:
            raise ValueError(f"No posts found on page {page_num}")

        return mongodb.upsert_data(
            collection_name=MongoCollectionName.RAW_NHATOT_SEARCH_POSTS,
            data=posts,
            key_compare='list_id',
            only_insert_new=True
        )

    def crawl_posts_by_url_search(self, url: str, page_num: int, filter_by: int = None, limit: int = LIMIT_CRAWL):
        """Crawl posts by url search and save raw data to MongoDB.

        Args:
            url (str): Url search.
            page_num (int): Page number.
            filter_by (int, optional): Filter by. Defaults to None.
            limit (int, optional): Limit. Defaults to LIMIT_CRAWL.

        Returns:
            None: None.
        """

        logger.info(f"Crawling posts from={url} with from_page={page_num}, filter={filter_by}, limit={limit}")
        num_count = 1
        while num_count <= limit:
            if self.get_posts_by_url_search(url, page_num, filter_by) == 0:
                break

            page_num += 1
            num_count += 1
            time.sleep(10)

    @notify.send_notify(only_failed=True)
    def crawl_posts_by_url_api(self, url: str, limit: int = LIMIT_CRAWL):
        """Crawl posts by url API and save raw data to MongoDB.

        Args:
            url (str): Url API.
            limit (int, optional): Limit. Defaults to LIMIT_CRAWL.

        Returns:
            None: None.
        """

        logger.info(f"Crawling posts from={url}, limit={limit}")
        num_count = 1
        data = self.nhatot_crawler.get_posts_by_url_api(url)
        while num_count <= limit:
            raw_data = next(data, None)
            if not raw_data:
                logger.debug("Got None data, stop crawling")
                break

            count_insert = mongodb.upsert_data(
                collection_name=MongoCollectionName.RAW_NHATOT_SEARCH_POSTS,
                data=raw_data,
                key_compare='list_id',
                only_insert_new=True
            )
            if count_insert == 0:
                logger.debug(f"Inserted {count_insert} records, stop crawling")
                break

            num_count += 1
            time.sleep(15)
