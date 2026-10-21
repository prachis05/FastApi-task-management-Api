import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False}
)

session=sessionmaker(autoflush=False,bind=engine)


def getDb():
    db = session()
    try:
        yield db
    finally:
        db.close()