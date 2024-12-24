import json
import requests
import tests.keycloak_tests.get_user_token
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/carts"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

product_id = create_product.saved_product_id


def add_cart_save_product_id():
    url = base_url + "/add"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "productId": product_id,
        "quantity": 1
    }

    response = requests.post(url=url, headers=headers, json=data)

    assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("added product to cart ", json_str)

    #Find the hihgets cartItem Id and returen
    highest_cart_item = max(json_data["items"], key=lambda x: x["cartItemId"])
    get_product_id = highest_cart_item["productId"]

    assert get_product_id is not None, "product id is null!"

    print("Added product to cart, product ID:", get_product_id)

    return get_product_id


saved_product_id = add_cart_save_product_id()
