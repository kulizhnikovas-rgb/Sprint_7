import pytest
import requests
import random
import string
from data.urls import Urls

# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass 




@pytest.fixture(scope="function")
def cleanup_courier():
    
    courier_data = {}
    yield courier_data  
   
    if "login" in courier_data and "password" in courier_data:
        login_resp = requests.post(Urls.LOGIN_COURIER, data={
            "login": courier_data["login"], 
            "password": courier_data["password"]
        })
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}")


@pytest.fixture(scope="function")
def registered_courier():
    
    courier_info = register_new_courier_and_return_login_password()
    yield courier_info
    
    login_payload = {"login": courier_info[0], "password": courier_info[1]}
    login_resp = requests.post(Urls.LOGIN_COURIER, data=login_payload)
    
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}")


@pytest.fixture(scope="function")
def existing_courier():

    courier_info = register_new_courier_and_return_login_password()
    return courier_info

