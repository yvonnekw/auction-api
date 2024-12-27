import json
import pytest
import requests
from tests.base_api import BaseAPI
from tests.product.category import TestCategory


class TestProduct:
    @pytest.fixture(scope="module")
    def base_api(self):
        with open("../../config/dev_config.json", "r") as config_file:
            config = json.load(config_file)
        return BaseAPI(config)

    @pytest.fixture(scope="module")
    def category_id(self, base_api):
        category_test = TestCategory()
        return category_test.create_category(base_api)

    def get_all_products(self, base_api):
        try:
            response = base_api.send_no_auth_get_request("/products/get-all-products")
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {json.dumps(json_data, indent=4)}")

            assert response.status_code == 200
            assert isinstance(json_data, list), "Expected a list of products"

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")
        except AssertionError as e:
            pytest.fail(f"Assertion failed: {e}")

    def create_product(self, base_api, category_id):
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
            "categoryId": category_id,
        }
        try:
            response = base_api.send_post_request("/products/create-product", data)
            response.raise_for_status()

            json_data = response.json()
            print(f"Created product: {json.dumps(json_data, indent=4)}")

            product_id = json_data.get("productId")
            assert product_id is not None, "Product ID is missing in the response."

            print(f"Created product with ID: {product_id}")
            return product_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def test_create_product(self, base_api, category_id):
        product_id = self.create_product(base_api, category_id)
        assert product_id is not None, "Product ID should not be None"
        print(f"Saved Product ID: {product_id}")

    def test_get_all_products(self, base_api):
        self.get_all_products(base_api)

