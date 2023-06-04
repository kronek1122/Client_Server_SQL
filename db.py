import psycopg2

class DatabaseManager:
    def __init__(self, database, user, password, host):
        self.conn = psycopg2.connect(database=database, user = user, password = password, host = host)
        self.c = self.conn.cursor()


    def add_user(self, user_name, password, is_admin):
        query = "INSERT INTO user_info (user_name, password, is_admin) VALUES (%s, %s, %s);"
        user_table = f"""CREATE TABLE {user_name} (
                        message_id SERIAL PRIMARY KEY,
                        message_text VARCHAR(255),
                        sender VARCHAR(50),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_unread BOOLEAN);"""
        try: 
            self.c.execute(query, (user_name, password, is_admin))
            self.c.execute(user_table)
            self.conn.commit()
            msg = 'User succesfully registered'
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            msg = 'User already exist'
        return msg


    def login_user(self, user_name, password):
        query = "SELECT * FROM user_info WHERE user_name = (%s) AND password = (%s)"
        self.c.execute(query, (user_name, password))
        rows = self.c.fetchall()

        if len(rows)>0:
            msg = "User succesfully login"
        else:
            msg = "Wrong password or user doesn't exist"
            user_name = ''
        return msg, user_name


    def get_users(self):
        query = "SELECT user_name FROM user_info"
        self.c.execute(query)
        return self.c.fetchall()


    def send_message(self, user_name, message, sender):
        values = (''.join(message), sender, True)
        query = f"INSERT INTO {user_name} (message_text, sender, is_unread) VALUES {values};"
        try: 
            self.c.execute(query)
            self.conn.commit()
            msg = f'You successfully send message to user {user_name}'
        except psycopg2.errors.UndefinedTable:
            self.conn.rollback()
            msg = "User doesn't exist"
        return msg


