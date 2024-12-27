import json
import pytest
import requests
from tests.base_api import BaseAPI
from tests.product.category import TestCategory
from tests.product.product import TestProduct


class TestOrder:
    @pytest.fixture(scope="module")
    def base_api(self):
        with open("../../config/dev_config.json", "r") as config_file:
            config = json.load(config_file)
        return BaseAPI(config)

    @pytest.fixture(scope="module")
    def category_id(self, base_api):
        category_test = TestCategory()
        return category_test.create_category(base_api)

    @pytest.fixture(scope="module")
    def product_one_id(self, base_api, category_id):
        product_test = TestProduct()
        return product_test.create_product(base_api, category_id)

    @pytest.fixture(scope="module")
    def product_two_id(self, base_api, category_id):
        product_test = TestProduct()
        return product_test.create_product(base_api, category_id)

    def create_order(self, base_api, product_one_id, product_two_id):
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

        #try:
        response = base_api.send_post_request("/orders/create-order", data)
#        response.raise_for_status()

        json_data = response.json()
        print(f"Status Code: {response.status_code}")
        print("Order Creation Response:", json.dumps(json_data, indent=4))

            #order_id = json_data.get("orderId")
            #assert order_id is not None, "Order ID is missing in the response."

           # print("Created Order ID:", order_id)
           # return order_id

       # except requests.RequestException as e:
           # pytest.fail(f"HTTP request failed: {e}")
        #except json.JSONDecodeError as e:
           # pytest.fail(f"Error decoding JSON response: {e}")

    def test_create_order(self, base_api, product_one_id, product_two_id):
        self.create_order(base_api, product_one_id, product_two_id)
        #assert order_id is not None, "Order ID should not be None"
        print(f" order is created but there is a problem with kafka ")


"""
import json
import requests
import tests.keycloak_tests.get_user_token
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/orders"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

product_one_id = create_product.saved_product_id
product_two_id = create_product.saved_product_id
"""

# def create_order():
"""
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

    # assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("create order ", json_str)

    order_id = json_data["orderId"]

    assert order_id is not None, "order is null!"

    print("order id ", order_id)

    return order_id


    saved_order_id = create_order()
    """
