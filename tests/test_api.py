# запускается через pytest tests/test_api.py
import pytest 
from httpx import AsyncClient, ASGITransport
from main import app

# проверяем get запрос на столики
@pytest.mark.asyncio
async def test_get_tables():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get("/tables/")
        assert response.status_code == 200


# проверяем post запрос на столики
@pytest.mark.asyncio
async def test_post_table():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post("/tables/", json={
            "id": 11,
            "name": "stol",
            "seats": 6,
            "location": "szadi"
        })
        assert response.status_code == 200 or response.status_code == 201
        assert response.json()["name"] == "stol"


# Проверка удаления стола

@pytest.mark.asyncio
async def test_delete_table():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:

        response_delete = await ac.delete(f"/tables/1")
        assert response_delete.status_code == 200
        assert response_delete.json() == {"ok": True}

        response_get = await ac.get("/tables/")
        assert all(table["id"] != 1 for table in response_get.json())

# проверка создания, просмтра и удаления броней 

@pytest.mark.asyncio
async def test_get_res():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get("/reservations/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_res():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post("/tables/", json={
            "id": 11,
            "customer_name": "stol",
            "tables_id": 5,
            "reservation_time": "2025-04-14T21:08:50.794Z"
        })
        assert response.status_code == 200 or response.status_code == 201
        assert response.json()["name"] == "stol"


@pytest.mark.asyncio
async def test_delete_res():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:

        response_delete = await ac.delete(f"/reservations/1")
        assert response_delete.status_code == 200
        assert response_delete.json() == {"ok": True}

        response_get = await ac.get("/reservations/")
        assert all(table["id"] != 1 for table in response_get.json())