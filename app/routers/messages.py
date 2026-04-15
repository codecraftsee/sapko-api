from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.get("/inbox", response_model=List[MessageResponse])
def inbox(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return (
        db.query(Message)
        .filter(Message.to_user_id == current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )


@router.get("/sent", response_model=List[MessageResponse])
def sent(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return (
        db.query(Message)
        .filter(Message.from_user_id == current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send(
    data: MessageCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    recipient = db.query(User).filter(User.id == data.to_user_id).first()
    if not recipient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Primalac ne postoji")

    msg = Message(from_user_id=current_user.id, **data.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.put("/{message_id}/read", response_model=MessageResponse)
def mark_read(
    message_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    msg = db.query(Message).filter(
        Message.id == message_id,
        or_(Message.from_user_id == current_user.id, Message.to_user_id == current_user.id),
    ).first()
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poruka nije pronađena")
    msg.read = True
    db.commit()
    db.refresh(msg)
    return msg
