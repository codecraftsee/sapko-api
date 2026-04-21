from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any
from app.models.urgent import UrgentType, UrgentStatus
from app.models.pet import Species
from app.schemas.user import UserPublic


class UrgentRequestPhotoResponse(BaseModel):
    id: str
    url: str
    sort_order: int

    class Config:
        from_attributes = True


class UrgentRequestCreate(BaseModel):
    type: UrgentType
    species: Optional[Species] = None
    title: str
    description: str
    city: str
    deadline: Optional[datetime] = None
    contact_phone: Optional[str] = None
    extra_data: Optional[dict[str, Any]] = None


class UrgentRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[UrgentStatus] = None
    contact_phone: Optional[str] = None
    extra_data: Optional[dict[str, Any]] = None


class UrgentRequestResponse(BaseModel):
    id: str
    author_id: str
    type: UrgentType
    species: Optional[Species] = None
    title: str
    description: str
    city: str
    deadline: Optional[datetime] = None
    status: UrgentStatus
    contact_phone: Optional[str] = None
    extra_data: Optional[dict[str, Any]] = None
    created_at: datetime
    photos: List[UrgentRequestPhotoResponse] = []
    author: Optional[UserPublic] = None

    class Config:
        from_attributes = True
