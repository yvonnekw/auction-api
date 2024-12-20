import json

import requests

base_url = "http://localhost:8222/api/v1/products"


def get_all_products():
    url = base_url + "/get-all-products"
    headers = {"Accept": "application/json"}
    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    assert response.status_code == 200
    json_str = json.dumps(json_data, indent=4)
    print("get all products ", json_str)


get_all_products()
