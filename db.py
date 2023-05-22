import psycopg2

class DatabaseManager:
    def __init__(self, database, user, password, host):
        self.conn = psycopg2.connect(database=database, user = user, password = password, host = host)
        self.c = self.conn.cursor()

    def add_user(self, username, password, is_admin=False):
        query = "INSERT INTO user_info (user_name, password, is_admin) VALUES (%s, %s, %s);"
        self.c.execute(query, (username, password, is_admin))
        self.conn.commit

