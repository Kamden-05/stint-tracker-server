from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.models import BaseModel
from contextlib import contextmanager

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="127.0.0.1",
    port="5432",
    password="portland25",
    database="test",
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
