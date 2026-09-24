import os
import allure
import requests
from jsonschema import validate
from schemas.login_schema import login_response_schema, login_request_schema
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TEST_API_URL")
USERNAME = "avbalchugov12"
PASSWORD = "password12"
TOKEN_PATH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма логина")
@allure.story("Успешная авторизация")
@allure.title("Отправка формы с корректными логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_auth(attach_api):
    request_body = {"username": USERNAME, "password": PASSWORD}
    validate(request_body, schema=login_request_schema)

    response = requests.post(f"{API_URL}/login", json=request_body)

    attach_api(response)
    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=login_response_schema)

    token = body["token"]
    assert TOKEN_PATH in token
    assert len(token.split(".")) == 3
    assert body["message"] == 'Вход выполнен успешно'
