import json

import requests
from sqlalchemy import null

import tests.keycloak_tests.get_user_token
from tests.product import category

base_url = "http://localhost:8222/api/v1/products"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

category_id = create_category.saved_category_id

def create_product():
    url = base_url + "/create-product"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "productName": "iPhone 12 Pro",
        "brandName": "Apple",
        "description": "Latest Apple smartphone with A16 chip, 128GB storage, and 48MP camera",
        "startingPrice": 800.99,
        "buyNowPrice": 1100.00,
        "colour": "Space Black",
        "productSize": "6.1 inches",
        "isAvailableForBuyNow": True,
        "isSold": False,
        "quantity": 10,
        "categoryId": category_id
    }

    response = requests.post(url=url, headers=headers, json=data)

    assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("create a product ", json_str)

    product_id = json_data["productId"]

    assert product_id is not None, "product is null!"

    print("product id ", product_id)

    return product_id


saved_product_id = create_product()
# create_product()
