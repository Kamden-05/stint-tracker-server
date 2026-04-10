import hashlib
import secrets
from typing import Optional

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


def validate_api_key(db: DbSessionDep, raw_key: str) -> Optional[ApiKey]:
    key_hash = hash_key(raw_key)

    # pylint: disable=singleton-comparison
    return api_crud.get_one(db, ApiKey.key_hash == key_hash, ApiKey.active.is_(True))
