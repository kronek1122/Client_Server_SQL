import psycopg2

class DatabaseManager:
    def __init__(self, database, user, password, host):
        self.conn = psycopg2.connect(database=database, user = user, password = password, host = host)
        self.c = self.conn.cursor()

    def add_user(self, user_name, password, is_admin):
        query = "INSERT INTO user_info (user_name, password, is_admin) VALUES (%s, %s, %s);"
        try: 
            self.c.execute(query, (user_name, password, is_admin))
            self.conn.commit()
            msg = 'User succesfully registered'
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            msg = 'User already exist'
        
        return msg

    def login_user(self, user_name, password):
        query = "SELECT * FROM user_info WHERE user_name = (%s) AND password = (%s)"
        if self.c.execute(query, (user_name, password)):

            return 