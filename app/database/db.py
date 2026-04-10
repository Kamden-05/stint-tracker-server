import logging
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

logger = logging.getLogger(__name__)

load_dotenv()
url = os.environ["TEST_DB"]

try:
    engine = create_engine(url)
    logger.info("Database engine created successfully")
except:
    logger.exception("Failed to create database engine")
    raise

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    """For use in FastAPI dependency injections"""
    db = SessionLocal()
    logger.debug("FastAPI DB Session started")
    try:
        yield db
    finally:
        db.close()
        logger.debug("FastAPI DB Session closed")


@contextmanager
def get_db_context():
    """For non FastAPI usage"""
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
