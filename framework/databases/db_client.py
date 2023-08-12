from typing import Optional, List

from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class DBClient:

    def __init__(self, dbname: str, host: str, port: str, user: str, password: str) -> connect:
        """Initializing the connection

        Args:
            dbname:     name Postgres database;
            host:       URL for connecting to the Postgres database;
            port:       port for connecting to the Postgres database;
            user:       username for connecting to the Postgres database;
            password:   password for connecting to the Postgres database.
        """
        self.conn = connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.conn.autocommit = True
        self.curs = self.conn.cursor(cursor_factory=RealDictCursor)

    def close(self) -> None:
        if not self.conn:
            return
        if self.curs:
            self.curs.close()
        self.conn.close()

    def execute(self, query: str) -> None:
        """Executing a query to the Postgres database without returning data

        Args:
            query: query to the Postgres database
        """
        self.curs.execute(str(query), None)

    def fetch_all(self, query: str) -> Optional[List[dict]]:
        """Executing a query to the Postgres database with returning data in the form of list

        Args:
            query: query to the Postgres database
        """
        self.execute(query)
        records = self.curs.fetchall()
        if records:
            rows = [dict(rec) for rec in records]
            return rows

        return []
