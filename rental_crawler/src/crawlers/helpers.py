from typing import Optional
import random
from playwright.sync_api import ProxySettings

from config import PROXY_IP_PORTS, PROXY_USERNAME, PROXY_PASSWORD
from .user_agent import USER_AGENTS


def get_playwright_proxy() -> Optional[ProxySettings]:
    """Get a proxy for Playwright."""

    if PROXY_IP_PORTS and PROXY_USERNAME and PROXY_PASSWORD:
        proxy_address = random.choice(PROXY_IP_PORTS)
        return ProxySettings(
            server=f"http://{proxy_address}",
            username=PROXY_USERNAME,
            password=PROXY_PASSWORD
        )


def get_requests_proxy() -> Optional[dict]:
    """Get a proxy for requests."""

    if PROXY_IP_PORTS and PROXY_USERNAME and PROXY_PASSWORD:
        proxy_address = random.choice(PROXY_IP_PORTS)
        return {
            "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{proxy_address}",
            # "https": f"https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{proxy_address}"
        }


def get_random_user_agent() -> str:
    """Get a random user agent from a list."""

    return random.choice(USER_AGENTS)["useragent"]
