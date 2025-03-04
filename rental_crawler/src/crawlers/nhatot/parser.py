from bs4 import BeautifulSoup
import json
import time

from commons.utils import get_json_value
from .constant import SelectorPathBS4, DictPath


def parse_posts_by_url_search(html: str) -> list:
    """
    Parse posts from search page html.

    Args:
        html (str): HTML of search page.

    Returns:
        list: List of posts.
    """

    soup = BeautifulSoup(html, 'html.parser')

    script_tag = soup.find(**SelectorPathBS4.SEARCH_PAGE_POSTS)
    if not script_tag:
        raise ValueError(f"Cannot find script tag with {SelectorPathBS4.SEARCH_PAGE_POSTS}")

    tag_data = json.loads(script_tag.string.strip())
    posts = get_json_value(tag_data, DictPath.SEARCH_PAGE_POST) or []
    posts = [{**post, 'created_at': int(time.time())} for post in posts]

    return posts
