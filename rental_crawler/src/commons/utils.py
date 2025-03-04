from typing import Any
import time
from functools import wraps

from .logger import logger


def retry(n_attempts: int=3, delay: int=2):
    """Decorator to retry a function n_attempts times with a delay between each attempt."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(n_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1}/{n_attempts} failed: {e}")
                    if attempt < n_attempts - 1:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator


def get_json_value(json_data: dict, path: str) -> Any:
    """Get the value of a key in a JSON object using a dot notation path.

    Args:
        json_data (dict): The JSON object.
        path (str): The dot notation path to the key.

    Returns:
        Any: The value of the key or None if the key does not exist.
    """

    if not isinstance(json_data, dict):
        return None

    keys = path.split(".")
    value = json_data

    try:
        for key in keys:
            if key.isdigit():
                key = int(key)
                value = value[key]
            else:
                value = value[key]
        return value
    except (KeyError, IndexError, TypeError):
        return None


def save_file(file_path: str, content: str) -> bool:
    """Save content to a file.

    Args:
        file_path (str): The path to the file.
        content (str): The content to be saved.

    Returns:
        bool: True if the file is saved successfully, False otherwise.
    """

    try:
        with open(file_path, "w") as f:
            f.write(content)
        return True
    except Exception:
        return False
