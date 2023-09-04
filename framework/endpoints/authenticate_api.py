import json

import requests
from requests import Response

from configs import HOST


class AuthenticateAPI:

    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + '/api/v1/auth'
        self.headers = {'Content-Type': 'application/json'}

    def registration(self, data: dict) -> Response:
        """Endpoint for registration of user

        Args:
            data: registration data with required fields:
                firstName:  name;
                lastName:   surname;
                email:      electronic mail;
                username:   username;
                password:   password for username.
        """
        path = self.url + '/register'
        response = requests.post(url=path, data=json.dumps(data), headers=self.headers)

        return response

    def authentication(self, username: str, password: str) -> Response:
        """Endpoint for authentication of user

        Args:
            username: username
            password: password for username
        """
        data = {
            "username": username,
            "password": password,
        }
        path = self.url + '/authenticate'
        response = requests.post(url=path, data=json.dumps(data), headers=self.headers)

        return response

    def logout(self, token: str) -> None:
        """User logout

        Args:
            token: JWT token for authorization of request
        """
        headers = self.headers
        headers['Authorization'] = f'Bearer {token}'
        path = self.url + '/logout'
        requests.get(url=path, headers=headers)
