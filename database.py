import mysql.connector
import re


class DataToMySQL:
    def __init__(self):
        # Connection Details
        hostname = 'localhost'
        username = 'root'
        password = '12345678a'  # your password
        database = 'pxgo'

        # Create/Connect to database
        self.connection = mysql.connector.connect(
            host=hostname, user=username, password=password, database=database)
        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        # Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS items(
            id INT auto_increment PRIMARY KEY,
            name VARCHAR(255),
            weight FLOAT,
            price FLOAT,
            time DATE
        )
        """)

    def insert_data(self, name: str, w: str, price: str, date: str):

        w = re.findall(r'\d+g', w)[0][:-1]
        price = price.split('$')[1]

        # Define insert statement
        self.cur.execute("""insert into items(
            name,
            weight,
            price,
            time
            ) values (%s,%s,%s,%s)""",  (
            name,
            w,
            price,
            date
        ))

        # Execute insert of data into database
        self.connection.commit()

    def close(self):

        # Close cursor & connection to database
        self.cur.close()
        self.connection.close()
