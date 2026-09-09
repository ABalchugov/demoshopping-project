import os
import allure
import requests
from jsonschema import validate

from schemas.products_schema import products_schema
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TEST_API_URL")


@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Получить список всех продуктов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_products():
    response = requests.get(f"{API_URL}/products")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=products_schema)


@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Добавление нового продукта")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product():
    request_body = {
        "name": "iPhone 17",
        "description": "Описание для Apple iPhone 17",
        "price": 1300,
        "category": "Phones",
        "manufacturer": "Apple",
        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYLwvcBDB1Qn4UvFrL2zdEJRlBPxe76yVnfZG1mEhFYNtsXHKtddZXfK3X&s=10",
        "freeShipping": True
    }
    response = requests.post(f"{API_URL}/add-product", json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.text
    assert body.startswith("Продукт успешно добавлен с ID:")

    product_id = int(body.replace("Продукт успешно добавлен с ID:", "").strip())

    delete_response = requests.delete(f"{API_URL}/products/id/{product_id}")

    assert delete_response.status_code == 200


@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Удаление продукта по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_product():
    request_body = {
        "name": "iPhone 17",
        "description": "Описание для Apple iPhone 17",
        "price": 1300,
        "category": "Phones",
        "manufacturer": "Apple",
        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYLwvcBDB1Qn4UvFrL2zdEJRlBPxe76yVnfZG1mEhFYNtsXHKtddZXfK3X&s=10",
        "freeShipping": True
    }
    response = requests.post(f"{API_URL}/add-product", json=request_body)

    assert response.status_code == 200

    body = response.text

    product_id = int(body.replace("Продукт успешно добавлен с ID:", "").strip())

    delete_response = requests.delete(f"{API_URL}/products/id/{product_id}")

    print("\nStatus code:", delete_response.status_code)
    print("Headers:", delete_response.headers)
    print("Body:", delete_response.text)

    assert delete_response.status_code == 200
    assert delete_response.text == "Товар удалён"


@allure.epic("API Automation")
@allure.feature("Каталог продуктов")
@allure.title("Частичное обновление товара по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_patch_product():
    request_body = {
        "name": "iPhone 17",
        "description": "Описание для Apple iPhone 17",
        "price": 1300,
        "category": "Phones",
        "manufacturer": "Apple",
        "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYLwvcBDB1Qn4UvFrL2zdEJRlBPxe76yVnfZG1mEhFYNtsXHKtddZXfK3X&s=10",
        "freeShipping": True
    }
    response = requests.post(f"{API_URL}/add-product", json=request_body)

    assert response.status_code == 200

    body = response.text

    product_id = int(body.replace("Продукт успешно добавлен с ID:", "").strip())

    patch_response = requests.patch(f"{API_URL}/products/id/{product_id}", json={"description": "Новое описание"})

    print("\nStatus code:", patch_response.status_code)
    print("Headers:", patch_response.headers)
    print("Body:", patch_response.text)

    assert patch_response.status_code == 200
    assert patch_response.text == "Товар частично обновлён"

    delete_response = requests.delete(f"{API_URL}/products/id/{product_id}")

    assert delete_response.status_code == 200
