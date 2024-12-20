import json

import requests

import tests.keycloak_tests.get_user_token
import tests.data

base_url = "http://localhost:8222/api/v1"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

with open("../data/categories.json", "r") as file:
    categories_data = json.load(file)["categories"]

def create_categories():
    url = base_url + "/categories/create-category"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    for category in categories_data:
        response = requests.post(url=url, headers=headers, json=category)
        print(f"Creating category: {category['name']}")
        if response.status_code == 200:
            print(f"Category {category['name']} created successfully!")
        else:
            print(f"Failed to create category {category['name']}: {response.text}")

print("Seeding categories...")
create_categories()


