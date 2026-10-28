import requests
from jsonschema import validate

from schemas.products_schema import product_schema


def create_product(url, product):
    validate(product, schema=product_schema)
    response = requests.post(f"{url}/add-product", json=product)

    return response


def delete_product(url, product_id):
    delete_response = requests.delete(f"{url}/products/id/{product_id}")

    return delete_response
