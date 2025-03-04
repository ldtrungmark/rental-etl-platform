import os
from typing import List
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker


# Logging settings
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'DEBUG')

# Selenium settings
HEADLESS: bool = bool(os.getenv("HEADLESS", "0").upper() in ("1", "TRUE"))

# Celery settings
CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "pyamqp://guest@localhost//")
CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")

# Database settings
MIN_POOL_SIZE: int = int(os.environ.get('MIN_POOL_SIZE', 5))
MAX_POOL_SIZE: int = int(os.environ.get('MAX_POOL_SIZE', 50))
MONGO_URI: str = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/dummy')
MONGO_DB_NAME: str = os.environ.get('MONGO_DB_NAME', 'dummy')
POSTGRES_URI: str = os.environ.get('POSTGRES_URI', 'postgresql://dummy:dummy@localhost:5432/dummy')
_mongo_client_pool: MongoClient = MongoClient(MONGO_URI, minPoolSize=MIN_POOL_SIZE, maxPoolSize=MAX_POOL_SIZE)
mongodb: MongoDatabase = _mongo_client_pool[MONGO_DB_NAME]
_postgres_engine: Engine = create_engine(POSTGRES_URI,poolclass=QueuePool,pool_size=MIN_POOL_SIZE,
                                max_overflow=MAX_POOL_SIZE-MIN_POOL_SIZE)
session_maker: sessionmaker = sessionmaker(bind=_postgres_engine)

# PROXY settings
PROXY_IP_PORTS: List[str] = os.environ.get('PROXY_IP_PORTS', '').split(',') or [] # Example: '89.0.142.86:8080,89.0.142.86:8080'
PROXY_USERNAME: str = os.environ.get('PROXY_USERNAME', '')
PROXY_PASSWORD: str = os.environ.get('PROXY_PASSWORD', '')

# Telegram settings
TELEGRAM_BOT_TOKEN: str = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID: int = int(os.environ.get('TELEGRAM_CHAT_ID', '0'))
