import requests
from functools import wraps

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from commons.logger import logger


def send_telegram_message(message: str):
    """Send message to Telegram chat."""
    if not TELEGRAM_BOT_TOKEN and not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)


def send_notify(only_failed: bool=False):
    """Decorator send message to Telegram chat."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                message = f"[SUCCESS] {func.__name__}:\n>> args={args}\n>> kwargs={kwargs}"
                return func(*args, **kwargs)
            except Exception as e:
                message = f"[ERROR] {func.__name__}:\n>> args={args}\n>> kwargs={kwargs}\n>> Reason: {str(e)}"
                logger.error(f'ERROR: {func.__name__} with message {str(e)}')
                return
            finally:
                if not only_failed or "[ERROR]" in message:
                    send_telegram_message(message)
        return wrapper
    return decorator
