import os
import allure
import requests
from jsonschema import validate

from helpers.products import create_product, delete_product
from schemas.products_schema import products_schema
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TEST_API_URL")


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Получить список всех продуктов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_products(attach_api):
    response = requests.get(f"{API_URL}/products")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)
    attach_api(response)
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=products_schema)


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Добавление нового продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product(attach_api):
    response = create_product(API_URL)
    attach_api(response["original_response"])
    assert response["status"] == 200
    assert response["body"].startswith("Продукт успешно добавлен с ID:")

    product_id = int(response["body"].replace("Продукт успешно добавлен с ID:", "").strip())
    delete_response = delete_product(API_URL, product_id)
    attach_api(delete_response["original_response"])
    assert delete_response["status"] == 200


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Удаление продукта по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product(attach_api):
    response = create_product(API_URL)
    attach_api(response["original_response"])
    assert response["status"] == 200

    product_id = int(response["body"].replace("Продукт успешно добавлен с ID:", "").strip())

    delete_response = delete_product(API_URL, product_id)

    attach_api(delete_response["original_response"])
    assert delete_response["status"] == 200
    assert delete_response["body"] == "Товар удалён"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Частичное обновление товара по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product(attach_api):
    response = create_product(API_URL)
    attach_api(response["original_response"])
    assert response["status"] == 200

    product_id = int(response["body"].replace("Продукт успешно добавлен с ID:", "").strip())
    patch_response = requests.patch(f"{API_URL}/products/id/{product_id}", json={"description": "Новое описание"})

    print("\nStatus code:", patch_response.status_code)
    print("Headers:", patch_response.headers)
    print("Body:", patch_response.text)

    attach_api(patch_response)
    assert patch_response.status_code == 200
    assert patch_response.text == "Товар частично обновлён"

    delete_response = delete_product(API_URL, product_id)

    attach_api(delete_response["original_response"])
    assert delete_response["status"] == 200
