from sqlalchemy import create_engine
from app.database.base_class import Base

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all()
