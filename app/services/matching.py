import logging
from typing import List
from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.models.user import User
from app.models.donor import DonorRegistration, BloodGroup
from app.models.urgent import UrgentRequest, UrgentType
from app.services.email import send_email

logger = logging.getLogger(__name__)


# Compatible donor blood groups for each recipient group.
# Dogs: DEA 1.1- is universal donor; DEA 1.1+ can only receive +.
# Cats: must match exactly (A, B, AB) — no universal donor.
BLOOD_COMPAT = {
    BloodGroup.DEA_1_1_POS: [BloodGroup.DEA_1_1_POS, BloodGroup.DEA_1_1_NEG],
    BloodGroup.DEA_1_1_NEG: [BloodGroup.DEA_1_1_NEG],
    BloodGroup.A: [BloodGroup.A],
    BloodGroup.B: [BloodGroup.B],
    BloodGroup.AB: [BloodGroup.AB, BloodGroup.A, BloodGroup.B],
}


def find_matching_donors(request: UrgentRequest, db: Session) -> List[DonorRegistration]:
    if request.type != UrgentType.BLOOD or request.species is None:
        return []

    requested_group = (request.extra_data or {}).get("blood_group") if request.extra_data else None
    compat_groups = []
    if requested_group:
        try:
            bg = BloodGroup(requested_group)
            compat_groups = BLOOD_COMPAT.get(bg, [])
        except ValueError:
            compat_groups = []

    q = (
        db.query(DonorRegistration)
        .join(Pet, DonorRegistration.pet_id == Pet.id)
        .join(User, Pet.owner_id == User.id)
        .filter(
            DonorRegistration.active.is_(True),
            DonorRegistration.consent.is_(True),
            Pet.species == request.species,
        )
    )

    if compat_groups:
        q = q.filter(DonorRegistration.blood_group.in_([g.value for g in compat_groups] + [BloodGroup.UNKNOWN.value]))

    # Prioritize same city, but include all matches — vets can travel short distances.
    return q.all()


def notify_donors_of_request(request: UrgentRequest, db: Session, frontend_url: str) -> int:
    donors = find_matching_donors(request, db)
    notified = 0
    request_url = f"{frontend_url.rstrip('/')}/urgentno/{request.id}"

    for donor in donors:
        pet = db.query(Pet).filter(Pet.id == donor.pet_id).first()
        if not pet:
            continue
        owner = db.query(User).filter(User.id == pet.owner_id).first()
        if not owner or not owner.email:
            continue

        subject = f"Hitno: potreban donor krvi za {request.species.value} u {request.city}"
        body = (
            f"Poštovani/a,\n\n"
            f"Vaš ljubimac {pet.name} je registrovan kao donor krvi na Šapko platformi.\n\n"
            f"Hitno se traži donor krvi:\n"
            f"- Vrsta: {request.species.value}\n"
            f"- Grad: {request.city}\n"
            f"- Opis: {request.title}\n\n"
            f"Ako možete da pomognete, posetite: {request_url}\n\n"
            f"Hvala Vam od srca.\n"
            f"— Šapko"
        )
        try:
            send_email(owner.email, subject, body)
            notified += 1
        except Exception as e:
            logger.error(f"Failed to notify donor {owner.email}: {e}")

    return notified
