import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Species(str, PyEnum):
    DOG = "dog"
    CAT = "cat"


class Sex(str, PyEnum):
    MALE = "male"
    FEMALE = "female"


class Size(str, PyEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Pet(Base):
    __tablename__ = "pets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    species = Column(Enum(Species), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    age_years = Column(Integer, nullable=True)
    sex = Column(Enum(Sex), nullable=True)
    breed = Column(String(100), nullable=True)
    size = Column(Enum(Size), nullable=True)
    weight_kg = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    vaccinated = Column(Boolean, default=False)
    neutered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    photos = relationship("PetPhoto", back_populates="pet", cascade="all, delete-orphan", order_by="PetPhoto.sort_order")
