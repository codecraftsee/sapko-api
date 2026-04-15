from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    to_user_id: str
    subject: Optional[str] = None
    body: str
    related_listing_id: Optional[str] = None
    related_request_id: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    from_user_id: str
    to_user_id: str
    subject: Optional[str] = None
    body: str
    related_listing_id: Optional[str] = None
    related_request_id: Optional[str] = None
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True
