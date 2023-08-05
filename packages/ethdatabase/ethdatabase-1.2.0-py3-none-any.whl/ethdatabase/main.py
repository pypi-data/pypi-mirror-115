import mysql.connector
from datetime import datetime
import yaml


def connect(credentials: dict):
    return mysql.connector.connect(
        host=credentials["HOST"],
        user=credentials["USER"],
        passwd=credentials["PASSWD"],
        database=credentials["DATABASE"])


class EthDatabase:

    def __init__(self, credentials):
        self.db = connect(credentials)
        self.cursor = self.db.cursor()

    @classmethod
    def from_values(cls, host: str, user: str, passwd: str, database: str):
        return EthDatabase({"HOST": host, "USER": user, "PASSWD": passwd, "DATABASE": database})

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as f:
            credentials = yaml.safe_load(f)
            return cls(credentials)

    def print_db_list(self):
        self.cursor.execute("SHOW DATABASES")
        for x in self.cursor:
            print(x)

    def print_table_list(self):
        self.cursor.execute("SHOW TABLES")
        for x in self.cursor:
            print(x)

    def print_table_structure(self, table_name):
        self.cursor.execute("DESCRIBE " + table_name)
        for x in self.cursor:
            print(x)

    def create_generic_table(self, transaction: str):
        self.cursor.execute(transaction)
        self.db.commit()

    def create_value_table(self):
        self.create_generic_table(
            "CREATE TABLE Value ("
            "date datetime PRIMARY KEY,"
            "usd float,"
            "eur float)")

    def create_fee_table(self):
        self.create_generic_table(
            "CREATE TABLE Fee ("
            "date datetime,"
            "fast float,"
            "average float,"
            "safelow float,"
            "FOREIGN KEY (date) references Value(date))")

    def print_table(self, table):
        self.cursor.execute("SELECT * FROM " + table)
        for x in self.cursor:
            print(x)

    def is_connected(self):
        return self.db.is_connected()

    def close_connection(self):
        self.db.close()

    def generic_insert(self, insert: str, values: tuple):
        self.cursor.execute(insert, values)
        self.db.commit()

    def insert_in_value(self, usd, eur, time=datetime.now()):
        insert = "INSERT INTO Value (date, usd, eur) VALUES (%s, %s, %s)"
        values = (time, usd, eur)
        self.generic_insert(insert, values)

    def insert_in_fee(self, fast, average, safelow, time=datetime.now()):
        insert = "INSERT INTO Fee(date, fast, average, safelow) VALUES (%s, %s, %s, %s)"
        values = (time, fast, average, safelow)
        self.generic_insert(insert, values)

    def insert_in_value_and_fee(self, usd, eur, fast, average, safelow, time=datetime.now()):
        self.insert_in_value(usd, eur, time=time)
        self.insert_in_fee(fast, average, safelow, time=time)
