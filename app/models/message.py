import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    to_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject = Column(String(200), nullable=True)
    body = Column(Text, nullable=False)
    related_listing_id = Column(String(36), ForeignKey("adoption_listings.id", ondelete="SET NULL"), nullable=True)
    related_request_id = Column(String(36), ForeignKey("urgent_requests.id", ondelete="SET NULL"), nullable=True)
    read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
