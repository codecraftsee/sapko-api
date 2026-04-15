import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from app.database import Base


class UserRole(str, PyEnum):
    ADMIN = "admin"
    SHELTER = "shelter"
    VET = "vet"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
