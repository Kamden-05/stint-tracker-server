from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreate(BaseModel):
    name: str
    is_admin: bool = False


class ApiKeyRead(BaseModel):
    id: int
    name: str
    is_admin: bool
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreateResponse(BaseModel):
    api_key: str


class ApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    is_admin: Optional[bool] = Field(default=None)

    model_config = ConfigDict(extra="forbid")
