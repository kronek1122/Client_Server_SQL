import json, os
from db import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

db_database = os.getenv('database')
db_user = os.getenv('user')
db_password = os.getenv('password')
db_host = os.getenv('host')
db_port = os.getenv('port')



class User:
    '''Represents a user in the system with methods for user registration, login, 
    show all existing users, sending message, check inbox and chech only unread messages.'''

    def __init__(self):
        self.active_user = ''

    def register(self, username, password, is_admin='false'):
        '''Adding a new user'''

        db = DatabaseManager(db_database, db_user, db_password, db_host)
        msg = db.add_user(username, password, is_admin)
        return json.dumps(msg, indent=1)

    def login(self, username, password):
        '''Login user function'''

        db = DatabaseManager(db_database, db_user, db_password, db_host)
        msg, self.active_user = db.login_user(username, password)
        return json.dumps(msg, indent=1)


    def users_list(self):
        '''return list of existing users'''

        if self.active_user != '':
            db = DatabaseManager(db_database, db_user, db_password, db_host)
            all_users = db.get_users()
            return json.dumps(all_users)
        
        else:
            return json.dumps("You have to be logged to check list of users", indent=1)


    def send_message(self, username, message):
        '''sending message to other users'''

        db = DatabaseManager(db_database, db_user, db_password, db_host)

        if not self.active_user:
            return json.dumps('Command available only for logged users', indent=1)

        if self.active_user == username:
            return json.dumps("You can't send message to yourself", indent=1)

        if db.count_unread(username) >= 5 and not (db.is_user_admin(self.active_user) or db.is_user_admin(username)):
            msg = f'Message could not be sent, mailbox user {username} is full'
        else:
            msg = db.send_message(username, message, self.active_user)
        
        return json.dumps(msg, indent=1)


    def check_inbox(self, query):
        '''return messages in user inbox'''

        db = DatabaseManager(db_database, db_user, db_password, db_host)

        if self.active_user != '':
            if len(query)>1 and db.is_user_admin(self.active_user) is True:
                msg = db.get_message(query[1])
                
            elif len(query)>1 and db.is_user_admin(self.active_user) is False:
                msg = 'You do not have permission to check another user mail'

            else:
                msg = db.get_message(self.active_user)
                db.change_from_unread(self.active_user)
            
        else: msg = 'First you must log in!'
        return json.dumps(msg, indent=1)


    def check_unread_messages(self):
        '''return only unread messages in user inbox'''
        
        db = DatabaseManager(db_database, db_user, db_password, db_host)
        if self.active_user != '':
            if db.is_msg_unread(self.active_user):
                msg = db.get_unread_message(self.active_user)
                db.change_from_unread(self.active_user)
            else:
                msg = "Your unread message inbox is empty"
        else:
            msg = 'First you must log in!'
        return json.dumps(msg, indent=1)
