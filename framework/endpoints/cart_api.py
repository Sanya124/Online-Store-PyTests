import json

import requests
from requests import Response

from configs import HOST


class CartAPI:

    def __init__(self):
        self.url = HOST + '/api/v1/cart'
        self.headers = {'Content-Type': 'application/json'}

    def add_item(self, token: str, body: dict) -> Response:
        """Adding of item in cart

        Args:
            token:  JWT token for authorization of request;
            body:   request body.
        """
        headers = self.headers
        headers['Authorization'] = f'Bearer {token}'
        url = self.url + '/items/'
        response = requests.post(url=url, data=json.dumps(body), headers=headers)
        return response

    def get_cart(self, token: str, shopping_session_id: str) -> Response:
        """Getting information about the shopping cart by the purchase session ID

        Args:
            token:               JWT token for authorization of request;
            shopping_session_id: purchase session ID.
        """
        headers = self.headers
        headers['Authorization'] = f'Bearer {token}'
        url = self.url + f'/{shopping_session_id}'
        response = requests.get(headers=headers, url=url)
        return response
