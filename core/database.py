import psycopg2

class PostgreSQL():
    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        """
        Initializes the PostgreSQL class by establishing a connection to the database 
        and creating a cursor object to execute SQL queries.

        Args:
            host (str): The hostname or IP address of the PostgreSQL server.
            database (str): The name of the database to connect to.
            user (str): The username used to authenticate to the PostgreSQL server.
            password (str): The password used to authenticate the user.
        """
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()
        
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        """
        Creates the 'conversation_his' table if it does not already exist.
        The table will contain the following columns:
        - user: text
        - time: time
        - content: text
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS conversation_his (
            id SERIAL PRIMARY KEY,
            "user" TEXT,
            time TIME,
            content TEXT
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def add(self, table: str, columns: str, values: tuple) -> None:
        """
        Adds a new record to the specified table in the database.

        Args:
            table (str): The name of the table to insert the data into.
            columns (str): The columns where data will be inserted, in a comma-separated string format.
            values (tuple): A tuple containing the values to be inserted into the specified columns.

        Example:
            db.add("users", "name, age", ("John", 30))
        """
        query = f"INSERT INTO {table} ({columns}) VALUES (%s, %s)"
        self.cur.execute(query, values)
        self.conn.commit()

    def get(self, table: str, columns: str = "*", condition: str = None) -> list:
        """
        Retrieves records from the specified table in the database.

        Args:
            table (str): The name of the table to fetch data from.
            columns (str, optional): The columns to retrieve, default is all columns (*).
            condition (str, optional): An SQL condition to filter the results (e.g., "age > 30").

        Returns:
            list: A list of tuples containing the retrieved records.

        Example:
            results = db.get("users", "name, age", "age > 30")
        """
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def delete(self, table: str, condition: str) -> None:
        """
        Deletes records from the specified table based on a condition.

        Args:
            table (str): The name of the table from which to delete records.
            condition (str): The condition that specifies which records to delete.

        Example:
            db.delete("users", "age < 20")
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cur.execute(query)
        self.conn.commit()

    def close(self) -> None:
        """
        Closes the cursor and the database connection.
        """
        self.cur.close()
        self.conn.close()
