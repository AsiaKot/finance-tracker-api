import pytest

pytestmark = pytest.mark.asyncio

async def register_and_login(client, email="test@example.com", password="secretpassword123"):
    await client.post("/auth/register", json={"email": email, "password": password})
    response = await client.post("/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_create_transaction_unauthenticated(client):
    response = await client.post("/transactions/", json={
        "title": "Biedronka",
        "amount": 45.50,
        "type": "expense",
        "category": "groceries"
    })
    assert response.status_code == 401

async def test_create_transaction_authenticated(client):
    headers = await register_and_login(client)
    response = await client.post("/transactions/", json={
        "title": "Biedronka",
        "amount": 45.50,
        "type": "expense",
        "category": "groceries"
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Biedronka"
    assert data["amount"] == 45.50

async def test_get_only_own_transactions(client):
    headers_user1 = await register_and_login(client, "user1@example.com")
    headers_user2 = await register_and_login(client, "user2@example.com")

    await client.post("/transactions/", json={
        "title": "User1 zakupy",
        "amount": 100,
        "type": "expense",
        "category": "groceries"
    }, headers=headers_user1)

    await client.post("/transactions/", json={
        "title": "User2 zakupy",
        "amount": 200,
        "type": "expense",
        "category": "groceries"
    }, headers=headers_user2)

    response = await client.get("/transactions/", headers=headers_user1)
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "User1 zakupy"

async def test_summary_only_own_transactions(client):
    headers = await register_and_login(client)
    await client.post("/transactions/", json={
        "title": "Wypłata",
        "amount": 8000,
        "type": "income",
        "category": "salary"
    }, headers=headers)
    await client.post("/transactions/", json={
        "title": "Biedronka",
        "amount": 100,
        "type": "expense",
        "category": "groceries"
    }, headers=headers)
    response = await client.get("/transactions/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 8000
    assert data["total_expenses"] == 100
    assert data["balance"] == 7900