from sqlalchemy import create_engine
from .base_class import Base

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all()
