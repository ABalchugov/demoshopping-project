import requests


def create_product(url, product):
    response = requests.post(f"{url}/add-product", json=product)

    return response


def delete_product(url, product_id):
    delete_response = requests.delete(f"{url}/products/id/{product_id}")

    return delete_response
