"""
Seed script — populates urgent requests with realistic Serbian data.

Usage:
    venv/Scripts/python.exe scripts/seed_urgent.py
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

# Extra users that will post urgent requests (vet + regular users)
EXTRA_USERS = [
    {
        "email": "dr.jovic@sapko.rs",
        "full_name": "Dr. Marija Jović",
        "phone": "064-111-2233",
        "city": "Beograd",
        "role": UserRole.VET,
    },
    {
        "email": "petar.nikolic@example.com",
        "full_name": "Petar Nikolić",
        "phone": "065-333-4455",
        "city": "Novi Sad",
        "role": UserRole.USER,
    },
    {
        "email": "ana.stojanovic@example.com",
        "full_name": "Ana Stojanović",
        "phone": "066-555-6677",
        "city": "Niš",
        "role": UserRole.USER,
    },
    {
        "email": "jovana.markovic@example.com",
        "full_name": "Jovana Marković",
        "phone": "063-777-8899",
        "city": "Kragujevac",
        "role": UserRole.USER,
    },
]

now = datetime.utcnow()

URGENT_REQUESTS = [
    # Blood requests
    {
        "author_email": "dr.jovic@sapko.rs",
        "type": UrgentType.BLOOD,
        "species": Species.DOG,
        "title": "Hitno potrebna krv za psa — DEA 1.1-",
        "description": (
            "Labrador meštanac, 4 godine, hitno potrebna transfuzija nakon saobraćajne nesreće. "
            "Krvna grupa DEA 1.1-. Molimo vlasnike kompatibilnih pasa da se jave što pre. "
            "Pas je na Veterinarskoj klinici Čukarica."
        ),
        "city": "Beograd",
        "deadline": now + timedelta(days=1),
        "contact_phone": "064-111-2233",
        "extra_data": {"blood_group": "DEA 1.1-", "clinic": "VK Čukarica"},
    },
    {
        "author_email": "dr.jovic@sapko.rs",
        "type": UrgentType.BLOOD,
        "species": Species.CAT,
        "title": "Potrebna krv za mačku — krvna grupa A",
        "description": (
            "Mačka, 3 godine, potrebna transfuzija zbog anemije uzrokovane parazitima. "
            "Krvna grupa A. Primaoci su u ordinaciji Dr. Jović, Novi Beograd."
        ),
        "city": "Beograd",
        "deadline": now + timedelta(hours=36),
        "contact_phone": "064-111-2233",
        "extra_data": {"blood_group": "A", "clinic": "Ordinacija Dr. Jović"},
    },
    # Injured strays
    {
        "author_email": "petar.nikolic@example.com",
        "type": UrgentType.INJURED_STRAY,
        "species": Species.DOG,
        "title": "Povređen pas kod Riblje pijace — Novi Sad",
        "description": (
            "Pronašao sam povređenog psa ispred Riblje pijace na Limanu. Pas šepa na prednju levu nogu, "
            "verovatno prelom. Pas je miran ali uplašen. Potrebna pomoć za transport do veterinara ili "
            "neko ko može da ga privremeno zbrine."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(hours=12),
        "contact_phone": "065-333-4455",
        "extra_data": {"location": "Riblja pijaca, Liman, Novi Sad"},
    },
    {
        "author_email": "ana.stojanovic@example.com",
        "type": UrgentType.INJURED_STRAY,
        "species": Species.CAT,
        "title": "Povređena mačka na Bulevaru — Niš",
        "description": (
            "Mačka sa vidljivim povredama leži pored kontejnera na Bulevaru Zorana Đinđića. "
            "Dišće ali ne može da ustane. Ako neko može da pomogne ili zna veterinara koji dolazi na teren, "
            "molim da se javi."
        ),
        "city": "Niš",
        "deadline": now + timedelta(hours=6),
        "contact_phone": "066-555-6677",
        "extra_data": {"location": "Bulevar Zorana Đinđića, kod br. 45"},
    },
    # Lost pets
    {
        "author_email": "jovana.markovic@example.com",
        "type": UrgentType.LOST_PET,
        "species": Species.DOG,
        "title": "Izgubio se pas — Šarplaninac, Kragujevac",
        "description": (
            "Naš pas Vuk (Šarplaninac, 5 godina, siv, oko 40kg) pobegao je sinoć sa Aerodromskog naselja. "
            "Ima plavu ogrlicu sa privezkom. Veoma voli ljude. Molimo sve koji ga vide da pozovu ili "
            "odvedu u najbliži azil."
        ),
        "city": "Kragujevac",
        "deadline": now + timedelta(days=7),
        "contact_phone": "063-777-8899",
        "extra_data": {"pet_name": "Vuk", "breed": "Šarplaninac", "color": "siv", "chip": "941000024123456"},
    },
    {
        "author_email": "petar.nikolic@example.com",
        "type": UrgentType.LOST_PET,
        "species": Species.CAT,
        "title": "Nestala mačka — bela sa crnim flekama, Novi Sad",
        "description": (
            "Naša mačka Snežana (bela sa crnim flekama, sterilisana, 2 godine) nestala je sa terase "
            "na Bulevaru Oslobođenja. Veoma je plašljiva, skloniće se pod auto ili u žbunje. "
            "Nagrađujemo za informaciju."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(days=14),
        "contact_phone": "065-333-4455",
        "extra_data": {"pet_name": "Snežana", "color": "bela sa crnim flekama"},
    },
    # Food donations
    {
        "author_email": "ana.stojanovic@example.com",
        "type": UrgentType.FOOD_DONATION,
        "species": None,
        "title": "Potrebna hrana za azil — Niš",
        "description": (
            "Azil u Nišu prima donacije hrane za pse i mačke. Trenutno imamo 80 pasa i 30 mačaka. "
            "Prihvatamo suvu i konzervisanu hranu svih vrsta. Donacije možete doneti lično ili "
            "dogovoriti preuzimanje. Hvala svima koji pomognu!"
        ),
        "city": "Niš",
        "deadline": None,
        "contact_phone": "018-345-6789",
        "extra_data": {"address": "Industrijska zona bb, Niš", "working_hours": "08-16h radnim danima"},
    },
    # Medical fundraising
    {
        "author_email": "jovana.markovic@example.com",
        "type": UrgentType.MEDICAL_FUNDRAISING,
        "species": Species.DOG,
        "title": "Prikupljamo sredstva za operaciju — pas Garo",
        "description": (
            "Naš pas Garo (Husky mešanac, 3 godine) ima tumor na slezini koji zahteva hitnu operaciju. "
            "Trošak operacije je 85.000 din. Do sada smo skupili 30.000 din. Svaka pomoć je dobrodošla. "
            "Uplatu možete izvršiti na račun 160-123456789-01, poziv na broj: GARO2024."
        ),
        "city": "Kragujevac",
        "deadline": now + timedelta(days=21),
        "contact_phone": "063-777-8899",
        "extra_data": {
            "target_amount": 85000,
            "collected_amount": 30000,
            "bank_account": "160-123456789-01",
            "reference": "GARO2024",
        },
    },
    # Other
    {
        "author_email": "petar.nikolic@example.com",
        "type": UrgentType.OTHER,
        "species": Species.DOG,
        "title": "Traži se privremeni smeštaj za 2 psa — Novi Sad",
        "description": (
            "Zbog hitne hospitalizacije vlasnika, potreban privremeni dom za dva psa — "
            "Zlatni retriver Lesi (ženka, 4g) i mali mešanac Deki (mužjak, 6g). "
            "Oba su vakcinisana, kastrirana i navikla na život u stanu. Period: 2-4 nedelje."
        ),
        "city": "Novi Sad",
        "deadline": now + timedelta(days=3),
        "contact_phone": "065-333-4455",
        "extra_data": {"duration": "2-4 nedelje", "num_pets": 2},
    },
]


def run():
    with Session(engine) as db:
        user_map: dict[str, str] = {}

        # Create extra users
        for u in EXTRA_USERS:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if existing:
                user_map[u["email"]] = existing.id
                print(f"  [skip] user already exists: {u['email']}")
                continue

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
            user_map[u["email"]] = user.id
            print(f"  [+] user ({u['role']}): {u['email']}")

        # Create urgent requests
        for r in URGENT_REQUESTS:
            author_id = user_map[r["author_email"]]

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
            print(f"  [+] urgent [{r['type'].value}]: {r['title'][:50].encode('ascii', 'replace').decode()}...")

        db.commit()
        print("\nSeed uspešan!")
        print("\nNalozi (lozinka: Test123!):")
        for u in EXTRA_USERS:
            print(f"  {u['email']} ({u['role']})")


if __name__ == "__main__":
    print("Seeding urgent requests...\n")
    run()
