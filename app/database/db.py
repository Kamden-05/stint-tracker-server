from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.logger import get_logger
from app.models import Base

import os

logger = get_logger(__name__)

url = os.environ["DATABASE_URL"]

try:
    engine = create_engine(url)
    logger.info("Database engine created successfully")
except:
    logger.exception("Failed to create database engine")
    raise

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

"""For use in FastAPI dependency injections"""


def get_db():
    db = SessionLocal()
    logger.debug("FastAPI DB Session started")
    try:
        yield db
    finally:
        db.close()
        logger.debug("FastAPI DB Session closed")


"""For non FastAPI usage"""


@contextmanager
def get_db_context():
    db = SessionLocal()
    logger.debug("DB Session Started")
    try:
        yield db
    except Exception:
        db.rollback()
        logger.exception("DB Session rolled back due to error")
        raise
    finally:
        db.close()
        logger.debug("DB session closed")
