import json
import pytest
import requests

from tests.base_api import BaseAPI
from tests.product.category import TestCategory
from tests.product.product import TestProduct


class TestCart:
    base_url = "/carts"

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
    def product_id(self, base_api, category_id):
        product_test = TestProduct()
        return product_test.create_product(base_api, category_id)

    def add_cart(self, base_api, product_id):
        endpoint = f"{self.base_url}/add"
        data = {
            "productId": product_id,
            "quantity": 1
        }

        try:
            response = base_api.send_post_request(endpoint, data)
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print("Added Product to Cart:", json.dumps(json_data, indent=4))

            cart_id = json_data.get("cartId")
            assert cart_id is not None, "Cart ID is missing in the response."

            print("Cart ID:", cart_id)
            return cart_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def add_cart_save_product_id(self, base_api, product_id):
        endpoint = f"{self.base_url}/add"
        data = {
            "productId": product_id,
            "quantity": 1
        }
        try:
            response = base_api.send_post_request(endpoint, data)
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print("Added product to cart:", json.dumps(json_data, indent=4))

            highest_cart_item = max(json_data["items"], key=lambda x: x["cartItemId"])
            get_product_id = highest_cart_item["productId"]

            assert get_product_id is not None, "Product ID is null!"

            print("Added product to cart, product ID:", get_product_id)

            return get_product_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def delete_cart(self, base_api, cart_id):
        endpoint = f"{self.base_url}/items/{cart_id}"

        try:
            response = base_api.send_delete_request(endpoint)
            response.raise_for_status()

            assert response.status_code == 204, f"Expected status code 204, but got {response.status_code}"
            print(f"Status Code: {response.status_code}")

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def get_user_cart(self, base_api):
        endpoint = f"{self.base_url}/items"
        try:
            response = base_api.send_get_request(endpoint)
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print("Getting user cart:", json.dumps(json_data, indent=4))

            cart_id = json_data.get("cartId")
            assert cart_id is not None, "Cart ID is missing in the response."

            print("Cart ID:", cart_id)
            return cart_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {e}")

    def test_get_user_cart(self, base_api, product_id):
        cart_one_id = self.add_cart(base_api, product_id)
        cart_id = self.get_user_cart(base_api)
        assert cart_id is not None, "Cart ID should not be None"
        print(f"Saved Cart ID: {cart_id}")

    def test_delete_cart(self, base_api, product_id):
        cart_id = self.add_cart(base_api, product_id)
        self.delete_cart(base_api, cart_id)
        print(f"Deleted cart item with ID: {cart_id}")

    def test_add_cart(self, base_api, product_id):
        cart_id = self.add_cart(base_api, product_id)
        assert cart_id is not None, "Cart ID should not be None"
        print(f"Saved Cart ID: {cart_id}")

    def test_add_cart_save_product_id(self, base_api, product_id):
        saved_product_id = self.add_cart_save_product_id(base_api, product_id)
        assert saved_product_id is not None, "Saved product ID should not be None"
        print(f"Saved Product ID: {saved_product_id}")

