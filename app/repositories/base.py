from sqlalchemy.orm import Session
from app.models import Base
from typing import Type

class CRUDRepository:

    def __init__(self, model: Type[Base]):
        self.

    def create(self, db: Session, obj)