from typing import List, Dict, Optional, Any, Tuple
import time
from datetime import datetime, timedelta
from airflow.decorators import dag, task

from scripts.commons import logger
from scripts.config import mongodb
from scripts.database import postgres
from scripts.helpers.datetime import get_unix_timestamp_of_day


POST_NHATOT_COLLECTION = "raw_nhatot_search_posts"
RENTAL_SCHEMA = "rental"
ACCOUNT_TABLE = f"{RENTAL_SCHEMA}.account"
RENTAL_TABLE = f"{RENTAL_SCHEMA}.rental"


@dag(
    dag_id='etl_posts_nhatot_to_dwh',
    description='ETL DAG to transfer data rental Nhatot from MongoDB to PostgreSQL',
    default_args={
        "depends_on_past": False,
        "email": ["oo.nino193@gmail.com"],
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        'start_date': datetime(2025, 2, 1),
    },
    schedule_interval='@daily',
    catchup=False,
    tags=['nhatot']
)
def etl_posts_nhatot_to_dwh():
    """ETL DAG to transfer data rental Nhatot from MongoDB to PostgreSQL."""
    @task
    def extract_posts_nhatot(from_unix_timestamp: int) -> List[Optional[Dict[str, Any]]]:
        """Extract data from MongoDB."""

        logger.info(f"ETL posts nhatot with updated_at>={updated_at}")
        query = {"updated_at": {"$gte": from_unix_timestamp}}
        data = list(mongodb[POST_NHATOT_COLLECTION].find(query, {"_id": 0}))
        if not data:
            logger.warning(f"Not found data with updated_at >= {from_unix_timestamp}")

        return data

    @task
    def transform_posts_nhatot(raw_data: List[Optional[Dict[str, Any]]]) -> Dict[str, list]:
        """
        Transform data from MongoDB to match PostgreSQL schema.
        """
        rental_data = []
        account_data = {}

        for record in raw_data:
            account_id = record["account_id"]
            if account_id not in account_data:
                account_data[account_id] = {
                    "account_id": account_id,
                    "account_name": record.get("account_name", ""),
                    "full_name": record.get("full_name", ""),
                }

            address = record.get("address", "")
            if not address:
                address = record.get("street_number", "") + " " + record.get("street_name", "")
                address = address.strip()

            rental_data.append({
                "list_id": record["list_id"],
                "account_id": account_id,
                "average_rating": record.get("average_rating", 0),
                "category": record.get("category", 0),
                "category_name": record.get("category_name", ""),
                "list_time": record.get("list_time", 0),
                "price": record.get("price", 0),
                "size_unit": record.get("size_unit", 0),
                "size_unit_string": record.get("size_unit_string", ""),
                "type": record.get("type", ""),
                "area_name": record.get("area_name", ""),
                "region_name": record.get("region_name", ""),
                "address": address,
            })

        logger.info(f"Transformed {len(rental_data)} rental records & {len(account_data)} accounts")
        return {
            'account_data': list(account_data.values()),
            'rental_data': rental_data
        }

    @task
    def load_posts_nhatot(account_data: list, rental_data: list):
        """Load data into PostgreSQL."""
        account_query = """
        INSERT INTO rental.account (account_id, account_name, full_name)
        VALUES (:account_id, :account_name, :full_name)
        ON CONFLICT (account_id) DO NOTHING;
        """
        postgres.execute(account_query, account_data)

        rental_query = """
        INSERT INTO rental.rental (
            list_id, account_id, average_rating, category, category_name,
            list_time, price, size_unit, size_unit_string, type,
            area_name, region_name, address
        ) VALUES (
            :list_id, :account_id, :average_rating, :category, :category_name,
            :list_time, :price, :size_unit, :size_unit_string, :type,
            :area_name, :region_name, :address
        )
        ON CONFLICT (list_id) DO NOTHING;
        """
        postgres.execute(rental_query, rental_data)

    # updated_at = get_unix_timestamp_of_day()
    updated_at = int(datetime(2025, 2, 1).timestamp())
    raw_data = extract_posts_nhatot(from_unix_timestamp=updated_at)
    transformed_data = transform_posts_nhatot(raw_data)
    logger.info("Load data into PostgreSQL")
    load_posts_nhatot(transformed_data['account_data'], transformed_data['rental_data'])


etl_posts_nhatot_to_dwh_dag = etl_posts_nhatot_to_dwh()
