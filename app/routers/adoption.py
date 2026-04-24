from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.pet import Pet, Species
from app.models.adoption import AdoptionListing, AdoptionStatus
from app.schemas.adoption import AdoptionListingCreate, AdoptionListingUpdate, AdoptionListingResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/adoption", tags=["adoption"])


@router.get("", response_model=List[AdoptionListingResponse])
def list_adoptions(
    db: Annotated[Session, Depends(get_db)],
    species: Optional[Species] = None,
    city: Optional[str] = None,
    status_filter: Optional[AdoptionStatus] = Query(None, alias="status"),
    limit: int = 50,
    offset: int = 0,
):
    query = db.query(AdoptionListing).join(Pet, AdoptionListing.pet_id == Pet.id)
    if species:
        query = query.filter(Pet.species == species)
    if city:
        query = query.filter(AdoptionListing.city == city)
    if status_filter:
        query = query.filter(AdoptionListing.status == status_filter)
    else:
        query = query.filter(AdoptionListing.status == AdoptionStatus.OPEN)
    listings = query.order_by(AdoptionListing.created_at.desc()).offset(offset).limit(limit).all()
    # Eager load pet + owner for response
    result = []
    for l in listings:
        pet = db.query(Pet).filter(Pet.id == l.pet_id).first()
        l.pet = pet
        l.owner = db.query(User).filter(User.id == pet.owner_id).first() if pet else None
        result.append(l)
    return result


@router.post("", response_model=AdoptionListingResponse, status_code=status.HTTP_201_CREATED)
def create_adoption(
    data: AdoptionListingCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    pet = db.query(Pet).filter(Pet.id == data.pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ljubimac nije pronađen")
    if pet.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")

    listing = AdoptionListing(pet_id=pet.id, city=data.city)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    listing.pet = pet
    listing.owner = db.query(User).filter(User.id == pet.owner_id).first()
    return listing


@router.get("/{listing_id}", response_model=AdoptionListingResponse)
def get_adoption(listing_id: str, db: Annotated[Session, Depends(get_db)]):
    listing = db.query(AdoptionListing).filter(AdoptionListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oglas nije pronađen")
    pet = db.query(Pet).filter(Pet.id == listing.pet_id).first()
    listing.pet = pet
    listing.owner = db.query(User).filter(User.id == pet.owner_id).first() if pet else None
    return listing


@router.put("/{listing_id}", response_model=AdoptionListingResponse)
def update_adoption(
    listing_id: str,
    data: AdoptionListingUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    listing = db.query(AdoptionListing).filter(AdoptionListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oglas nije pronađen")
    pet = db.query(Pet).filter(Pet.id == listing.pet_id).first()
    if pet.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)
    db.commit()
    db.refresh(listing)
    listing.pet = pet
    return listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_adoption(
    listing_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    listing = db.query(AdoptionListing).filter(AdoptionListing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oglas nije pronađen")
    pet = db.query(Pet).filter(Pet.id == listing.pet_id).first()
    if pet.owner_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    db.delete(listing)
    db.commit()
