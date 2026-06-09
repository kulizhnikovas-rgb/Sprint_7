import random

class CourierTestData:
    BASE_PASSWORD = "password123"
    BASE_FIRST_NAME = "Ivan"
    ALTERNATIVE_FIRST_NAME = "Petr"
    ALTERNATIVE_PASSWORD = "completely_new_password"
    NON_EXISTENT_PREFIX = "non_existent_user_"
    LOGIN_PREFIX = "courier_test_"
    WRONG_LOGIN = "wrong_login_12345"
    WRONG_PASSWORD = "wrong_password_9999"
    ANY_PASSWORD = "any_password"

class OrderTestData:
    RENT_TIME = 3
    DELIVERY_DATE = "2026-12-12"

    @staticmethod
    def generate_order_payload(colors):
        unique_id = random.randint(100000, 999999)
        return {
            "firstName": f"Имя_{unique_id}",
            "lastName": f"Фамилия_{unique_id}",
            "address": f"Улица Тестовая, дом {unique_id}",
            "metroStation": random.randint(1, 10),
            "phone": f"+7999{unique_id}",
            "rentTime": OrderTestData.RENT_TIME,        
            "deliveryDate": OrderTestData.DELIVERY_DATE,  
            "comment": f"Тестовый комментарий {unique_id}",
            "color": colors
        } 