import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError

load_dotenv()
DB_NAME = os.getenv("db_name") + ".db"

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "quote_scrap.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()


def check_database_exists():
    try:
        with engine.connect():
            return True
    except OperationalError:
        return False


def create_table(engine):
    Base.metadata.create_all(engine)
