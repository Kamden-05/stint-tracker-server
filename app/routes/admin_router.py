import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import (
    DbSessionDep,
    create_api_key,
    require_admin,
    generate_api_key,
    hash_key,
)
from app.models import ApiKey
from app.repositories import api_crud
from app.schemas import ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, ApiKeyUpdate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)]
)


def get_key(key_id: int, db: DbSessionDep) -> ApiKey:
    key = api_crud.get_one(db, ApiKey.id == key_id)

    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"api key with id={key_id} not found",
        )

    return key


KeyDep = Annotated[ApiKey, Depends(get_key)]


@router.get("/api-keys", response_model=list[ApiKeyRead])
def get_keys(db: DbSessionDep):
    keys = api_crud.get_many(db)

    return keys


@router.post("/api-keys", response_model=ApiKeyCreateResponse)
def post_key(payload: ApiKeyCreate, db: DbSessionDep):
    return create_api_key(db, payload.name)


@router.patch("/api-keys/{key_id}/revoke", response_model=ApiKeyRead)
def revoke_key(key: KeyDep, db: DbSessionDep):

    key = api_crud.update(db, key, {"active": False})

    return key


@router.patch("/api-keys/{key_id}/activate", response_model=ApiKeyRead)
def activate_key(key: KeyDep, db: DbSessionDep):

    key = api_crud.update(db, key, {"active": True})

    return key


@router.patch("/api-keys/{key_id}/role", response_model=ApiKeyRead)
def update_key(key: KeyDep, key_update: ApiKeyUpdate, db: DbSessionDep):

    updated_key = api_crud.update(db, key, key_update.model_dump(exclude_unset=True))

    return updated_key


@router.post("/api-keys/{key_id}/rotate", response_model=ApiKeyCreateResponse)
def rotate_key(key: KeyDep, db: DbSessionDep):
    raw_key = generate_api_key()
    key_hash = hash_key(raw_key)

    updated_key = api_crud.update(db, key, {"key_hash": key_hash})

    return updated_key
