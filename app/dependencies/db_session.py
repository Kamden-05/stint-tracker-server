from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.db import get_db

DbSessionDep = Annotated[Session, Depends(get_db)]
