from typing import List

from framework.databases.db_client import DBClient


class PostgresDB:
    host = None
    port = None
    dbname = None
    user = None
    password = None

    def __init__(self):
        """Initializing the connection"""

        self.db = DBClient(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )

    def close(self) -> None:
        """Closing the connection"""
        self.db.close()

    def get_data_by_filter(self, table: str, field: str, value: str) -> List[dict]:
        """Getting data from table by filter field and its value

        Args:
            table: table in database;
            field: field of table;
            value: field value.

        Returns:
            [{row1}, {row2}, ...]

        """
        response = self.db.fetch_all(f'''
            SELECT *
            FROM {table}
            WHERE {field} = '{value}';
        ''')

        return response

    def get_random_products(self, quantity: int = 1) -> List[dict]:
        """Getting a random product

        Args:
            quantity: number of random products
        """
        response = self.db.fetch_all(f'''
            SELECT *
            FROM product
            WHERE active = true
            ORDER BY RANDOM()
            LIMIT {quantity};
        ''')
        return response

    def get_random_users(self, quantity: int = 1) -> List[dict]:
        """Getting a random user

        Args:
            quantity: number of random users
        """
        response = self.db.fetch_all(f'''
            SELECT *
            FROM user_details
            ORDER BY RANDOM()
            LIMIT {quantity};
        ''')
        return response

    def delete_user(self, user_name) -> List[dict]:
        """Deleting data from tables user_details by user_name

        Args:
            user_name: name of user which data deleting
        """
        response = self.db.fetch_all(f'''
            DELETE 
            FROM user_details 
            WHERE user_name = '{user_name}'
            RETURNING *;
        ''')
        return response

    def get_product_by_filter(self, field: str, ascend: bool = False, size: int = -1, page: int = -1) -> List[dict]:
        response = f'''
            SELECT *
            FROM product
            ORDER BY {field} {'ASC' if ascend else 'DESC'}
        '''
        if size > 0:
            response += f' LIMIT {size}'
        if page >= 0:
            response += f' OFFSET {size * page}'
        return self.db.fetch_all(response)
