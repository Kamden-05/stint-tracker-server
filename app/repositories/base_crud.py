import logging
from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Base

logger = logging.getLogger(__name__)

# pylint: disable=invalid-name
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.name = model.__name__

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        logger.debug("Retrieving record for model %s", self.model.__name__)
        filters = [
            *args,
            *[getattr(self.model, k) == v for k, v in kwargs.items() if v is not None],
        ]
        stmt = select(self.model).where(*filters)
        return db.scalars(stmt).first()

    def get_many(
        self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        logger.debug(
            "Retrieving records for %s with skip %s and limit %s",
            self.model.__name__,
            skip,
            limit,
        )
        filters = [
            *args,
            *[getattr(self.model, k) == v for k, v in kwargs.items() if v is not None],
        ]
        stmt = select(self.model).where(*filters).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    def get_by_composite(
        self, db: Session, session_id: int, car_id: int
    ) -> Optional[ModelType]:
        return self.get_one(db, session_id=session_id, car_id=car_id)

    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        try:
            db.commit()
            db.refresh(obj)
        except Exception:
            db.rollback()
            raise

        return obj

    def update(self, db: Session, db_obj: ModelType, data: dict) -> ModelType:

        for field, value in data.items():
            if field in ["session_id", "car_id"]:
                continue
            setattr(db_obj, field, value)

        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)
        except Exception:
            db.rollback()
            raise

        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return db_obj
