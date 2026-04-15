from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.pet import Species
from app.models.urgent import UrgentRequest, UrgentType, UrgentStatus
from app.models.photo import UrgentRequestPhoto
from app.schemas.urgent import (
    UrgentRequestCreate, UrgentRequestUpdate, UrgentRequestResponse, UrgentRequestPhotoResponse,
)
from app.dependencies import get_current_user
from app.services.storage import save_upload
from app.services.matching import notify_donors_of_request
from app.config import get_settings

router = APIRouter(prefix="/api/urgent", tags=["urgent"])
settings = get_settings()


@router.get("", response_model=List[UrgentRequestResponse])
def list_urgent(
    db: Annotated[Session, Depends(get_db)],
    type_filter: Optional[UrgentType] = Query(None, alias="type"),
    species: Optional[Species] = None,
    city: Optional[str] = None,
    status_filter: Optional[UrgentStatus] = Query(None, alias="status"),
    limit: int = 50,
    offset: int = 0,
):
    q = db.query(UrgentRequest)
    if type_filter:
        q = q.filter(UrgentRequest.type == type_filter)
    if species:
        q = q.filter(UrgentRequest.species == species)
    if city:
        q = q.filter(UrgentRequest.city == city)
    if status_filter:
        q = q.filter(UrgentRequest.status == status_filter)
    else:
        q = q.filter(UrgentRequest.status == UrgentStatus.OPEN)
    return q.order_by(UrgentRequest.created_at.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=UrgentRequestResponse, status_code=status.HTTP_201_CREATED)
def create_urgent(
    data: UrgentRequestCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    req = UrgentRequest(author_id=current_user.id, **data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)

    # Fire-and-log: notify matching donors when a blood request is created.
    if req.type == UrgentType.BLOOD:
        try:
            notify_donors_of_request(req, db, settings.frontend_url)
        except Exception:
            pass

    return req


@router.get("/{request_id}", response_model=UrgentRequestResponse)
def get_urgent(request_id: str, db: Annotated[Session, Depends(get_db)]):
    req = db.query(UrgentRequest).filter(UrgentRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zahtev nije pronađen")
    return req


@router.put("/{request_id}", response_model=UrgentRequestResponse)
def update_urgent(
    request_id: str,
    data: UrgentRequestUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    req = db.query(UrgentRequest).filter(UrgentRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zahtev nije pronađen")
    if req.author_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    db.commit()
    db.refresh(req)
    return req


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_urgent(
    request_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    req = db.query(UrgentRequest).filter(UrgentRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zahtev nije pronađen")
    if req.author_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")
    db.delete(req)
    db.commit()


@router.post("/{request_id}/photos", response_model=UrgentRequestPhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_urgent_photo(
    request_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    req = db.query(UrgentRequest).filter(UrgentRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zahtev nije pronađen")
    if req.author_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nije dozvoljeno")

    url = await save_upload(file, subdir=f"urgent/{req.id}")
    next_order = db.query(UrgentRequestPhoto).filter(UrgentRequestPhoto.request_id == req.id).count()
    photo = UrgentRequestPhoto(request_id=req.id, url=url, sort_order=next_order)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo
