from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.pet import Pet
from app.models.photo import PetPhoto
from app.schemas.pet import PetCreate, PetUpdate, PetResponse, PetPhotoResponse
from app.dependencies import get_current_user
from app.services.storage import save_upload

router = APIRouter(prefix="/api/pets", tags=["pets"])


def _get_owned_pet(pet_id: str, user: User, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ljubimac nije pronađen")
    if pet.owner_id != user.id and user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    return pet


@router.get("", response_model=List[PetResponse])
def list_my_pets(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return db.query(Pet).filter(Pet.owner_id == current_user.id).order_by(Pet.created_at.desc()).all()


@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(
    data: PetCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    pet = Pet(owner_id=current_user.id, **data.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: str, db: Annotated[Session, Depends(get_db)]):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ljubimac nije pronađen")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id: str,
    data: PetUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    pet = _get_owned_pet(pet_id, current_user, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    pet = _get_owned_pet(pet_id, current_user, db)
    db.delete(pet)
    db.commit()


@router.post("/{pet_id}/photos", response_model=PetPhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_pet_photo(
    pet_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pet = _get_owned_pet(pet_id, current_user, db)
    url = await save_upload(file, subdir=f"pets/{pet.id}")
    next_order = db.query(PetPhoto).filter(PetPhoto.pet_id == pet.id).count()
    photo = PetPhoto(pet_id=pet.id, url=url, sort_order=next_order)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.delete("/{pet_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_photo(
    pet_id: str,
    photo_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    _get_owned_pet(pet_id, current_user, db)
    photo = db.query(PetPhoto).filter(PetPhoto.id == photo_id, PetPhoto.pet_id == pet_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fotografija nije pronađena")
    db.delete(photo)
    db.commit()
