# Šapko API — Claude Instructions

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite (local dev) / PostgreSQL (prod)
- **ORM**: SQLAlchemy 2.x
- **Auth**: JWT (access + refresh tokens) via python-jose, bcrypt via passlib
- **Validation**: Pydantic v2

## Start Server (Windows)
```bash
python -m venv venv
venv/Scripts/pip.exe install -r requirements.txt
cp .env.example .env
venv/Scripts/uvicorn.exe app.main:app --reload
```

## User Roles
| Role | Description |
|------|-------------|
| `admin` | Full access, moderation, user management |
| `shelter` | Verified shelter — can post adoption listings and urgent requests |
| `vet` | Verified vet — can see donor registry, post urgent blood requests |
| `user` | Default — can adopt, register donor pets, post urgent aid |

## API Surface

- `POST /api/auth/register` — self-register (role `user`)
- `POST /api/auth/login` · `POST /api/auth/refresh` · `PUT /api/auth/change-password` · `GET /api/auth/me`
- `GET|PUT /api/users/me`
- `GET|POST /api/pets`, `GET|PUT|DELETE /api/pets/{id}`, `POST /api/pets/{id}/photos`
- `GET|POST /api/adoption`, `GET|PUT|DELETE /api/adoption/{id}`
- `GET|POST /api/donors`, `GET /api/donors/mine`, `PUT|DELETE /api/donors/{id}`
- `GET|POST /api/urgent`, `GET|PUT|DELETE /api/urgent/{id}`, `POST /api/urgent/{id}/photos`
- `GET|POST /api/messages`, `GET /api/messages/inbox`, `/sent`, `PUT /api/messages/{id}/read`
- `GET /api/admin/users`, `PUT /api/admin/users/{id}/verify|role`, `PUT /api/admin/urgent|adoption/{id}/close`

## Key Files
- `app/main.py` — app entry, CORS, static uploads, admin seed
- `app/config.py` — pydantic-settings, reads `.env`
- `app/database.py` — SQLAlchemy engine/session (SQLite or PostgreSQL)
- `app/dependencies.py` — auth deps (`get_current_user`, `require_admin`, `require_admin_or_vet`)
- `app/services/auth.py` — JWT + bcrypt helpers
- `app/services/storage.py` — image upload (JPEG/PNG/WebP, max 8MB)
- `app/services/email.py` — SMTP sender (stubs to log if unconfigured)
- `app/services/matching.py` — blood-donor matching + notification

## Blood Matching Rules
- Dogs: DEA 1.1- is universal donor; DEA 1.1+ recipient accepts + and -
- Cats: must match exactly (A, B); AB recipients can accept A or B
- Donors with `UNKNOWN` blood group are always included — vets can test on demand

## Default Admin
- Email: `admin@sapko.rs`
- Password: `ChangeMe123!` (seeded on first startup)

## Known Issues
- **passlib + bcrypt 5.x incompatibility**: pin `bcrypt<4.1` in requirements.txt
