from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import Base
from typing import Type, TypeVar
from app.logger import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.name = model.__name__

    def create(self, db: Session, obj: CreateSchemaType) -> Base:
        logger.debug(
            f"Creating record for {self.model.__name__} with data {obj.model_dump()}"
        )

        data = obj.model_dump()
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj: UpdateSchemaType) -> Base:

        logger.debug(
            f"Creating record for {self.model.__name__} with data {obj.model_dump()}"
        )

        data = obj.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
