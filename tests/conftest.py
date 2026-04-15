import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_sapko.db")
os.environ.setdefault("SECRET_KEY", "test-secret")

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/register", json={
        "email": "alice@test.rs",
        "password": "Test12345!",
        "full_name": "Alice",
        "city": "Beograd",
    })
    resp = client.post(
        "/api/auth/login",
        data={"username": "alice@test.rs", "password": "Test12345!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
