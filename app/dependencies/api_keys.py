import hashlib
import secrets
from typing import Optional, Annotated

from fastapi import Depends, Header, HTTPException, status

from app.dependencies.db_session import DbSessionDep
from app.models import ApiKey
from app.repositories import api_crud


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def create_api_key(db: DbSessionDep, name: str) -> str:
    raw_key = generate_api_key()
    key_hash = hash_key(raw_key)

    api_key = ApiKey(key_hash=key_hash, name=name, active=True)

    api_crud.create(db, api_key)

    return raw_key


def validate_api_key(db: DbSessionDep, raw_key: str) -> ApiKey:
    key_hash = hash_key(raw_key)

    # pylint: disable=singleton-comparison
    api_key = api_crud.get_one(db, ApiKey.key_hash == key_hash, ApiKey.active == True)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return api_key


def get_api_key(
    db: DbSessionDep,
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> ApiKey:
    return validate_api_key(db, x_api_key)


def require_admin(api_key: ApiKey = Depends(get_api_key)) -> ApiKey:
    if not api_key.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return api_key


RequireAuthDep = Annotated[ApiKey, Depends(get_api_key)]
AdminDep = Annotated[ApiKey, Depends(require_admin)]
