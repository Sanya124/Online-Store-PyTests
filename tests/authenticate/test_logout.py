from allure import description, feature, link, step, title
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI


@feature('Logout of a user')
@link(url='', name='NONE. Description of the tested functionality')
class TestLogout:

    @title('Checking log out')
    @description('WHEN the user logout, THEN the JWT token is not valid')
    def test_logout(self, auth, postgres):
        with step('Authentication of user'):
            token = auth

        with step('Getting info about the random user in DB'):
            data_user = postgres.get_random_users()[0]

        with step('Getting user info by ID via API'):
            user = UsersAPI().get_user_by_id(token=token, user_id=data_user['id'])
            assert_that(user.status_code, is_(200), reason='Failed request "get_user_by_id"')

        with step('Log out of user'):
            AuthenticateAPI().logout(token=token)

        with step('Re-getting data user by ID via API'):
            user = UsersAPI().get_user_by_id(token=token, user_id=data_user['id'])
            assert_that(user.status_code, is_(401), reason='Log out not executed')
