from allure import description, feature, link, step, title
from hamcrest import assert_that, is_

from asserts.authenticate_asserts import AuthenticateAsserts
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from steps.registration_steps import RegistrationSteps


@feature('Authentication of user')
@link(url='', name='NONE. Description of the tested functionality')
class TestAuthentication:

    @title('Checking authentication')
    @description('WHEN the user is authenticated, THEN user can send authorized requests')
    def test_authentication(self, postgres):
        with step('Generation data of user for registration'):
            reg_data = RegistrationSteps.reg_data()

        with step('Registration of user'):
            registration = AuthenticateAPI().registration(data=reg_data)
            assert_that(registration.status_code, is_(201), reason='The user is not created')

        with step('Getting info about the created user in DB'):
            data_user = postgres.get_data_by_filter(
                table='user_details', field='user_name', value=reg_data['username']
            )[0]

        with step('Authentication of the created user'):
            response = AuthenticateAPI().authentication(username=reg_data['username'], password=reg_data['password'])
            token = response.json()['token']

        with step('Getting user info by ID via API'):
            user = UsersAPI().get_user_by_id(token=token, user_id=data_user['id'])
            assert_that(user.status_code, is_(200), reason='Failed request "get_user_by_id"')

        with step('Delete data from DB'):
            postgres.delete_user(user_name=reg_data['username'])

    @title('Checking authentication with an invalid password')
    @description('WHEN the user is authenticated with an invalid password, '
                 'THEN the user receives a 401 status code without a token')
    def test_authentication_not_valid_data(self, postgres):
        with step('Generation data of user for registration'):
            reg_data = RegistrationSteps.reg_data()

        with step('Registration of user'):
            registration = AuthenticateAPI().registration(data=reg_data)
            assert_that(registration.status_code, is_(201), reason='The user is not created')

        with step('Authentication of the created user with an invalid password'):
            response = AuthenticateAPI().authentication(
                username=reg_data['username'], password=f"{reg_data['password']}1"
            )

        with step('Checking API response'):
            AuthenticateAsserts.check_response_absence_token(response=response, expected_status_code=401)
            # TODO Fix checking of response - response body

        with step('Delete data from DB'):
            postgres.delete_user(user_name=reg_data['username'])

    @title('Checking authentication with empty fields')
    @description('WHEN a user sends a request with empty username and password fields, '
                 'THEN the response code 400 with a description of the mandatory filling in of the fields')
    def test_authentication_with_empty_parameters(self):
        with step('Authentication with empty request body parameters'):
            response = AuthenticateAPI().authentication(username='', password='')

        with step('Checking API response'):
            AuthenticateAsserts.check_response_when_empty_body_parameters(response=response)
