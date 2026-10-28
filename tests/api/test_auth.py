import allure
import requests
from jsonschema import validate

from schemas.login_schema import login_response_schema, login_request_schema
from utils.attach import attach_api_response
from utils.config import API_PASSWORD, API_USERNAME, TEST_API_URL


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма логина")
@allure.story("Успешная авторизация")
@allure.title("Отправка формы с корректными логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_auth():
    assert API_USERNAME and API_PASSWORD, "Укажите API_USERNAME и API_PASSWORD в .env"
    request_body = {"username": API_USERNAME, "password": API_PASSWORD}
    validate(request_body, schema=login_request_schema)

    response = requests.post(f"{TEST_API_URL}/login", json=request_body)

    attach_api_response(response)
    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=login_response_schema)

    token = body["token"]
    assert len(token.split(".")) == 3
    assert body["message"] == 'Вход выполнен успешно'
