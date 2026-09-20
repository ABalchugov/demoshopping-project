import os
import allure
import requests
from jsonschema import validate
from schemas.base_response_schema import base_response_schema as success_registration_schema
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TEST_API_URL")
USERNAME = "avbalchugov1"
PASSWORD = "password1"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма регистрации")
@allure.story("Успешная регистрация")
@allure.title("Отправка формы с корректными логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_registration():
    request_body = {"username": USERNAME, "password": PASSWORD}

    response = requests.post(f"{API_URL}/register", json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_registration_schema)

    assert body["message"] == 'Регистрация выполнена успешно'

    response_users = requests.get(f"{API_URL}/users")

    users_body = response_users.json()

    user_id = None

    for item in users_body:
        if item["login"] == USERNAME:
            user_id = item["user_id"]
            break

    assert user_id is not None, f"Пользователь с логином '{USERNAME}' не найден"

    response_delete_user = requests.delete(f"{API_URL}/users/{user_id}")
    assert response_delete_user.status_code is 200
