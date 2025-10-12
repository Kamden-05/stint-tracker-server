from sqlalchemy import ForeignKey, String, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from app.database.base_class import Base


class Lap(Base):
    __tablename__ = "Lap"

    lap_id: Mapped[int] = mapped_column(primary_key=True)
    stint_id: Mapped[int] = mapped_column(ForeignKey("stint.id"))
    number: Mapped[int]
    time: Mapped[float]
    incidents: Mapped[Optional[int]]
    start_position: Mapped[Optional[int]]
    end_position: Mapped[Optional[int]]
    pit: Mapped[Optional[bool]]
    created_at: Mapped[Optional[DateTime]] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[DateTime]] = mapped_column(TIMESTAMP(timezone=True))
