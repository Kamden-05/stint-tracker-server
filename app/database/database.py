from sqlalchemy import create_engine
from app.models import BaseModel

engine = create_engine("sqlite://", echo=True)
BaseModel.metadata.create_all(engine)
