from allure import description, feature, link, step, title
from hamcrest import assert_that, is_

from asserts.authenticate_asserts import AuthenticateAsserts
from framework.endpoints.authenticate_api import AuthenticateAPI
from steps.registration_steps import RegistrationSteps


@feature('Registering a new user')
@link(url='', name='NONE. Description of the tested functionality')
class TestRegistration:

    @title('Checking registration')
    @description('WHEN the user is registered, '
                 'THEN the data is saved in database and he can authenticate for authorized requests')
    def test_registration(self, postgres):
        with step('Generation data of user for registration'):
            reg_data = RegistrationSteps.reg_data()

        with step('Registration of user'):
            registration = AuthenticateAPI().registration(data=reg_data)
            assert_that(registration.status_code, is_(201), reason='The user is not created')

        with step('Getting info about the created user in DB'):
            data_user_from_db = postgres.get_data_by_filter(
                table='user_details', field='user_name', value=reg_data['username']
            )[0]

        with step('Checking mapping data DB <> API'):
            AuthenticateAsserts.check_map_db_to_api(reference=reg_data, compared=data_user_from_db)

        with step('Delete data from DB'):
            postgres.delete_user(user_name=reg_data['username'])

    @title('Checking double registration')
    @description('WHEN the user submits the registration data again, '
                 'THEN the service returns an error when registering again')
    def test_double_registration(self, postgres):
        with step('Generation data of user for registration'):
            reg_data = RegistrationSteps.reg_data()

        with step('First registration of user'):
            first_registration = AuthenticateAPI().registration(data=reg_data)
            assert_that(first_registration.status_code, is_(201), reason='The user is not created')

        with step('Second registration of user'):
            second_registration = AuthenticateAPI().registration(data=reg_data)
            assert_that(second_registration.status_code, is_(400), reason='The user is created')
            # TODO adding assert of response

        with step('Delete data from DB'):
            postgres.delete_user(user_name=reg_data['username'])
