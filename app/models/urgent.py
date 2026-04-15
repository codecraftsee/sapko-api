import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.pet import Species


class UrgentType(str, PyEnum):
    BLOOD = "blood"
    FOOD_DONATION = "food_donation"
    LOST_PET = "lost_pet"
    INJURED_STRAY = "injured_stray"
    MEDICAL_FUNDRAISING = "medical_fundraising"
    OTHER = "other"


class UrgentStatus(str, PyEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    CLOSED = "closed"


class UrgentRequest(Base):
    __tablename__ = "urgent_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(UrgentType), nullable=False, index=True)
    species = Column(Enum(Species), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(UrgentStatus), nullable=False, default=UrgentStatus.OPEN, index=True)
    contact_phone = Column(String(50), nullable=True)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    photos = relationship("UrgentRequestPhoto", back_populates="request", cascade="all, delete-orphan", order_by="UrgentRequestPhoto.sort_order")
