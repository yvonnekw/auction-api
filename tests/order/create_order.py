import json
import requests
import tests.keycloak_tests.get_user_token
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/orders"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

product_one_id = create_product.saved_product_id
product_two_id = create_product.saved_product_id

def create_order():
    url = base_url + "/create-order"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "paymentRequest": {
            "paymentMethod": "CREDIT_CARD"
        },
        "orderRequest": {
            "reference": "ORDER-REF-001",
            "totalAmount": 300.50,
            "paymentMethod": "CREDIT_CARD",
            "products": [
                {
                    "productId": product_one_id,
                    "quantity": 1
                },
                {
                    "productId": product_two_id,
                    "quantity": 1
                }
            ]
        }
    }

    response = requests.post(url=url, headers=headers, json=data)

    #assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("create order ", json_str)

    order_id = json_data["orderId"]

    assert order_id is not None, "order is null!"

    print("order id ", order_id)

    return order_id


saved_order_id = create_order()

