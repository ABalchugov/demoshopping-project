import pytest
import requests
from jsonschema import validate

from data.products import ProductData
from schemas.login_schema import login_request_schema
from schemas.registration_schema import registration_request_schema
from utils.attach import attach_api_response
from utils.config import (
    API_PASSWORD,
    API_REGISTRATION_PASSWORD,
    API_REGISTRATION_USERNAME,
    API_USERNAME,
    TEST_API_URL,
)
from utils.products import create_product, delete_product


def _get_product_id(response):
    prefix = "Продукт успешно добавлен с ID:"
    product_id = response.text.replace(prefix, "", 1).strip()
    if response.text.startswith(prefix) and product_id.isdecimal():
        return int(product_id)
    return None


def _cleanup_product(product_id):
    response = delete_product(TEST_API_URL, product_id)
    attach_api_response(response)
    assert response.status_code == 200, "Не удалось удалить товар при очистке после теста"


@pytest.fixture
def auth_response():
    assert API_USERNAME and API_PASSWORD, "Укажите API_USERNAME и API_PASSWORD в .env"
    request_body = {"username": API_USERNAME, "password": API_PASSWORD}
    validate(request_body, schema=login_request_schema)
    response = requests.post(f"{TEST_API_URL}/login", json=request_body)
    attach_api_response(response)
    return response


@pytest.fixture
def product_response():
    response = create_product(TEST_API_URL, ProductData.PRODUCT)
    attach_api_response(response)
    return response


@pytest.fixture
def created_product(product_response):
    yield product_response

    product_id = _get_product_id(product_response)
    if product_id is not None:
        _cleanup_product(product_id)


@pytest.fixture
def product_id(created_product):
    assert created_product.status_code == 200, "Не удалось создать товар для подготовки теста"
    product_id = _get_product_id(created_product)
    assert product_id is not None, "В ответе подготовки отсутствует числовой ID товара"
    return product_id


@pytest.fixture
def product_to_delete(product_response):
    product_id = _get_product_id(product_response)
    try:
        assert product_response.status_code == 200, "Не удалось создать товар для подготовки теста"
        assert product_id is not None, "В ответе подготовки отсутствует числовой ID товара"
        yield product_id
    finally:
        if product_id is not None:
            response = requests.get(f"{TEST_API_URL}/products")
            attach_api_response(response)
            assert response.status_code == 200, "Не удалось проверить наличие товара при очистке после теста"
            if any(product["product_id"] == product_id for product in response.json()):
                _cleanup_product(product_id)


@pytest.fixture
def deleted_product(product_to_delete):
    response = delete_product(TEST_API_URL, product_to_delete)
    attach_api_response(response)
    return response


@pytest.fixture
def patched_product(product_id):
    response = requests.patch(
        f"{TEST_API_URL}/products/id/{product_id}",
        json={"description": ProductData.UPDATED_DESCRIPTION},
    )
    attach_api_response(response)
    return response


@pytest.fixture
def registered_user():
    assert API_REGISTRATION_USERNAME and API_REGISTRATION_PASSWORD, (
        "Укажите API_REGISTRATION_USERNAME и API_REGISTRATION_PASSWORD в .env"
    )
    request_body = {"username": API_REGISTRATION_USERNAME, "password": API_REGISTRATION_PASSWORD}
    validate(request_body, schema=registration_request_schema)

    response_users = requests.get(f"{TEST_API_URL}/users")
    attach_api_response(response_users)
    assert response_users.status_code == 200, "Не удалось получить пользователей перед регистрацией"
    assert not any(user["login"] == API_REGISTRATION_USERNAME for user in response_users.json()), (
        "Логин API_REGISTRATION_USERNAME уже занят: задайте свободный логин в .env"
    )

    try:
        response = requests.post(f"{TEST_API_URL}/register", json=request_body)
        attach_api_response(response)
        yield response
    finally:
        response_users = requests.get(f"{TEST_API_URL}/users")
        attach_api_response(response_users)
        assert response_users.status_code == 200, "Не удалось получить пользователей при очистке после теста"
        users = [user for user in response_users.json() if user["login"] == API_REGISTRATION_USERNAME]
        assert len(users) <= 1, "Найдено несколько пользователей с логином регистрации; очистка остановлена"
        if users:
            user_id = users[0]["user_id"]
            response_delete = requests.delete(f"{TEST_API_URL}/users/{user_id}")
            attach_api_response(response_delete)
            assert response_delete.status_code == 200, "Не удалось удалить пользователя при очистке после теста"
