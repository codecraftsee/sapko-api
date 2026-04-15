"""
Seed script — adds extra food_donation and medical_fundraising urgent requests.

Usage:
    venv/Scripts/python.exe scripts/seed_urgent_extra.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.models.user import User, UserRole
from app.models.urgent import UrgentRequest, UrgentType, UrgentStatus
from app.models.pet import Species
from app.services.auth import get_password_hash

Base.metadata.create_all(bind=engine)

EXTRA_USERS = [
    {
        "email": "milica.pavlovic@example.com",
        "full_name": "Milica Pavlovic",
        "phone": "062-100-2030",
        "city": "Subotica",
        "role": UserRole.USER,
    },
    {
        "email": "dr.tesla@sapko.rs",
        "full_name": "Dr. Nikola Tesla",
        "phone": "064-200-3040",
        "city": "Novi Sad",
        "role": UserRole.VET,
    },
    {
        "email": "azil.kragujevac@sapko.rs",
        "full_name": "Azil Kragujevac",
        "phone": "034-400-5060",
        "city": "Kragujevac",
        "role": UserRole.SHELTER,
    },
]

now = datetime.utcnow()

EXTRA_REQUESTS = [
    # ── HRANA (food_donation) ────────────────────────────────────────────────
    {
        "author_email": "azil.kragujevac@sapko.rs",
        "type": UrgentType.FOOD_DONATION,
        "species": None,
        "title": "Donacija hrane za azil Kragujevac — hitno",
        "description": (
            "Azil u Kragujevcu zbrinuo je 45 novih pasa nakon racije i hitno su nam potrebne "
            "zalihe hrane. Prihvatamo suvu hranu za pse i mace svih brendova. "
            "Mozete donirati direktno u azilu ili organizovati dostavu. "
            "Kontaktirajte nas pre dolaska."
        ),
        "city": "Kragujevac",
        "deadline": now + timedelta(days=5),
        "contact_phone": "034-400-5060",
        "extra_data": {
            "address": "Stari aerodrom bb, Kragujevac",
            "working_hours": "07-15h svakog dana",
            "needed_kg": 500,
        },
    },
    {
        "author_email": "milica.pavlovic@example.com",
        "type": UrgentType.FOOD_DONATION,
        "species": Species.CAT,
        "title": "Hrana za koloniju maca — Subotica centar",
        "description": (
            "Brinem o koloniji od 20 maca u centru Subotice. Ostala sam bez posla i tesko mi je "
            "da finansiram hranu sama. Ako imate viska suve ili konzervne hrane za mace, "
            "bila bih veoma zahvalna. Mogu da preuzmem ili dogovorimo dostavu."
        ),
        "city": "Subotica",
        "deadline": None,
        "contact_phone": "062-100-2030",
        "extra_data": {"colony_size": 20, "location": "Centar Subotice"},
    },
    {
        "author_email": "ana.stojanovic@example.com",
        "type": UrgentType.FOOD_DONATION,
        "species": Species.DOG,
        "title": "Zimske zalihe hrane za pse lutalice — Nis",
        "description": (
            "Udruženje volontera u Nisu organizuje zimsko hranjenje pasa lutalica. "
            "Tražimo donacije suve hrane, konzervi i grickalica. Sve donacije se dele "
            "direktno psima na terenu svakog jutra. Prikupljanje do kraja meseca."
        ),
        "city": "Nis",
        "deadline": now + timedelta(days=18),
        "contact_phone": "066-555-6677",
        "extra_data": {
            "organization": "Volonteri Nis",
            "distribution": "svako jutro 08h",
        },
    },
    {
        "author_email": "petar.nikolic@example.com",
        "type": UrgentType.FOOD_DONATION,
        "species": None,
        "title": "Potrebni kecevi i konzerve za mali privatni azil — Novi Sad",
        "description": (
            "Vodim mali privatni azil sa 12 pasa i 8 maca. Trenutno nemam finansija za hranu "
            "do sledece plate. Svaka pomoc je dobrodosla — hrana, poslastice, igracke. "
            "Dolazak po dogovoru, Futoski put, Novi Sad."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(days=10),
        "contact_phone": "065-333-4455",
        "extra_data": {
            "num_dogs": 12,
            "num_cats": 8,
            "address": "Futoski put, Novi Sad",
        },
    },
    # ── LECENJE (medical_fundraising) ────────────────────────────────────────
    {
        "author_email": "dr.tesla@sapko.rs",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.DOG,
        "title": "Operacija kicme za psa Boba — Novi Sad",
        "description": (
            "Bob je meštanac od 6 godina koji je dovezen kao povredeni lutalica. Dijagnoza: "
            "hernija diska L4-L5, potrebna hitna operacija kako ne bi ostao paralizovan. "
            "Trošak operacije i rehabilitacije: 120.000 din. Prikupljeno: 45.000 din. "
            "Uplata na racun 265-1234567890-11, poziv na broj: BOB2024."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(days=14),
        "contact_phone": "064-200-3040",
        "extra_data": {
            "target_amount": 120000,
            "collected_amount": 45000,
            "bank_account": "265-1234567890-11",
            "reference": "BOB2024",
            "diagnosis": "hernija diska L4-L5",
        },
    },
    {
        "author_email": "milica.pavlovic@example.com",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.CAT,
        "title": "Lecenje malijeg Dude od FIP — Subotica",
        "description": (
            "Moja macka Duda (1.5 godina) dijagnostikovana je sa FIP-om (Feline Infectious Peritonitis). "
            "Terapija antiviralem GS-441524 traje 12 nedelja i kosta 60.000 din. "
            "Molim za pomoc — svaki dinar je bitan. "
            "Racun: 170-9876543210-22, poziv: DUDA2024."
        ),
        "city": "Subotica",
        "deadline": now + timedelta(days=7),
        "contact_phone": "062-100-2030",
        "extra_data": {
            "target_amount": 60000,
            "collected_amount": 8000,
            "bank_account": "170-9876543210-22",
            "reference": "DUDA2024",
            "diagnosis": "FIP",
        },
    },
    {
        "author_email": "jovana.markovic@example.com",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.DOG,
        "title": "Hemoterapija za kujicu Roru — Kragujevac",
        "description": (
            "Rora je zlatni retriver od 7 godina kojoj je dijagnostikovana limfoma. "
            "Hemoterapija se sastoji od 6 ciklusa — ukupan trošak je 200.000 din. "
            "Rora je puna zivota i zasluzuje svakog dana. Pomozite nam da se bori! "
            "Uplata: 160-1122334455-33, poziv: RORA2024."
        ),
        "city": "Kragujevac",
        "deadline": now + timedelta(days=30),
        "contact_phone": "063-777-8899",
        "extra_data": {
            "target_amount": 200000,
            "collected_amount": 55000,
            "bank_account": "160-1122334455-33",
            "reference": "RORA2024",
            "diagnosis": "limfoma",
            "treatment_cycles": 6,
        },
    },
    {
        "author_email": "ana.stojanovic@example.com",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.CAT,
        "title": "Operacija bubrega za macku Persu — Nis",
        "description": (
            "Persa (persijanka, 9 godina) ima hronicnu bolest bubrega i potrebna joj je "
            "operacija uklanjanja kamenca uz dugotrajnu terapiju. Ukupni trošak: 75.000 din. "
            "Persa je stara dama koja zasluzuje dostojnu starost. "
            "Pomozite: 310-5566778899-44, poziv: PERSA2024."
        ),
        "city": "Nis",
        "deadline": now + timedelta(days=21),
        "contact_phone": "066-555-6677",
        "extra_data": {
            "target_amount": 75000,
            "collected_amount": 12000,
            "bank_account": "310-5566778899-44",
            "reference": "PERSA2024",
            "diagnosis": "hronicna bolest bubrega",
        },
    },
    {
        "author_email": "dr.tesla@sapko.rs",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.DOG,
        "title": "Proteza zadnje noge za psa Ace — Novi Sad",
        "description": (
            "Aca je meštanac od 4 godine koji je izgubio zadnju levu nogu u saobracajnoj nesreci. "
            "Potpuno je zdrav i vedar, ali mu je potrebna proteza kako bi mogao normalno da trci. "
            "Proteza i postavljanje: 95.000 din. "
            "Donacije na racun: 265-9988776655-55, poziv: ACA2024."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(days=45),
        "contact_phone": "064-200-3040",
        "extra_data": {
            "target_amount": 95000,
            "collected_amount": 22000,
            "bank_account": "265-9988776655-55",
            "reference": "ACA2024",
            "treatment": "proteza zadnje noge",
        },
    },
]


def get_or_create_user(db: Session, u: dict) -> str:
    existing = db.query(User).filter(User.email == u["email"]).first()
    if existing:
        print(f"  [skip] user already exists: {u['email']}")
        return existing.id

    user = User(
        id=str(uuid.uuid4()),
        email=u["email"],
        password_hash=get_password_hash("Test123!"),
        full_name=u["full_name"],
        phone=u["phone"],
        city=u["city"],
        role=u["role"],
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.flush()
    print(f"  [+] user ({u['role'].value}): {u['email']}")
    return user.id


def run():
    with Session(engine) as db:
        user_map: dict[str, str] = {}

        for u in EXTRA_USERS:
            user_map[u["email"]] = get_or_create_user(db, u)

        # Also load existing users by email so we can reference them
        existing_emails = [
            "petar.nikolic@example.com",
            "ana.stojanovic@example.com",
            "jovana.markovic@example.com",
        ]
        for email in existing_emails:
            if email not in user_map:
                user = db.query(User).filter(User.email == email).first()
                if user:
                    user_map[email] = user.id

        print()
        for r in EXTRA_REQUESTS:
            author_id = user_map.get(r["author_email"])
            if not author_id:
                print(f"  [skip] author not found: {r['author_email']}")
                continue

            req = UrgentRequest(
                id=str(uuid.uuid4()),
                author_id=author_id,
                type=r["type"],
                species=r["species"],
                title=r["title"],
                description=r["description"],
                city=r["city"],
                deadline=r["deadline"],
                status=UrgentStatus.OPEN,
                contact_phone=r["contact_phone"],
                extra_data=r["extra_data"],
            )
            db.add(req)
            label = r["title"][:50].encode("ascii", "replace").decode()
            print(f"  [+] [{r['type'].value}]: {label}...")

        db.commit()
        print("\nSeed uspešan!")
        print("\nNovi nalozi (lozinka: Test123!):")
        for u in EXTRA_USERS:
            print(f"  {u['email']} ({u['role'].value})")


if __name__ == "__main__":
    print("Seeding extra food_donation + medical_fundraising requests...\n")
    run()
