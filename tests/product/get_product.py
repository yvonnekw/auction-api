import tests.keycloak_tests.get_user_token
import requests
import json

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]
print("access_token from keycloak another file :", access_token)

base_url = "http://localhost:8222/api/v1/"


def get_all_products():
    url = base_url + "products/get-all-products"
    headers = {"Accept": "application/json"}

    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    assert response.status_code == 200
    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("get all products ", json_str)


def get_product():
    url = base_url + "products/1"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    assert response.status_code == 200
    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("get a product ", json_str)


get_all_products()
get_product()
