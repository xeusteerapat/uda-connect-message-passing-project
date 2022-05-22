import os

from sqlalchemy import create_engine
from sqlalchemy.ext import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

SQL_ALCHEMY_DB_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}" \
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQL_ALCHEMY_DB_URI)
Base = declarative_base()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
