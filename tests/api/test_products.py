from decimal import Decimal

import allure
import requests
from jsonschema import validate

from data.products import ProductData
from schemas.products_schema import products_schema
from utils.attach import attach_api_response
from utils.config import TEST_API_URL


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Получить список всех продуктов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_products():
    response = requests.get(f"{TEST_API_URL}/products")

    attach_api_response(response)
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=products_schema)


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка статуса ответа при добавлении продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product(created_product):
    response = created_product
    assert response.status_code == 200


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка сообщения и данных созданного продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product_content(created_product):
    response = created_product
    prefix = "Продукт успешно добавлен с ID:"
    assert response.text.startswith(prefix)
    product_id = response.text.replace(prefix, "", 1).strip()
    assert product_id.isdecimal(), "В ответе создания отсутствует числовой ID товара"

    response_products = requests.get(f"{TEST_API_URL}/products")
    attach_api_response(response_products)
    response_products.raise_for_status()
    products = [product for product in response_products.json() if product["product_id"] == int(product_id)]
    assert len(products) == 1, "Созданный продукт не найден или найден несколько раз"

    product = products[0]
    expected = ProductData.PRODUCT
    assert product["name"] == expected["name"]
    assert product["description"] == expected["description"]
    assert Decimal(str(product["price"])) == Decimal(str(expected["price"]))
    assert product["category"] == expected["category"]
    assert product["manufacturer"] == expected["manufacturer"]
    assert product["imageUrl"] == expected["imageUrl"]
    assert product["freeShipping"] == int(expected["freeShipping"])


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка статуса ответа при удалении продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product(deleted_product):
    response = deleted_product
    assert response.status_code == 200


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка сообщения и отсутствия удалённого продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product_content(deleted_product, product_to_delete):
    response = deleted_product
    assert response.text == "Товар удалён"

    response_products = requests.get(f"{TEST_API_URL}/products")
    attach_api_response(response_products)
    response_products.raise_for_status()
    assert all(product["product_id"] != product_to_delete for product in response_products.json()), (
        "Продукт остался в каталоге после удаления"
    )


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка статуса ответа при обновлении продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product(patched_product):
    assert patched_product.status_code == 200


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Проверка сообщения и сохранённого описания продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product_content(patched_product, product_id):
    assert patched_product.text == "Товар частично обновлён"

    response_products = requests.get(f"{TEST_API_URL}/products")
    attach_api_response(response_products)
    response_products.raise_for_status()
    products = [product for product in response_products.json() if product["product_id"] == product_id]
    assert len(products) == 1, "Обновлённый продукт не найден или найден несколько раз"
    assert products[0]["description"] == ProductData.UPDATED_DESCRIPTION
