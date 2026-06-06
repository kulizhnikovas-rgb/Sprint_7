import pytest
import requests
import random
import allure
from data.urls import Urls
from conftest import register_new_courier_and_return_login_password
from data.courier_data import CourierTestData

@allure.epic("Работа с курьерами")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_create_courier_success(self, cleanup_courier):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": f"{CourierTestData.LOGIN_PREFIX}{unique_number}",
            "password": CourierTestData.BASE_PASSWORD,
            "firstName": CourierTestData.BASE_FIRST_NAME
        }
        
        cleanup_courier["login"] = payload["login"]
        cleanup_courier["password"] = payload["password"]
        
        with allure.step("Отправка POST-запроса на создание курьера"):
            response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        with allure.step("Проверка успешного создания (код 201)"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        
        

    @allure.title("Нельзя создать двух абсолютно одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self, cleanup_courier, existing_courier):
      
        payload = {
        "login": existing_courier[0],
        "password": existing_courier[1],
        "firstName": existing_courier[2]
      }
        
        cleanup_courier["login"] = payload["login"]
        cleanup_courier["password"] = payload["password"]

        
        with allure.step("Попытка создания дубликата курьера"):
            response_duplicate = requests.post(Urls.CREATE_COURIER, data=payload)
        
        with allure.step("Проверка ошибки дублирования (код 409)"):
            assert response_duplicate.status_code == 409
            assert response_duplicate.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        


    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": f"{CourierTestData.LOGIN_PREFIX}{unique_number}",
            "password": CourierTestData.BASE_PASSWORD,
            "firstName": CourierTestData.BASE_FIRST_NAME
        }
        del payload[missing_field]
        
        with allure.step(f"Отправка запроса на создание курьера без поля: {missing_field}"):
            response = requests.post(Urls.CREATE_COURIER, data=payload)
        
        with allure.step("Проверка ошибки валидации (код 400)"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать пользователя с логином, который уже занят")
    def test_create_courier_with_existing_login_error(self, cleanup_courier):
        
        with allure.step("Регистрация нового курьера через хелпер"):
            courier_info = register_new_courier_and_return_login_password()
            existing_login = courier_info[0]
        payload_with_same_login = {
            "login": existing_login,
            "password": CourierTestData.ALTERNATIVE_PASSWORD,
            "firstName": CourierTestData.ALTERNATIVE_FIRST_NAME
        }
        
        cleanup_courier["login"] = courier_info[0]
        cleanup_courier["password"] = courier_info[1]

        with allure.step("Попытка создания курьера с уже занятым логином"):
            response = requests.post(Urls.CREATE_COURIER, data=payload_with_same_login)
        
        with allure.step("Проверка ошибки занятого логина (код 409)"):
            assert response.status_code == 409
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        
       