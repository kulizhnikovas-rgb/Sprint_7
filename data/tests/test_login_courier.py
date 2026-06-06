import pytest
import requests
import random
import allure
from data.urls import Urls
from data.courier_data import CourierTestData

@allure.epic("Работа с курьерами")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Курьер может успешно авторизоваться (возвращается id)")
    def test_login_courier_success(self, registered_courier):
        login = registered_courier[0]
        password = registered_courier[1]
        payload = {"login": login, "password": password}
        
        with allure.step("Отправка POST-запроса на авторизацию курьера"):
            response = requests.post(Urls.LOGIN_COURIER, data=payload)
        
        with allure.step("Проверка успешного ответа (код 200 и наличие id)"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Ошибка авторизации, если не передано одно из полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, registered_courier, missing_field):
        login = registered_courier[0]
        password = registered_courier[1]
        payload = {"login": login, "password": password}
        del payload[missing_field]
        
        with allure.step(f"Отправка запроса на авторизацию без поля {missing_field}"):
            response = requests.post(Urls.LOGIN_COURIER, data=payload)
        
        with allure.step("Проверка ошибки валидации полей (код 400)"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка авторизации при неверном логине")
    def test_login_with_wrong_login_error(self, registered_courier):
        real_password = registered_courier[1]
        
        payload = {
            "login": CourierTestData.WRONG_LOGIN, 
            "password": real_password            
        }
        
        with allure.step("Отправка запроса на авторизацию с неверным логином"):
            response = requests.post(Urls.LOGIN_COURIER, data=payload)
            
        with allure.step("Проверка ошибки (код 404) и текста сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"


    @allure.title("Ошибка авторизации при неверном пароле")
    def test_login_with_wrong_password_error(self, registered_courier):
        real_login = registered_courier[0]
        
        payload = {
            "login": real_login,                     
            "password": CourierTestData.WRONG_PASSWORD
        }
        
        with allure.step("Отправка запроса на авторизацию с неверным паролем"):
            response = requests.post(Urls.LOGIN_COURIER, data=payload)
            
        with allure.step("Проверка ошибки (код 404) и текста сообщения"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"


    @allure.title("Ошибка авторизации под несуществующим пользователем")
    def test_login_non_existent_user_error(self):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": f"{CourierTestData.NON_EXISTENT_PREFIX}{unique_number}",
            "password": CourierTestData.ANY_PASSWORD
        }
        
        with allure.step("Отправка запроса на авторизацию под вымышленным пользователем"):
            response = requests.post(Urls.LOGIN_COURIER, data=payload)
        
        with allure.step("Проверка ошибки отсутствия пользователя в базе (код 404)"):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"
