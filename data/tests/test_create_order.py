import pytest
import requests
import random
import allure
from data.urls import Urls

@allure.epic("Работа с заказами")
class TestOrders:

    @allure.feature("Создание заказа")
    @allure.title("Создание заказа с цветами: {colors}")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_various_colors(self, colors):
        unique_id = random.randint(100000, 999999)
        order_payload = {
            "firstName": "Имя_" + str(unique_id),
            "lastName": "Фамилия_" + str(unique_id),
            "address": "Улица Тестовая, дом " + str(unique_id),
            "metroStation": random.randint(1, 10),
            "phone": "+7999" + str(unique_id),
            "rentTime": 3,
            "deliveryDate": "2026-12-12",
            "comment": "Тестовый комментарий " + str(unique_id),
            "color": colors
        }
        response = requests.post(Urls.ORDERS, json=order_payload)
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.feature("Список заказов")
    @allure.title("Успешное получение списка заказов")
    def test_get_orders_list_returns_list(self):
        response = requests.get(Urls.ORDERS)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
