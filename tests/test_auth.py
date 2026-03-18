import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["role"] == "user"

@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient):
    # Ya existe 'user_test' del conftest
    response = await client.post(
        "/api/v1/auth/register",
        json={"username": "user_test", "password": "newpassword"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "user_test", "password": "test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "user_test", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username" in response.json()["detail"]

@pytest.mark.asyncio
async def test_read_me(client: AsyncClient, user_token_headers: dict):
    response = await client.get(
        "/api/v1/auth/me",
        headers=user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user_test"

@pytest.mark.asyncio
async def test_create_admin_success(client: AsyncClient, superadmin_token_headers: dict):
    response = await client.post(
        "/api/v1/auth/create-admin",
        json={"username": "newadmin", "password": "adminpassword"},
        headers=superadmin_token_headers
    )
    assert response.status_code == 200
    assert response.json()["role"] == "superadmin"

@pytest.mark.asyncio
async def test_create_admin_forbidden(client: AsyncClient, user_token_headers: dict):
    response = await client.post(
        "/api/v1/auth/create-admin",
        json={"username": "shouldfail", "password": "password"},
        headers=user_token_headers
    )
    assert response.status_code == 403
