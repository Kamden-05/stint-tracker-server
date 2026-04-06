from typing import Type, TypeVar, Optional, List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Base
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.name = model.__name__

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        logger.debug(f"Retrieving record for {self.model.__name__}")
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
            f"Retrieving records for {self.model.__name__} with skip {skip} and limit {limit}"
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

    def create(self, db: Session, obj: CreateSchemaType) -> Base:
        logger.debug(
            f"Creating record for {self.model.__name__} with data {obj.model_dump()}"
        )

        data = obj.model_dump(by_alias=True)
        db_obj = self.model(**data)
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except Exception as e:
            db.rollback()
            raise

        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj: UpdateSchemaType) -> Base:

        logger.debug(
            f"Updating record for {self.model.__name__} with data {obj.model_dump(exclude_unset=True)}"
        )

        data = obj.model_dump(by_alias=True, exclude_unset=True)

        for field, value in data.items():
            if field in ["session_id", "car_id"]:
                continue
            setattr(db_obj, field, value)

        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)
        except Exception as e:
            db.rollback()
            raise

        return db_obj
