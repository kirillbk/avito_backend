from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import String

from uuid import UUID
from datetime import datetime


class Employee(Base):
    __tablename__ = "employee"
    
    id: Mapped[UUID] = mapped_column(server_default=func.gen_random_uuid(), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    updated_at:Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
