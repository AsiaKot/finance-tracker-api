import pytest

pytestmark = pytest.mark.asyncio

async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "secretpassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data

async def test_register_duplicate_email(client):
    await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "secretpassword123"
    })
    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "differentpassword"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

async def test_login_success(client):
    await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "secretpassword123"
    })
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "secretpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "secretpassword123"
    })
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

async def test_login_nonexistent_user(client):
    response = await client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "secretpassword123"
    })
    assert response.status_code == 401