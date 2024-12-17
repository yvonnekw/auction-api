import requests
import json


keycloak_token_url = "http://localhost:9098/realms/auction-realm/protocol/openid-connect/token"

def post_request_get_user_token():
    url = keycloak_token_url
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": "auction-client",
        "grant_type": "password",
        "username": "testuser",
        "password": "password",
        "client_secret": "4fLoRVTTU7Hu7S1iBY2FNwPY7zYJYM77"
    }

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)

    print("The response body ", json_str)

    assert "access_token" in json_data

    access_token = json_data["access_token"]

    #print("access_token ", access_token)

   # return access_token

    return json_data


def get_token():
    token_data = post_request_get_user_token()
    access_token = token_data["access_token"]
    print("access_token from keycloak:", access_token)


post_request_get_user_token()

#get_token()