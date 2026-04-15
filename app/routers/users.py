from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
