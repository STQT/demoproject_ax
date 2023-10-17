import os

os.environ['DB_ENV'] = 'test'
import asyncio

import aiounittest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src import crud, models, schemas
from src.database import engine, async_session
from src.models import Base

os.environ['DB_ENV'] = 'test'


async def create_tables(engine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.metadata.create_all)


# Call the `create_tables` function using an event loop and ensure it is awaited properly
async def create_database_tables():
    file_path = "db/test.db"

    # Проверяем, существует ли файл, и удаляем его
    if os.path.exists(file_path):
        os.remove(file_path)
    await create_tables(engine, Base)


class TestMain(aiounittest.AsyncTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = async_session
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_database_tables())

    def tearDown(self):
        async def clean_up():
            await self.db.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(clean_up())

    async def test_create_user(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword"
        }
        response = self.client.post("/users/", json=user_data)
        assert response.status_code == 200
        created_user = response.json()
        assert created_user["username"] == user_data["username"]
        assert created_user["email"] == user_data["email"]
        assert created_user["full_name"] == user_data["full_name"]

    async def test_get_user(self):
        user_id = 1
        user = self.client.get(f"/users/{user_id}")
        self.assertIsNotNone(user, "Пользователь не найден")

    async def test_get_all_users(self):
        response = self.client.get("/users/")

        assert response.status_code == 200

        users = response.json()
        assert isinstance(users, list)

        if users:
            for user in users:
                assert "username" in user
                assert "email" in user
                assert "full_name" in user

    async def test_update_user(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword"
        }
        create_response = self.client.post("/users/", json=user_data)
        assert create_response.status_code == 200

        created_user = create_response.json()
        user_id = created_user["id"]

        updated_user_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "full_name": "Updated User",
            "password": "updatedpassword"
        }
        update_response = self.client.put(f"/users/{user_id}", json=updated_user_data)
        assert update_response.status_code == 200

        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        updated_user = get_response.json()
        assert updated_user["username"] == updated_user_data["username"]
        assert updated_user["email"] == updated_user_data["email"]
        assert updated_user["full_name"] == updated_user_data["full_name"]

    async def test_delete_user(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword"
        }
        create_response = self.client.post("/users/", json=user_data)
        assert create_response.status_code == 200

        created_user = create_response.json()
        user_id = created_user["id"]

        delete_response = self.client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200

        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    async def test_search_user_by_name(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword"
        }
        create_response = self.client.post("/users/", json=user_data)
        assert create_response.status_code == 200

        created_user = create_response.json()

        search_response = self.client.get(f"/users/search/{user_data['username']}")
        assert search_response.status_code == 200

        found_user = search_response.json()

        assert found_user["id"] == created_user["id"]
        assert found_user["username"] == user_data["username"]
        assert found_user["email"] == user_data["email"]
        assert found_user["full_name"] == user_data["full_name"]


if __name__ == '__main__':
    aiounittest.main()
