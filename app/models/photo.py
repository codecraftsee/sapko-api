import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PetPhoto(Base):
    __tablename__ = "pet_photos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pet_id = Column(String(36), ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="photos")


class UrgentRequestPhoto(Base):
    __tablename__ = "urgent_request_photos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String(36), ForeignKey("urgent_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("UrgentRequest", back_populates="photos")
