from typing import Generator, List
from urllib.parse import parse_qs

from commons import logger
from constant import RequestMethod
from crawlers.base import BaseCrawler
from crawlers.nhatot.constant import SearchFilter
from crawlers.nhatot.parser import parse_posts_by_url_search
from crawlers.helpers import get_random_user_agent, get_requests_proxy


class NhatotCrawler(BaseCrawler):
    def get_headers(self):
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'ct-fingerprint': '',
            'ct-platform': 'web',
            'origin': 'https://www.nhatot.com',
            'priority': 'u=1, i',
            'referer': 'https://www.nhatot.com/',
            # 'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': get_random_user_agent(),
        }

    def get_posts_by_url_search(self, url: str, page_num: int, filter_by: int = None) -> list:
        """Get posts by url search.

        Example: You want to get posts from https://www.nhatot.com/thue-phong-tro-tp-ho-chi-minh?page=1&sp=6
            - url: https://www.nhatot.com/thue-phong-tro-tp-ho-chi-minh
            - page_num: 1
            - filter_by: SearchFilter.LOWEST_PRICE

        Args:
            url (str): Url to search posts.
            page_num (int): Page number to get posts.
            filter_by (int, optional): Filter by price. Defaults to None.

        Returns:
            list: List of posts.
        """

        params = {
            "page": page_num,
            "sp": filter_by or SearchFilter.NEWEST
        }
        url = self.build_url(url, params)
        logger.debug(f"Get posts by url search: {url}")
        html_page =self.lauch_scroll_all_pages(url)

        return parse_posts_by_url_search(html_page)

    def get_posts_by_url_api(self, url: str) -> Generator[List[dict], None, None]:
        """Get posts by url API.

        Example: 'https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000&o=150&page=3&st=u,h&limit=50&w=1&include_expired_ads=true&key_param_included=true'

        Args:
            url (str): Url to get posts.

        Yields:
            Generator[list, None, None]: List of posts.
        """

        items = url.split('?')
        if len(items) == 1:
            logger.error(f"Invalid url: {url}")
            return

        url = items[0]
        query_params = parse_qs(items[1])
        query_params = {k: v[0] if len(v) == 1 else ",".join(v) for k, v in query_params.items()}
        page_num = int(query_params.get('page', 1))
        offset = int(query_params.get('o', 0))
        limit = int(query_params.get('limit', 50))
        while True:
            query_params.update({
                'o': str(offset),
                'limit': str(limit),
                'page': str(page_num),
            })
            headers=self.get_headers()
            proxies=get_requests_proxy()
            logger.debug(f"Get posts by url API: {url} with params: {query_params}")
            response = self.send_request(
                method=RequestMethod.GET,
                url=url,
                headers=headers,
                proxies=proxies,
                params=query_params,
            )
            yield response.json()['ads']

            offset += limit
            page_num += 1
