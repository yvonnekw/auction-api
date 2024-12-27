import json
import requests
import tests.keycloak_tests.get_user_token
from tests.cart import add_cart
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/carts"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

cart_id = add_cart.saved_cart_id


def delete_cart():
    url = base_url + f"/items/{cart_id}"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    response = requests.delete(url=url, headers=headers)

    assert response.status_code == 204

    print(f"Status Code: {response.status_code}")

delete_cart()
