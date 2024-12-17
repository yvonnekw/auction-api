import tests.keycloak_tests.get_user_token
import requests
import json

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]
print("access_token from keycloak another file :", access_token)

base_url = "http://localhost:8222/api/v1/"


def create_product():
    url = base_url + "products/create-product"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
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
        "categoryId": 1
    }

    response = requests.post(url=url, headers=headers, json=data)

    assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("create a product ", json_str)


create_product()
