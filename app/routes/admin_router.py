import logging

from fastapi import APIRouter, HTTPException, status
from app.dependencies import AdminDep, DbSessionDep
from app.repositories import api_crud


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=AdminDep)


@router.get("/api-keys")
def get_api_keys(db: DbSessionDep):
    pass


@router.post("/api-keys")
def create_api_key():
    pass
