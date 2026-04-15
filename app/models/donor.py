import uuid
from datetime import datetime, date
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Date, Enum, ForeignKey
from app.database import Base


class BloodGroup(str, PyEnum):
    # Dogs — DEA 1.1 system
    DEA_1_1_POS = "DEA_1_1+"
    DEA_1_1_NEG = "DEA_1_1-"
    # Cats — AB system
    A = "A"
    B = "B"
    AB = "AB"
    UNKNOWN = "unknown"


class DonorRegistration(Base):
    __tablename__ = "donor_registrations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pet_id = Column(String(36), ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, unique=True)
    blood_group = Column(Enum(BloodGroup), nullable=False, default=BloodGroup.UNKNOWN, index=True)
    last_donation_date = Column(Date, nullable=True)
    consent = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
