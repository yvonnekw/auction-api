import json

import requests

import tests.keycloak_tests.get_user_token

base_url = "http://localhost:8222/api/v1"

token_data = tests.keycloak_tests.get_user_token.post_request_get_user_token()
access_token = token_data["access_token"]

def create_category():
    url = base_url + "/categories/create-category"
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }

    data = {
        "description": "Devices and gadgets including smartphones, laptops, cameras, and more.",
        "name": "Electronics",
    }

    try:
        response = requests.post(url=url, headers=headers, json=data)
        response.raise_for_status()

        json_data = response.json()
        print(f"Status Code: {response.status_code}")

        json_str = json.dumps(json_data, indent=4)
        print("Created category: ", json_str)

        category_id = json_data.get("categoryId")
        if category_id is None:
            raise ValueError("Category ID is missing in the response.")

        print("Category ID:", category_id)
        return category_id

    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
        raise

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        raise

    except ValueError as e:
        print(f"Error: {e}")
        raise


saved_category_id = create_category()