import json
import pytest
import requests
from tests.base_api import BaseAPI
from tests.product.category import TestCategory
from tests.product.product import TestProduct


class TestBid:
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

    def submit_bid(self, base_api, product_id):
        data = {
            "productId": product_id,
            "bidAmount": 1220.00
        }

        try:
            response = base_api.send_post_request("/bids/submit-bid", data)
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print("Bidding on product:", json.dumps(json_data, indent=4))

            bid_id = json_data.get("bidId")
            assert bid_id is not None, "Bid ID is missing in the response."

            print("Bid ID:", bid_id)
            return bid_id

        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def get_all_bids(self, base_api):
        try:
            response = base_api.send_get_request("/bids/get-all-bids")
            response.raise_for_status()

            json_data = response.json()
            print(f"Status Code: {response.status_code}")
            print("Retrieved bids:", json.dumps(json_data, indent=4))

            return json_data
        except requests.RequestException as e:
            pytest.fail(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            pytest.fail(f"Error decoding JSON response: {e}")

    def test_get_all_bids(self, base_api):
        bids = self.get_all_bids(base_api)
        assert bids is not None, "Bids data should not be None"
        assert isinstance(bids, list), "Bids data should be a list"
        print(f"Total Bids Retrieved: {len(bids)}")

    def test_submit_bid(self, base_api, product_id):
        bid_id = self.submit_bid(base_api, product_id)
        assert bid_id is not None, "Bid ID should not be None"
        print(f"Saved Bid ID: {bid_id}")



# base_url = "http://localhost:8222/api/v1/bids"

# token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
# access_token = token_data["access_token"]

"""
def get_all_bids():
    url = base_url + "/get-all-bids"
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
    print("get all bids ", json_str)

    #bid_id = json_data["bidId"]

    #assert bid_id is not None, "bid is null!"

    #print("bid id ", bid_id)

    #return bid_id


    #get_all_bids()
"""
