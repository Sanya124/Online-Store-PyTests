from allure import title, step
from psycopg2 import connect
from pytest import fixture

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS
from framework.databases.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from steps.registration_steps import RegistrationSteps

# Connection configuration
PostgresDB.dbname = DB_NAME
PostgresDB.host = HOST_DB
PostgresDB.port = PORT_DB
PostgresDB.user = DB_USER
PostgresDB.password = DB_PASS


@title('SetUp and TearDown connect to Postgres DataBase for testing')
@fixture(scope='function')
def postgres() -> connect:
    """Connect to Postgres DataBase"""
    with step('SetUp. Connecting to Postgres database'):
        conn = PostgresDB()

    yield conn

    with step('TearDown. Closing connect to Postgres database'):
        conn.close()


@title('SetUp and TearDown of user for testing')
@fixture(scope='function')
def auth(postgres) -> str:
    """Fixture for registering, authenticating and deleting a user

    Args:
        postgres: fixture of connect to Postgres DataBase

    Returns:
        JWT token for next authorizations of requests
    """
    with step('SetUp. Generation data of test user for registration'):
        reg_data = RegistrationSteps.reg_data()

    with step('SetUp. Registration of test user'):
        AuthenticateAPI().registration(data=reg_data)

    with step('SetUp. Authentication of test user'):
        response = AuthenticateAPI().authentication(username=reg_data['username'], password=reg_data['password'])
        token = response.json()['token']

    yield token

    with step('TearDown. Delete test user from DB'):
        response = postgres.delete_user(user_name=reg_data['username'])[0]
        assert response['user_name'] == reg_data['username'], 'The user has not been deleted'
