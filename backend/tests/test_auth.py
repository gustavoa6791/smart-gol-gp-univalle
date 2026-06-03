"""Pruebas de autenticacion (HU-001, tarea QA #89)."""


def register_user(client, email="user@test.com", password="secret123", name="Test User"):
    return client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password},
    )


def test_register_creates_viewer(client):
    res = register_user(client)
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "user@test.com"
    assert body["role"] == "viewer"  # el registro publico nunca escala privilegios
    assert "hashed_password" not in body


def test_register_duplicate_email_fails(client):
    register_user(client)
    res = register_user(client)
    assert res.status_code == 400


def test_login_ok_returns_jwt(client):
    register_user(client)
    res = client.post("/api/auth/login", json={"email": "user@test.com", "password": "secret123"})
    assert res.status_code == 200
    body = res.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"].count(".") == 2  # estructura de un JWT


def test_login_wrong_password_is_401(client):
    register_user(client)
    res = client.post("/api/auth/login", json={"email": "user@test.com", "password": "wrong"})
    assert res.status_code == 401


def test_login_unknown_email_is_401(client):
    res = client.post("/api/auth/login", json={"email": "nope@test.com", "password": "secret123"})
    assert res.status_code == 401


def test_me_with_valid_token(client):
    register_user(client)
    token = client.post(
        "/api/auth/login", json={"email": "user@test.com", "password": "secret123"}
    ).json()["access_token"]
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "user@test.com"


def test_me_without_token_is_rejected(client):
    res = client.get("/api/auth/me")
    assert res.status_code in (401, 403)


def test_me_with_invalid_token_is_401(client):
    res = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401
