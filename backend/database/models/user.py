from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import Date
from .base import Base
from datetime import date
from pydantic import BaseModel, EmailStr, Field

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[date] = mapped_column(Date)

    websites: Mapped[list["Website"]] = relationship("Website", back_populates="user")

class UserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)