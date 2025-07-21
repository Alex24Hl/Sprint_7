import pytest
from helpers import create_test_order

class TestCreateOrder:
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"],[]])
    def test_create_order_with_colors(self, color):
        response = create_test_order(color)
        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data
