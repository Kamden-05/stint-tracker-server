from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.logger import get_logger
from app.models import Base

logger = get_logger(__name__)

url = URL.create(
    drivername=settings.POSTGRES_DRIVER_NAME,
    username=settings.POSTGRES_USERNAME,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB,
)

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
