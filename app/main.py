import logging
import traceback
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.routers import auth, users, pets, adoption, donors, urgent, messages, admin
from app.database import engine, Base
from app.config import get_settings
from app.models import User
from app.models.user import UserRole
from app.services.auth import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Šapko API",
    description="Backend API for Šapko — pet adoption and urgent aid platform",
    version="0.1.0",
)


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"{request.method} {request.url.path} failed: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(status_code=500, content={"detail": str(exc)})


settings = get_settings()
origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists and serve it statically.
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(adoption.router)
app.include_router(donors.router)
app.include_router(urgent.router)
app.include_router(messages.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        admin_user = db.query(User).filter(User.email == "admin@sapko.rs").first()
        if not admin_user:
            db.add(User(
                email="admin@sapko.rs",
                password_hash=get_password_hash("ChangeMe123!"),
                role=UserRole.ADMIN,
                full_name="Admin",
                is_verified=True,
            ))
            db.commit()
            logger.info("Seeded default admin user: admin@sapko.rs / ChangeMe123!")


@app.get("/")
def root():
    return {"message": "Šapko API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
