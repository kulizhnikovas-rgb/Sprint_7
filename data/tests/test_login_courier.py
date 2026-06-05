import pytest
import requests
import random
import allure
from data.urls import Urls

@allure.epic("Работа с курьерами")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Курьер может успешно авторизоваться (возвращается id)")
    def test_login_courier_success(self, registered_courier):
        login = registered_courier[0]
        password = registered_courier[1]
        payload = {"login": login, "password": password}
        response = requests.post(Urls.LOGIN_COURIER, data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка авторизации, если не передано одно из полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, registered_courier, missing_field):
        login = registered_courier[0]
        password = registered_courier[1]
        payload = {"login": login, "password": password}
        del payload[missing_field]
        response = requests.post(Urls.LOGIN_COURIER, data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка авторизации при неверном логине или пароле")
    @pytest.mark.parametrize("is_login_wrong, is_password_wrong", [
        (True, False),
        (False, True)
    ])
    def test_login_with_wrong_credentials_error(self, registered_courier, is_login_wrong, is_password_wrong):
        real_login = registered_courier[0]
        real_password = registered_courier[1]
        final_login = real_login
        final_password = real_password
        
        if is_login_wrong:
            final_login = "wrong_login_12345"
        if is_password_wrong:
            final_password = "wrong_password_9999"
            
        payload = {"login": final_login, "password": final_password}
        response = requests.post(Urls.LOGIN_COURIER, data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Ошибка авторизации под несуществующим пользователем")
    def test_login_non_existent_user_error(self):
        unique_number = random.randint(100000, 999999)
        payload = {
            "login": "non_existent_user_" + str(unique_number),
            "password": "any_password"
        }
        response = requests.post(Urls.LOGIN_COURIER, data=payload)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
