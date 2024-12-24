import json
import requests
import tests.keycloak_tests.get_user_token
from tests.cart import add_cart
from tests.cart.add_cart_save_product_id import add_cart_save_product_id
from tests.cart.get_user_cart import get_user_cart
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/carts"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

product_id = add_cart_save_product_id()


def update_cart(product_id, expected_quantity):
    url = base_url + "/update"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "productId": product_id,
        "quantity": expected_quantity
    }

    response = requests.put(url=url, headers=headers, json=data)

    assert response.status_code == 200
 
    print(f"Status Code: {response.status_code}")


expected_quantity = 2
update_cart(product_id, expected_quantity)

updated_cart_data = get_user_cart()

cart_items = updated_cart_data["items"]
item = next((i for i in cart_items if i["productId"] == product_id), None)

assert item is not None, f"Product with ID {product_id} not found in the cart"
assert item["quantity"] == expected_quantity, f"Expected quantity {expected_quantity}, but got {item['quantity']}"

print(f"Product ID {product_id} has the expected quantity of {expected_quantity} in the cart.")