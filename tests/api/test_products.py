import allure
import requests
from jsonschema import validate

from data.products import ProductData
from schemas.products_schema import products_schema
from utils.attach import attach_api_response
from utils.config import TEST_API_URL
from utils.products import create_product, delete_product


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Получить список всех продуктов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_products():
    response = requests.get(f"{TEST_API_URL}/products")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)
    attach_api_response(response)
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=products_schema)


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Добавление нового продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product():
    response = create_product(TEST_API_URL, ProductData.PRODUCT)
    attach_api_response(response)
    assert response.status_code == 200
    assert response.text.startswith("Продукт успешно добавлен с ID:")

    product_id = int(response.text.replace("Продукт успешно добавлен с ID:", "").strip())
    delete_response = delete_product(TEST_API_URL, product_id)
    attach_api_response(delete_response)
    assert delete_response.status_code == 200


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Удаление продукта по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product():
    response = create_product(TEST_API_URL, ProductData.PRODUCT)
    attach_api_response(response)
    assert response.status_code == 200

    product_id = int(response.text.replace("Продукт успешно добавлен с ID:", "").strip())

    delete_response = delete_product(TEST_API_URL, product_id)

    attach_api_response(delete_response)
    assert delete_response.status_code == 200
    assert delete_response.text == "Товар удалён"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Частичное обновление товара по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product():
    response = create_product(TEST_API_URL, ProductData.PRODUCT)
    attach_api_response(response)
    assert response.status_code == 200

    product_id = int(response.text.replace("Продукт успешно добавлен с ID:", "").strip())
    patch_response = requests.patch(f"{TEST_API_URL}/products/id/{product_id}", json={"description": "Новое описание"})

    print("\nStatus code:", patch_response.status_code)
    print("Headers:", patch_response.headers)
    print("Body:", patch_response.text)

    attach_api_response(patch_response)
    assert patch_response.status_code == 200
    assert patch_response.text == "Товар частично обновлён"

    delete_response = delete_product(TEST_API_URL, product_id)

    attach_api_response(delete_response)
    assert delete_response.status_code == 200
