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
            time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
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
            db.add("conversation_his", '"user","content"', ("Jay", "黑琵測試"))
        """
        if values[1] is None:
            # 移除 "time" 列，並不插入 time 的值，讓數據庫使用默認值
            columns = '"user", "content"'
            query = f"INSERT INTO {table} ({columns}) VALUES (%s, %s)"
            self.cur.execute(query, (values[0], values[2]))  # 插入的值不包括 time
        else:
            # 如果 time 有值，則正常插入
            query = f"INSERT INTO {table} ({columns}) VALUES (%s, %s, %s)"
            self.cur.execute(query, values)  # 正常插入所有值
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
            results = db.get("conversation_his", '"id","user","time","content"')
        """
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cur.execute(query)
        
        temp_results = self.cur.fetchall()
        result = []
        if temp_results:
            for info in temp_results:
                id, user, time, content = info
                str_time = f"{time.year}/{time.month}/{time.day}"
                result.append({'id':id,
                                'user':user,
                                'time':str_time,
                                'content':content})
        return result
    

    def delete(self, table: str, ids: list) -> None:
        """
        Deletes records from the specified table based on a list of ids.

        Args:
            table (str): The name of the table from which to delete records.
            ids (list): A list of ids that specifies which records to delete. If only one id is provided, the query will handle it.

        Example:
            db.delete("conversation_his", [1])  # 刪除一條記錄
            db.delete("conversation_his", [1, 2, 3])  # 刪除多條記錄
        """
        if len(ids) == 1:
            # 如果只有一個 id，使用普通的等號進行刪除
            query = f"DELETE FROM {table} WHERE id = %s"
            self.cur.execute(query, (ids[0],))
        else:
            # 如果有多個 id，使用 IN 語句
            query = f"DELETE FROM {table} WHERE id IN %s"
            self.cur.execute(query, (tuple(ids),))

        # 提交更改
        self.conn.commit()

    def close(self) -> None:
        """
        Closes the cursor and the database connection.
        """
        self.cur.close()
        self.conn.close()
