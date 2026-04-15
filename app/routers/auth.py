from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, TokenResponse, RefreshRequest, ChangePasswordRequest
from app.schemas.user import UserResponse
from app.services.auth import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token, decode_token,
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email već postoji")

    user = User(
        email=request.email,
        password_hash=get_password_hash(request.password),
        full_name=request.full_name,
        phone=request.phone,
        city=request.city,
        role=UserRole.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pogrešan email ili lozinka",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nalog je deaktiviran")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest, db: Annotated[Session, Depends(get_db)]):
    payload = decode_token(request.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    new_refresh = create_refresh_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh)


@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lozinke se ne poklapaju")
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trenutna lozinka nije tačna")
    current_user.password_hash = get_password_hash(request.new_password)
    db.commit()
    return {"message": "Lozinka uspešno promenjena"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
