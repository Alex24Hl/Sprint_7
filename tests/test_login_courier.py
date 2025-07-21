import allure
import pytest
import requests
import helpers
from urls import BASE_URL

class TestLoginCourier:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.credentials = helpers.register_new_courier_and_return_login_password()
        assert len(self.credentials) == 3
        self.login, self.password, self.first_name = self.credentials
        yield
        delete_response = helpers.delete_courier(self.login, self.password)
        assert delete_response.status_code == 200

    @allure.title('Тест на успешную авторизацию')
    def test_login_success(self):
        response = requests.post(
            f'{BASE_URL}/courier/login',
            data={"login": self.login, "password": self.password}
        )
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Тест на проверку отсутствия обязательных полей при авторизации')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field):
        payload = {"login": self.login, "password": self.password}
        del payload[missing_field]

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Тест на проверку неверных учетных данных при авторизации')
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_wrong_credentials(self, wrong_field):
        payload = {"login": self.login, "password": self.password}
        payload[wrong_field] += "_invalid"

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Тест на проверку несуществующего пользователя')
    def test_login_nonexistent_user(self):
        response = requests.post(
            f'{BASE_URL}/courier/login',
            data={"login": "nonexistent_user", "password": "invalid_password"}
        )
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"