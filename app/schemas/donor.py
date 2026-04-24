from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from app.models.donor import BloodGroup
from app.schemas.pet import PetResponse
from app.schemas.user import UserPublic


class DonorRegistrationCreate(BaseModel):
    pet_id: str
    blood_group: BloodGroup = BloodGroup.UNKNOWN
    last_donation_date: Optional[date] = None
    consent: bool


class DonorRegistrationUpdate(BaseModel):
    blood_group: Optional[BloodGroup] = None
    last_donation_date: Optional[date] = None
    consent: Optional[bool] = None
    active: Optional[bool] = None


class DonorRegistrationResponse(BaseModel):
    id: str
    pet_id: str
    blood_group: BloodGroup
    last_donation_date: Optional[date] = None
    consent: bool
    active: bool
    created_at: datetime
    pet: Optional[PetResponse] = None
    owner: Optional[UserPublic] = None

    class Config:
        from_attributes = True
