import pymysql


class Database:
    def __init__(self):
        self.db = None
        self.connect()

    def __del__(self):
        self.db_connection_close()

    def connect(self):
        try:
            self.db = pymysql.connect(
                host="ip", port=15506, user="root", password="password", database="dbname"
            )
        except BaseException as e:
            print("connection fail", e)

    def get_cursor(self):
        return self.db.cursor()

    def db_connection_close(self):
        self.db.close()

    def commit(self):
        self.db.commit()
