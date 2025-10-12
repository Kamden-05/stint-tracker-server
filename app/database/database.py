from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.models import BaseModel
from contextlib import contextmanager
from app.config import settings

url = URL.create(
    drivername=settings.POSTGRES_DRIVER_NAME,
    username=settings.POSTGRES_USERNAME,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB,
)

engine = create_engine(url, echo=True)
BaseModel.metadata.create_all(engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

"""For use in FastAPI dependency injections"""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""For non FastAPI usage"""


@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
