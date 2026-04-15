from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.urgent import UrgentRequest, UrgentStatus
from app.models.adoption import AdoptionListing, AdoptionStatus
from app.schemas.user import UserResponse
from app.dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def list_users(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.put("/users/{user_id}/verify", response_model=UserResponse)
def verify_user(
    user_id: str,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Korisnik nije pronađen")
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


@router.put("/users/{user_id}/role", response_model=UserResponse)
def change_role(
    user_id: str,
    role: UserRole,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Korisnik nije pronađen")
    user.role = role
    db.commit()
    db.refresh(user)
    return user


@router.put("/urgent/{request_id}/close")
def close_urgent(
    request_id: str,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    req = db.query(UrgentRequest).filter(UrgentRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zahtev nije pronađen")
    req.status = UrgentStatus.CLOSED
    db.commit()
    return {"message": "ok"}


@router.put("/adoption/{listing_id}/close")
def close_adoption(
    listing_id: str,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    listing = db.query(AdoptionListing).filter(AdoptionListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oglas nije pronađen")
    listing.status = AdoptionStatus.CLOSED
    db.commit()
    return {"message": "ok"}
