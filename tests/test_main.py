import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMain(unittest.TestCase):
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    def test_create_user(self):
        # Реализуйте тесты для создания пользователя
        pass

    def test_get_user(self):
        # Реализуйте тесты для получения пользователя по id
        pass

    def test_get_all_users(self):
        # Реализуйте тесты для получения всех пользователей
        pass

    def test_update_user(self):
        # Реализуйте тесты для обновления пользователя по id
        pass

    def test_delete_user(self):
        # Реализуйте тесты для удаления пользователя по id
        pass

    def test_search_user_by_name(self):
        # Реализуйте тесты для поиска пользователя по имени
        pass


if __name__ == '__main__':
    unittest.main()
