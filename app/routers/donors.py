from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.pet import Pet, Species
from app.models.donor import DonorRegistration, BloodGroup
from app.schemas.donor import DonorRegistrationCreate, DonorRegistrationUpdate, DonorRegistrationResponse
from app.dependencies import get_current_user, require_admin_or_vet

router = APIRouter(prefix="/api/donors", tags=["donors"])


@router.get("/mine", response_model=List[DonorRegistrationResponse])
def list_my_donors(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    regs = (
        db.query(DonorRegistration)
        .join(Pet, DonorRegistration.pet_id == Pet.id)
        .filter(Pet.owner_id == current_user.id)
        .all()
    )
    for r in regs:
        pet = db.query(Pet).filter(Pet.id == r.pet_id).first()
        r.pet = pet
        r.owner = db.query(User).filter(User.id == pet.owner_id).first() if pet else None
    return regs


@router.get("", response_model=List[DonorRegistrationResponse])
def list_donors(
    _admin_or_vet: Annotated[User, Depends(require_admin_or_vet)],
    db: Annotated[Session, Depends(get_db)],
    species: Optional[Species] = None,
    blood_group: Optional[BloodGroup] = None,
    city: Optional[str] = None,
    active_only: bool = True,
):
    q = db.query(DonorRegistration).join(Pet, DonorRegistration.pet_id == Pet.id).join(User, Pet.owner_id == User.id)
    if active_only:
        q = q.filter(DonorRegistration.active.is_(True), DonorRegistration.consent.is_(True))
    if species:
        q = q.filter(Pet.species == species)
    if blood_group:
        q = q.filter(DonorRegistration.blood_group == blood_group)
    if city:
        q = q.filter(User.city == city)
    regs = q.all()
    for r in regs:
        pet = db.query(Pet).filter(Pet.id == r.pet_id).first()
        r.pet = pet
        r.owner = db.query(User).filter(User.id == pet.owner_id).first() if pet else None
    return regs


@router.post("", response_model=DonorRegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_donor(
    data: DonorRegistrationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    pet = db.query(Pet).filter(Pet.id == data.pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ljubimac nije pronađen")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    if db.query(DonorRegistration).filter(DonorRegistration.pet_id == pet.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ljubimac je već registrovan kao donor")
    if not data.consent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saglasnost je obavezna")

    reg = DonorRegistration(
        pet_id=pet.id,
        blood_group=data.blood_group,
        last_donation_date=data.last_donation_date,
        consent=data.consent,
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)
    reg.pet = pet
    return reg


@router.put("/{registration_id}", response_model=DonorRegistrationResponse)
def update_donor(
    registration_id: str,
    data: DonorRegistrationUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    reg = db.query(DonorRegistration).filter(DonorRegistration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registracija nije pronađena")
    pet = db.query(Pet).filter(Pet.id == reg.pet_id).first()
    if pet.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reg, field, value)
    db.commit()
    db.refresh(reg)
    reg.pet = pet
    return reg


@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donor(
    registration_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    reg = db.query(DonorRegistration).filter(DonorRegistration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registracija nije pronađena")
    pet = db.query(Pet).filter(Pet.id == reg.pet_id).first()
    if pet.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    db.delete(reg)
    db.commit()
