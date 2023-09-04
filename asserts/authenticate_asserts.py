import pytest
from hamcrest import assert_that, is_
from requests import Response

from asserts.dicts_of_checking import request_api_to_db_user


class AuthenticateAsserts:

    @staticmethod
    def check_map_db_to_api(reference: dict, compared: dict) -> None:
        """Checking the mapping of data from database in the request API

        Args:
            reference:  data from database;
            compared:   data from the request API.
        """
        for api_key, db_key in request_api_to_db_user.items():
            assert_that(reference[api_key], is_(compared[db_key]))

    @staticmethod
    def check_response_absence_token(response: Response, expected_status_code: int) -> None:
        """Checking for the absence of a token in the API response

        Args:
            response:               the API response;
            expected_status_code:   expected status code of service.
        """
        assert_that(response.text, is_(''))
        assert_that(response.status_code, is_(expected_status_code))

    @staticmethod
    def check_response_when_empty_body_parameters(response: Response) -> None:
        """Checking the response when user sends a request with empty username and password fields

        Args:
            response: the API response.
        """
        try:
            json_response = response.json()
            assert_that(response.status_code, is_(400))
            assert_that(json_response['username'], is_('Username is the mandatory attribute'))
            assert_that(json_response['password'], is_('Password is the mandatory attribute'))
        except ValueError:
            pytest.fail('Response not contains body')
