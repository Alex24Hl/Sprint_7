import pytest
import requests
import helpers
from urls import BASE_URL


class TestCreateCourier:
    def test_create_courier_success(self):
        result = helpers.register_new_courier_and_return_login_password()
        assert len(result) == 3, "Курьер не был создан"
        login, password, first_name = result

        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            data={"login": login, "password": password}
        )
        assert login_response.status_code == 200
        assert "id" in login_response.json()

        delete_response = helpers.delete_courier(login, password)
        assert delete_response.status_code == 200

    def test_create_duplicate_courier(self):
        first_result = helpers.register_new_courier_and_return_login_password()
        assert len(first_result) == 3
        login, password, first_name = first_result

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        duplicate_response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert duplicate_response.status_code == 409
        assert duplicate_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        delete_response = helpers.delete_courier(login, password)
        assert delete_response.status_code == 200

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        del payload[missing_field]

        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
