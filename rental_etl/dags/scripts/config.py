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
