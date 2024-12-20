import json
import requests
import tests.keycloak_tests.get_user_token
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/carts"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

def get_user_cart():
    url = base_url + "/get-user-cart"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    response = requests.get(url=url, headers=headers)

    assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("getting user cart ", json_str)

    cart_id = json_data["cartId"]

    assert cart_id is not None, "cart is null!"

    print("cart id ", cart_id)

    return cart_id


saved_cart_id = get_user_cart()
