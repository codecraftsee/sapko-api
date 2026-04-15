from app.database import SessionLocal
from app.models.pet import Pet, Species
from app.models.user import User, UserRole
from app.models.donor import DonorRegistration, BloodGroup
from app.models.urgent import UrgentRequest, UrgentType
from app.services.auth import get_password_hash
from app.services.matching import find_matching_donors


def test_dog_universal_donor_matches_positive_request(client):
    db = SessionLocal()
    try:
        owner = User(email="donor@test.rs", password_hash=get_password_hash("x"), role=UserRole.USER, city="Beograd")
        db.add(owner); db.commit(); db.refresh(owner)

        pet = Pet(owner_id=owner.id, species=Species.DOG, name="Arči", age_years=4, weight_kg=30)
        db.add(pet); db.commit(); db.refresh(pet)

        reg = DonorRegistration(pet_id=pet.id, blood_group=BloodGroup.DEA_1_1_NEG, consent=True, active=True)
        db.add(reg); db.commit()

        req = UrgentRequest(
            author_id=owner.id, type=UrgentType.BLOOD, species=Species.DOG,
            title="Hitno", description="Treba krv", city="Beograd",
            extra_data={"blood_group": BloodGroup.DEA_1_1_POS.value},
        )
        db.add(req); db.commit(); db.refresh(req)

        matches = find_matching_donors(req, db)
        assert len(matches) == 1
        assert matches[0].pet_id == pet.id
    finally:
        db.close()


def test_cat_type_a_does_not_match_type_b_request(client):
    db = SessionLocal()
    try:
        owner = User(email="o@test.rs", password_hash=get_password_hash("x"), role=UserRole.USER)
        db.add(owner); db.commit(); db.refresh(owner)

        pet = Pet(owner_id=owner.id, species=Species.CAT, name="Mica", weight_kg=5)
        db.add(pet); db.commit(); db.refresh(pet)

        reg = DonorRegistration(pet_id=pet.id, blood_group=BloodGroup.A, consent=True, active=True)
        db.add(reg); db.commit()

        req = UrgentRequest(
            author_id=owner.id, type=UrgentType.BLOOD, species=Species.CAT,
            title="x", description="x", city="x",
            extra_data={"blood_group": BloodGroup.B.value},
        )
        db.add(req); db.commit(); db.refresh(req)

        assert find_matching_donors(req, db) == []
    finally:
        db.close()
