"""
Seed script — populates adoption listings with realistic Serbian data.

Usage:
    venv/Scripts/python.exe scripts/seed_adoption.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.models.user import User, UserRole
from app.models.pet import Pet, Species, Sex, Size
from app.models.adoption import AdoptionListing, AdoptionStatus
from app.services.auth import get_password_hash

Base.metadata.create_all(bind=engine)

SHELTERS = [
    {
        "email": "azil.beograd@sapko.rs",
        "full_name": "Azil Beograd",
        "phone": "011-123-4567",
        "city": "Beograd",
    },
    {
        "email": "azil.novisad@sapko.rs",
        "full_name": "Azil Novi Sad",
        "phone": "021-234-5678",
        "city": "Novi Sad",
    },
    {
        "email": "azil.nis@sapko.rs",
        "full_name": "Azil Niš",
        "phone": "018-345-6789",
        "city": "Niš",
    },
]

PETS = [
    # Beograd shelter pets
    {
        "shelter_email": "azil.beograd@sapko.rs",
        "species": Species.DOG,
        "name": "Šarko",
        "age_years": 3,
        "sex": Sex.MALE,
        "breed": "Mešanac",
        "size": Size.MEDIUM,
        "weight_kg": 18.5,
        "description": "Šarko je veseo i energičan pas koji voli igru i šetnje. Odlično se slaže sa decom i odraslima. Vakcinisan i čipovan.",
        "vaccinated": True,
        "neutered": True,
        "city": "Beograd",
    },
    {
        "shelter_email": "azil.beograd@sapko.rs",
        "species": Species.CAT,
        "name": "Luna",
        "age_years": 2,
        "sex": Sex.FEMALE,
        "breed": "Domaća kratkolasnа",
        "size": Size.SMALL,
        "weight_kg": 3.8,
        "description": "Luna je mirna i nežna mačka koja voli maženje. Idealna za stan. Sterilisana i vakcinisana.",
        "vaccinated": True,
        "neutered": True,
        "city": "Beograd",
    },
    {
        "shelter_email": "azil.beograd@sapko.rs",
        "species": Species.DOG,
        "name": "Rex",
        "age_years": 5,
        "sex": Sex.MALE,
        "breed": "Labrador mešanac",
        "size": Size.LARGE,
        "weight_kg": 32.0,
        "description": "Rex je lojalan i poslušan pas. Prošao osnovnu obuku, voli decu. Traži mirnu porodicu sa dvorištem.",
        "vaccinated": True,
        "neutered": False,
        "city": "Beograd",
    },
    {
        "shelter_email": "azil.beograd@sapko.rs",
        "species": Species.CAT,
        "name": "Miki",
        "age_years": 1,
        "sex": Sex.MALE,
        "breed": "Mešanac",
        "size": Size.SMALL,
        "weight_kg": 2.9,
        "description": "Miki je mlad i radoznao mačak, pun energije. Voli igračke i lovi sve što se miče. Vakcinisan.",
        "vaccinated": True,
        "neutered": True,
        "city": "Beograd",
    },
    # Novi Sad shelter pets
    {
        "shelter_email": "azil.novisad@sapko.rs",
        "species": Species.DOG,
        "name": "Bella",
        "age_years": 2,
        "sex": Sex.FEMALE,
        "breed": "Bigl mešanac",
        "size": Size.MEDIUM,
        "weight_kg": 14.0,
        "description": "Bella je živahna i pametna kujica koja se brzo uči. Voli trčanje i igru loptom. Vakcinisana i čipovana.",
        "vaccinated": True,
        "neutered": True,
        "city": "Novi Sad",
    },
    {
        "shelter_email": "azil.novisad@sapko.rs",
        "species": Species.CAT,
        "name": "Cica",
        "age_years": 4,
        "sex": Sex.FEMALE,
        "breed": "Persijanka mešanac",
        "size": Size.MEDIUM,
        "weight_kg": 4.5,
        "description": "Cica je staložena mačka koja voli mirnu sredinu. Odlična za starije vlasnike. Sterilisana i vakcinisana.",
        "vaccinated": True,
        "neutered": True,
        "city": "Novi Sad",
    },
    {
        "shelter_email": "azil.novisad@sapko.rs",
        "species": Species.DOG,
        "name": "Bruno",
        "age_years": 7,
        "sex": Sex.MALE,
        "breed": "Bokser mešanac",
        "size": Size.LARGE,
        "weight_kg": 28.0,
        "description": "Bruno je stariji pas koji traži dom za zasluženu penziju. Miran, nežan, voli duge šetnje.",
        "vaccinated": True,
        "neutered": True,
        "city": "Novi Sad",
    },
    # Niš shelter pets
    {
        "shelter_email": "azil.nis@sapko.rs",
        "species": Species.DOG,
        "name": "Tara",
        "age_years": 1,
        "sex": Sex.FEMALE,
        "breed": "Mešanac",
        "size": Size.SMALL,
        "weight_kg": 8.0,
        "description": "Tara je štenad koja traži svoju prvu porodicu. Vedra, voli ljude, idealna za porodicu sa decom.",
        "vaccinated": True,
        "neutered": False,
        "city": "Niš",
    },
    {
        "shelter_email": "azil.nis@sapko.rs",
        "species": Species.CAT,
        "name": "Tigrica",
        "age_years": 3,
        "sex": Sex.FEMALE,
        "breed": "Tabi mešanac",
        "size": Size.MEDIUM,
        "weight_kg": 3.5,
        "description": "Tigrica je nezavisna mačka sa šarmantnim karakterom. Voli sunčane prozore i mirne večeri.",
        "vaccinated": True,
        "neutered": True,
        "city": "Niš",
    },
    {
        "shelter_email": "azil.nis@sapko.rs",
        "species": Species.DOG,
        "name": "Max",
        "age_years": 4,
        "sex": Sex.MALE,
        "breed": "Nemački ovčar mešanac",
        "size": Size.LARGE,
        "weight_kg": 35.0,
        "description": "Max je zaštitarski pas koji je odlican čuvar. Potrebna iskusna ruka. Vakcinisan i čipovan.",
        "vaccinated": True,
        "neutered": False,
        "city": "Niš",
    },
]


def run():
    with Session(engine) as db:
        shelter_map: dict[str, str] = {}

        # Create shelter users
        for s in SHELTERS:
            existing = db.query(User).filter(User.email == s["email"]).first()
            if existing:
                shelter_map[s["email"]] = existing.id
                print(f"  [skip] shelter already exists: {s['email']}")
                continue

            user = User(
                id=str(uuid.uuid4()),
                email=s["email"],
                password_hash=get_password_hash("Shelter123!"),
                full_name=s["full_name"],
                phone=s["phone"],
                city=s["city"],
                role=UserRole.SHELTER,
                is_active=True,
                is_verified=True,
            )
            db.add(user)
            db.flush()
            shelter_map[s["email"]] = user.id
            print(f"  [+] shelter: {s['email']}")

        # Create pets + adoption listings
        created_at_offset = 0
        for p in PETS:
            owner_id = shelter_map[p["shelter_email"]]

            pet = Pet(
                id=str(uuid.uuid4()),
                owner_id=owner_id,
                species=p["species"],
                name=p["name"],
                age_years=p["age_years"],
                sex=p["sex"],
                breed=p["breed"],
                size=p["size"],
                weight_kg=p["weight_kg"],
                description=p["description"],
                vaccinated=p["vaccinated"],
                neutered=p["neutered"],
                created_at=datetime.utcnow() - timedelta(days=created_at_offset),
            )
            db.add(pet)
            db.flush()

            listing = AdoptionListing(
                id=str(uuid.uuid4()),
                pet_id=pet.id,
                city=p["city"],
                status=AdoptionStatus.OPEN,
                created_at=datetime.utcnow() - timedelta(days=created_at_offset),
            )
            db.add(listing)
            print(f"  [+] pet + oglas: {p['name']} ({p['species'].value}) — {p['city']}")
            created_at_offset += 1

        db.commit()
        print("\nSeed uspešan!")
        print("\nAzil nalozi (lozinka: Shelter123!):")
        for s in SHELTERS:
            print(f"  {s['email']}")


if __name__ == "__main__":
    print("Seeding adoption data...\n")
    run()
