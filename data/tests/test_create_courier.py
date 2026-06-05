import pytest
import requests
import random
import allure
from data.urls import Urls
from conftest import register_new_courier_and_return_login_password

@allure.epic("Работа с курьерами")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_create_courier_success(self):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": "courier_test_" + str(unique_number),
            "password": "password123",
            "firstName": "Ivan"
        }
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_resp = requests.post(Urls.LOGIN_COURIER, data={"login": payload["login"], "password": payload["password"]})
        courier_id = login_resp.json()["id"]
        requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}")

    @allure.title("Нельзя создать двух абсолютно одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": "courier_test_" + str(unique_number),
            "password": "password123",
            "firstName": "Ivan"
        }
        requests.post(Urls.CREATE_COURIER, data=payload)
        response_duplicate = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response_duplicate.status_code == 409
        assert response_duplicate.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        
        login_resp = requests.post(Urls.LOGIN_COURIER, data={"login": payload["login"], "password": payload["password"]})
        courier_id = login_resp.json()["id"]
        requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}")

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": "courier_test_" + str(unique_number),
            "password": "password123",
            "firstName": "Ivan"
        }
        del payload[missing_field]
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать пользователя с логином, который уже занят")
    def test_create_courier_with_existing_login_error(self):
        courier_info = register_new_courier_and_return_login_password()
        existing_login = courier_info[0]
        payload_with_same_login = {
            "login": existing_login,
            "password": "completely_new_password",
            "firstName": "Petr"
        }
        response = requests.post(Urls.CREATE_COURIER, data=payload_with_same_login)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        
        login_resp = requests.post(Urls.LOGIN_COURIER, data={"login": courier_info[0], "password": courier_info[1]})
        courier_id = login_resp.json()["id"]
        requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}")
