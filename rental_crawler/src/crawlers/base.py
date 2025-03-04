from typing import Optional
from playwright.sync_api import sync_playwright, ProxySettings
from playwright_stealth import stealth_sync
from urllib.parse import urlencode, urljoin
from requests import Response, request

from config import HEADLESS
from constant import MAX_RETRIES, WAIT_TIME
from commons.utils import retry
from . import helpers


class BaseCrawler:
    def build_url(self, base_url: str, params: dict) -> str:
        """
        Build URL with query string.

        Args:
            base_url (str): Base URL.
            params (dict): Query string parameters.

        Returns:
            str: URL with query string.
        """

        query_string = urlencode(params)
        return urljoin(base_url, "?" + query_string) if query_string else base_url

    def lauch_scroll_all_pages(self, url: str) -> str:
        """
        Launch a browser and scroll all pages of a website.

        Args:
            url (str): Website URL.

        Returns:
            str: HTML content of the website.
        """

        with sync_playwright() as p:
            user_agent = helpers.get_random_user_agent()
            proxy: Optional[ProxySettings] = helpers.get_playwright_proxy()
            print("user_agent:", user_agent)
            print("proxy_playwright:", proxy)
            browser = p.chromium.launch(headless=HEADLESS, proxy=proxy)
            context = browser.new_context(user_agent=user_agent)
            page = context.new_page()
            stealth_sync(page)
            page.goto(url)

            previous_height = None
            while True:
                page.wait_for_timeout(3000)
                current_height = page.evaluate("document.body.scrollHeight")
                if previous_height == current_height:
                    break
                previous_height = current_height
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            content = page.content()
            browser.close()

            return content

    @retry(n_attempts=MAX_RETRIES, delay=WAIT_TIME)
    def send_request(self, method: str, url: str, **kwargs) -> Response:
        """
        Send a HTTP request.

        Args:
            method (str): HTTP method.
            url (str): URL.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: HTTP response.
        """

        response = request(method, url, **kwargs)
        response.raise_for_status()
        return response
