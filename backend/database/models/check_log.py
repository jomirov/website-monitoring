from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from pydantic import BaseModel

class Check_log(Base):
    __tablename__ = "check_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    website_id: Mapped[int] = mapped_column(ForeignKey("websites.id"), nullable=False)
    status_code: Mapped[int]
    response_time_ms: Mapped[int]
    is_up: Mapped[bool]
    checked_at: Mapped[datetime] = mapped_column(DateTime)
