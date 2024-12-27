import json
import requests
import tests.keycloak_tests.get_user_token
from tests.product import create_product

base_url = "http://localhost:8222/api/v1/bids"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

product_id = create_product.saved_product_id


def submit_bid():
    url = base_url + "/submit-bid"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "productId": product_id,
        "bidAmount": 1220.00
       # "username": "testuser",
       # "bidTime": "2024-11-30T12:00:00Z"
    }

    response = requests.post(url=url, headers=headers, json=data)

    assert response.status_code == 200
    json_data = response.json()

    print(f"Status Code: {response.status_code}")

    json_str = json.dumps(json_data, indent=4)
    print("bidding on product ", json_str)

    bid_id = json_data["bidId"]

    assert bid_id is not None, "bid is null!"

    print("bid id ", bid_id)

    return bid_id


saved_bid_id = submit_bid()
