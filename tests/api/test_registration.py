import allure
import requests
from jsonschema import validate

from schemas.base_response_schema import base_response_schema as success_registration_schema
from utils.attach import attach_api_response
from utils.config import API_REGISTRATION_USERNAME, TEST_API_URL


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма регистрации")
@allure.story("Успешная регистрация")
@allure.title("Отправка формы с корректными логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_registration(registered_user):
    response = registered_user
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_registration_schema)

    assert body["message"] == 'Регистрация выполнена успешно'

    response_users = requests.get(f"{TEST_API_URL}/users")
    attach_api_response(response_users)
    response_users.raise_for_status()
    users = [user for user in response_users.json() if user["login"] == API_REGISTRATION_USERNAME]
    assert len(users) == 1, "Созданный пользователь не найден или найден несколько раз"
