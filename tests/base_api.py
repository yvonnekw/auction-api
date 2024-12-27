import requests
import json


class BaseAPI:
    def __init__(self, config):
        self.config = config
        self.base_url = config["base_url"]
        self.token = self.get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json"
        }
        self.basic_headers = {
                  "Accept": "*/*"
        }

    def get_access_token(self):
        url = self.config["keycloak_token_url"]
        data = {
            "client_id": self.config["credentials"]["client_id"],
            "client_secret": self.config["credentials"]["client_secret"],
            "username": self.config["credentials"]["username"],
            "password": self.config["credentials"]["password"],
            "grant_type": "password"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def send_get_request(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response

    def send_no_auth_get_request(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.basic_headers)
        return response

    def send_post_request(self, endpoint, data):
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=data)
        return response

    def send_put_request(self, endpoint, data):
        response = requests.put(f"{self.base_url}{endpoint}", headers=self.headers, json=data)
        return response

    def send_delete_request(self, endpoint):
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
        return response
