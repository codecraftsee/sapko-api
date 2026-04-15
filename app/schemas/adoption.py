from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.adoption import AdoptionStatus
from app.schemas.pet import PetResponse


class AdoptionListingCreate(BaseModel):
    pet_id: str
    city: str


class AdoptionListingUpdate(BaseModel):
    city: Optional[str] = None
    status: Optional[AdoptionStatus] = None


class AdoptionListingResponse(BaseModel):
    id: str
    pet_id: str
    city: str
    status: AdoptionStatus
    created_at: datetime
    pet: Optional[PetResponse] = None

    class Config:
        from_attributes = True
