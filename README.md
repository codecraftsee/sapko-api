# Šapko API

Backend for **Šapko** — a pet adoption and urgent aid platform for Serbia/Balkans.

Built with FastAPI + SQLAlchemy + PostgreSQL (SQLite for local dev).

## Quick start (Docker)

```bash
docker compose up --build
```

Open http://localhost:8001/docs. Set `API_PORT` to use another host port.

Compose runs a local SQLite database in the `sapko-data` volume, and reloads when files in `app/` change. It disables Resend and Supabase, so emails are logged and uploads stay in the volume.

## Quick start (Windows)

```bash
python -m venv venv
venv/Scripts/pip.exe install -r requirements.txt
cp .env.example .env
venv/Scripts/uvicorn.exe app.main:app --reload --port 8001
venv/Scripts/uvicorn.exe app.main:app --reload --port 8001 2>&1 &
```

Open http://localhost:8001/docs

Default admin: `admin@sapko.rs` / `ChangeMe123!`

## Features (MVP)

1. **Adoption listings** — dogs & cats available for adoption
2. **Urgent blood donor matching** — find compatible donors by blood group + location
3. **Donor registry** — pet owners register healthy pets as blood donors
4. **Urgent help board** — food donations, lost pets, injured strays, medical fundraising

See `CLAUDE.md` for full API reference.
# sapko-api
