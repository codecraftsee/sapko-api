import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.config import get_settings

settings = get_settings()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 8 * 1024 * 1024


async def save_upload(file: UploadFile, subdir: str) -> str:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Samo JPEG, PNG ili WebP slike su dozvoljene")

    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slika je prevelika (max 8MB)")

    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[file.content_type]
    base_dir = Path(settings.upload_dir) / subdir
    base_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    path = base_dir / filename
    path.write_bytes(contents)
    return f"/uploads/{subdir}/{filename}"
