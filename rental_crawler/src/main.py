def test_etl_crawler(url):
    from etl.etl_crawl_nhatot import NhatotCrawlerETL
    crawler = NhatotCrawlerETL()
    crawler.crawl_posts_by_url_api(url)


def test_task_crawler(url):
    from tasks import task_crawl_nhatot as crawl
    crawl.crawl_posts_by_api_url.delay(url)


if __name__ == '__main__':
    url = 'https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000&o=350&page=7&st=u%2Ch&limit=50&w=1&include_expired_ads=true&key_param_included=true'
    # test_task_crawler(url)
    test_etl_crawler(url)
