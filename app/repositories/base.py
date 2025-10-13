from typing import Type, TypeVar, Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logger import get_logger
from app.models import Base

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.name = model.__name__

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ModelType]:
        logger.debug(f"Retrieving record for {self.model.__name__}")
        return db.execute(select(self.model).where(**kwargs))

    def create(self, db: Session, obj: CreateSchemaType) -> Base:
        logger.debug(
            f"Creating record for {self.model.__name__} with data {obj.model_dump()}"
        )

        data = obj.model_dump(by_alias=True)
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj: UpdateSchemaType) -> Base:

        logger.debug(
            f"Creating record for {self.model.__name__} with data {obj.model_dump()}"
        )

        data = obj.model_dump(by_alias=True, exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
