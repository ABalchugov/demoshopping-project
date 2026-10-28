import allure
import requests
from jsonschema import validate

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
@allure.title("Добавление нового продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product(created_product):
    response = created_product
    assert response.status_code == 200
    prefix = "Продукт успешно добавлен с ID:"
    assert response.text.startswith(prefix)
    product_id = response.text.replace(prefix, "", 1).strip()
    assert product_id.isdecimal(), "В ответе создания отсутствует числовой ID товара"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Удаление продукта по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product(deleted_product):
    response = deleted_product
    assert response.status_code == 200
    assert response.text == "Товар удалён"


@allure.label("layer", "API Tests")
@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Частичное обновление товара по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product(product_id):
    patch_response = requests.patch(f"{TEST_API_URL}/products/id/{product_id}", json={"description": "Новое описание"})

    attach_api_response(patch_response)
    assert patch_response.status_code == 200
    assert patch_response.text == "Товар частично обновлён"
