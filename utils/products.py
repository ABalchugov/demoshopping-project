import requests
from jsonschema import validate

from schemas.products_schema import product_schema


def create_product(url, product):
    validate(product, schema=product_schema)
    response = requests.post(f"{url}/add-product", json=product)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    return response


def delete_product(url, product_id):
    delete_response = requests.delete(f"{url}/products/id/{product_id}")

    print("\nStatus code:", delete_response.status_code)
    print("Headers:", delete_response.headers)
    print("Body:", delete_response.text)

    return delete_response
