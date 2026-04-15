from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.pet import Species, Sex, Size


class PetPhotoResponse(BaseModel):
    id: str
    url: str
    sort_order: int

    class Config:
        from_attributes = True


class PetBase(BaseModel):
    species: Species
    name: str
    age_years: Optional[int] = None
    sex: Optional[Sex] = None
    breed: Optional[str] = None
    size: Optional[Size] = None
    weight_kg: Optional[float] = None
    description: Optional[str] = None
    vaccinated: bool = False
    neutered: bool = False


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    age_years: Optional[int] = None
    sex: Optional[Sex] = None
    breed: Optional[str] = None
    size: Optional[Size] = None
    weight_kg: Optional[float] = None
    description: Optional[str] = None
    vaccinated: Optional[bool] = None
    neutered: Optional[bool] = None


class PetResponse(PetBase):
    id: str
    owner_id: str
    created_at: datetime
    photos: List[PetPhotoResponse] = []

    class Config:
        from_attributes = True
