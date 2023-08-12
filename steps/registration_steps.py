from random import randint


class RegistrationSteps:

    @staticmethod
    def reg_data() -> dict:
        """Registration data to be sent via the REST API"""
        user_name = f"test{randint(1, 99)}"
        data = {
            "lastName": "test",
            "firstName": "test",
            "username": user_name,
            "email": f"{user_name}@email.ru",
            "password": "password",
        }
        return data
