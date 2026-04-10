from pydantic import BaseModel


def build_model(schema: BaseModel, model_cls, exclude=None, **extra):
    data = schema.model_dump(exclude=exclude or {})
    return model_cls(**data, **extra)
