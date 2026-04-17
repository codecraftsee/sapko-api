import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.config import get_settings

settings = get_settings()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 8 * 1024 * 1024


def _supabase_client():
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_key)


async def save_upload(file: UploadFile, subdir: str) -> str:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Samo JPEG, PNG ili WebP slike su dozvoljene")

    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slika je prevelika (max 8MB)")

    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[file.content_type]
    filename = f"{uuid.uuid4().hex}{ext}"

    if settings.supabase_url and settings.supabase_key:
        client = _supabase_client()
        path = f"{subdir}/{filename}"
        client.storage.from_(settings.supabase_bucket).upload(
            path,
            contents,
            {"content-type": file.content_type},
        )
        public_url = client.storage.from_(settings.supabase_bucket).get_public_url(path)
        return public_url

    # Local fallback
    base_dir = Path(settings.upload_dir) / subdir
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / filename).write_bytes(contents)
    return f"/uploads/{subdir}/{filename}"
