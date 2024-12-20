import json

import requests

import tests.keycloak_tests.get_user_token
import tests.data

base_url = "http://localhost:8222/api/v1"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

with open("../data/products.json", "r") as file:
    product_data = json.load(file)["products"]

def create_products():
    url = base_url + "/products/create-product"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    for product in product_data:
        response = requests.post(url=url, headers=headers, json=product)
        print(f"Creating product: {product['productName']}")
        if response.status_code == 200:
            print(f"product {product['productName']} created successfully!")
        else:
            print(f"Failed to create product {product['productName']}: {response.text}")

print("Seeding products...")
create_products()


