from pymongo import UpdateOne
from typing import Any
import time

from ..config import mongodb
from ..commons.logger import logger


def upsert_data(collection_name: str, data: list, key_compare: Any, only_insert_new: bool = False):
    """Upsert data to MongoDB collection.

    Args:
        collection_name (str): MongoDB collection name.
        data (list): List of data to upsert.
        key_compare (Any): Key to compare to find the document to update.

    Returns:
        None
    """

    if not data:
        return

    method_update = "$setOnInsert" if only_insert_new else "$set"
    operations = [
        UpdateOne(
            {key_compare: item[key_compare]},
            {method_update: {**item, 'updated_at': int(time.time())}},
            upsert=True
        )
        for item in data
    ]
    num_records = mongodb[collection_name].bulk_write(operations).upserted_count
    logger.debug(f"Upserted {num_records} records to {collection_name} collection")
    return num_records
