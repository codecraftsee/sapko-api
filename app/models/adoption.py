import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from app.database import Base


class AdoptionStatus(str, PyEnum):
    OPEN = "open"
    ADOPTED = "adopted"
    CLOSED = "closed"


class AdoptionListing(Base):
    __tablename__ = "adoption_listings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pet_id = Column(String(36), ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    status = Column(Enum(AdoptionStatus), nullable=False, default=AdoptionStatus.OPEN, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
