import allure
import requests
import sys

from tests.helpers import BASE_URL

sys.path.insert(1, "../pages")

class TestGetOrdersList:
    @allure.title('Тест на получение списка заказов')
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200
        response_data = response.json()
        assert "orders" in response_data