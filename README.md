# Šapko API

Backend for **Šapko** — a pet adoption and urgent aid platform for Serbia/Balkans.

Built with FastAPI + SQLAlchemy + PostgreSQL (SQLite for local dev).

## Quick start (Windows)

```bash
python -m venv venv
venv/Scripts/pip.exe install -r requirements.txt
cp .env.example .env
venv/Scripts/uvicorn.exe app.main:app --reload
venv/Scripts/uvicorn.exe app.main:app --reload 2>&1 &
```

Open http://localhost:8000/docs

Default admin: `admin@sapko.rs` / `ChangeMe123!`

## Features (MVP)

1. **Adoption listings** — dogs & cats available for adoption
2. **Urgent blood donor matching** — find compatible donors by blood group + location
3. **Donor registry** — pet owners register healthy pets as blood donors
4. **Urgent help board** — food donations, lost pets, injured strays, medical fundraising

See `CLAUDE.md` for full API reference.
# sapko-api
