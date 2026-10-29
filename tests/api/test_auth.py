import allure
from jsonschema import validate

from schemas.login_schema import login_response_schema


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма логина")
@allure.story("Успешная авторизация")
@allure.title("Проверка статуса и схемы ответа при авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_auth(auth_response):
    response = auth_response
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=login_response_schema)


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Форма логина")
@allure.story("Успешная авторизация")
@allure.title("Проверка токена и сообщения авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_auth_content(auth_response):
    body = auth_response.json()
    token = body["token"]
    assert len(token.split(".")) == 3
    assert body["message"] == 'Вход выполнен успешно'
