"""
Seed script — downloads placeholder photos for each pet and inserts PetPhoto rows.

Uses:
  - https://placedog.net  for dogs
  - https://placekitten.com  for cats

Usage:
    venv/Scripts/python.exe scripts/seed_pet_photos.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import urllib.request
from pathlib import Path
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.models.pet import Pet, Species
from app.models.photo import PetPhoto
from app.config import get_settings

Base.metadata.create_all(bind=engine)

settings = get_settings()
UPLOAD_DIR = Path(settings.upload_dir) / "pets"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Different sizes so images look distinct
DOG_SIZES = [
    (400, 300),
    (450, 320),
    (380, 280),
]
CAT_SIZES = [
    (400, 300),
    (420, 310),
    (360, 270),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}


def download_image(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"    [warn] download failed ({url}): {e}")
        return False


def photo_urls_for(species: Species, count: int = 2) -> list[str]:
    sizes = DOG_SIZES if species == Species.DOG else CAT_SIZES
    results = []
    for i in range(count):
        w, h = sizes[i % len(sizes)]
        # Use a unique random seed per call to get different images
        rand = uuid.uuid4().hex[:6]
        if species == Species.DOG:
            url = f"https://placedog.net/{w}/{h}?r={rand}"
        else:
            url = f"https://loremflickr.com/{w}/{h}/cat?random={rand}"
        results.append(url)
    return results


def run():
    with Session(engine) as db:
        pets = db.query(Pet).all()

        for pet in pets:
            existing = db.query(PetPhoto).filter(PetPhoto.pet_id == pet.id).count()
            if existing:
                name = pet.name.encode("ascii", "replace").decode()
                print(f"  [skip] {name} already has {existing} photo(s)")
                continue

            name = pet.name.encode("ascii", "replace").decode()
            print(f"  downloading photos for {name} ({pet.species.value})...")

            urls = photo_urls_for(pet.species, count=2)
            inserted = 0
            for order, url in enumerate(urls):
                filename = f"{uuid.uuid4().hex}.jpg"
                dest = UPLOAD_DIR / filename
                ok = download_image(url, dest)
                if not ok:
                    continue

                photo = PetPhoto(
                    id=str(uuid.uuid4()),
                    pet_id=pet.id,
                    url=f"/uploads/pets/{filename}",
                    sort_order=order,
                )
                db.add(photo)
                inserted += 1
                print(f"    [+] photo {order + 1}: /uploads/pets/{filename}")

            if inserted:
                db.flush()

        db.commit()
        print("\nSeed uspešan!")


if __name__ == "__main__":
    print("Seeding pet photos...\n")
    run()
