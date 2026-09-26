from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from pydantic import BaseModel, HttpUrl


class Website(Base):
    __tablename__ = "websites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    url: Mapped[str]
    check_interval: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool]

    user: Mapped["User"] = relationship("User", back_populates="websites")

class WebsiteRequest(BaseModel):
    name: str
    url: HttpUrl

class UpdateValues(BaseModel):
    check_interval: int
    is_active: bool