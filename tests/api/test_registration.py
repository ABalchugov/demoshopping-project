import allure
import requests
from jsonschema import validate

from schemas.base_response_schema import base_response_schema as success_registration_schema
from schemas.registration_schema import registration_request_schema
from utils.attach import attach_api_response
from utils.config import API_REGISTRATION_PASSWORD, API_REGISTRATION_USERNAME, TEST_API_URL


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма регистрации")
@allure.story("Успешная регистрация")
@allure.title("Отправка формы с корректными логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_registration():
    assert API_REGISTRATION_USERNAME and API_REGISTRATION_PASSWORD, (
        "Укажите API_REGISTRATION_USERNAME и API_REGISTRATION_PASSWORD в .env"
    )
    request_body = {"username": API_REGISTRATION_USERNAME, "password": API_REGISTRATION_PASSWORD}
    validate(request_body, schema=registration_request_schema)

    response = requests.post(f"{TEST_API_URL}/register", json=request_body)

    attach_api_response(response)
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_registration_schema)

    assert body["message"] == 'Регистрация выполнена успешно'

    response_users = requests.get(f"{TEST_API_URL}/users")

    users_body = response_users.json()

    user_id = None

    for item in users_body:
        if item["login"] == API_REGISTRATION_USERNAME:
            user_id = item["user_id"]
            break

    assert user_id is not None, f"Пользователь с логином '{API_REGISTRATION_USERNAME}' не найден"

    response_delete_user = requests.delete(f"{TEST_API_URL}/users/{user_id}")
    attach_api_response(response_delete_user)
    assert response_delete_user.status_code is 200
