import pytest

from crawlers.nhatot.crawler import NhatotCrawler


@pytest.fixture
def crawler():
    return NhatotCrawler()


def test_get_posts_by_url_search():
    ...