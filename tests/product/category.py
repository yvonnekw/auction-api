import json
import pytest
import requests
from tests.base_api import BaseAPI


class TestCategory:
    @pytest.fixture(scope="module")
    def base_api(self):
        with open("../../config/dev_config.json", "r") as config_file:
            config = json.load(config_file)
        return BaseAPI(config)

    def create_category(self, base_api):
        data = {
            "description": "Devices and gadgets including smartphones, laptops, cameras, and more.",
            "name": "Electronics",
        }
        try:
            response = base_api.send_post_request("/categories/create-category", data)
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")

            category_id = json_data.get("categoryId")
            assert category_id is not None, "Category ID is missing in the response."

            print(f"Created category with ID: {category_id}")
            return category_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def test_create_category(self, base_api):
        category_id = self.create_category(base_api)
        assert category_id is not None, "Category ID should not be None"
        print(f"Saved Category ID: {category_id}")
