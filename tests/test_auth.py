def test_register_and_login(client):
    r = client.post("/api/auth/register", json={
        "email": "bob@test.rs",
        "password": "Test12345!",
        "full_name": "Bob",
    })
    assert r.status_code == 201
    assert "access_token" in r.json()

    r2 = client.post(
        "/api/auth/login",
        data={"username": "bob@test.rs", "password": "Test12345!"},
    )
    assert r2.status_code == 200


def test_me(client, auth_headers):
    r = client.get("/api/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "alice@test.rs"


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "c@test.rs", "password": "Test12345!",
    })
    r = client.post("/api/auth/login", data={"username": "c@test.rs", "password": "wrong"})
    assert r.status_code == 401
