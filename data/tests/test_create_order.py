import pytest
import requests
import random
import allure
from data.urls import Urls
from data.courier_data import OrderTestData

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
        order_payload = OrderTestData.generate_order_payload(colors)
        
        with allure.step(f"Отправка POST-запроса на создание заказа с цветом {colors}"):
            response = requests.post(Urls.ORDERS, json=order_payload)
        
        with allure.step("Проверка успешного создания заказа (код 201 и наличие трек-номера)"):
            assert response.status_code == 201
            assert "track" in response.json()

    @allure.feature("Список заказов")
    @allure.title("Успешное получение списка заказов")
    def test_get_orders_list_returns_list(self):
        
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = requests.get(Urls.ORDERS)
        
        with allure.step("Проверка успешного ответа (код 200) и структуры списка заказов"):
            assert response.status_code == 200
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)
