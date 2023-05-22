import psycopg2, os
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')

# Create Basic Database
conn = psycopg2.connect(user=user, password=password, host = host, port = port)
conn.autocommit = True
c = conn.cursor()

try:
    c.execute('CREATE DATABASE db_cs;')
except errors.DuplicateDatabase:
    pass

conn.close()

#Connect to database
conn = psycopg2.connect(user=user, password=password, host = host)
c = conn.cursor()

#Create Tables

query = """CREATE TABLE user_info (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            password TEXT,
            is_admin BOOLEAN NOT NULL);

        CREATE TABLE unread_messages (
            message_id INTEGER PRIMARY KEY,
            message_time TIME NOT NULL,
            sender TEXT,
            reciver TEXT,
            message TEXT);"""

try:
    c.execute(query)
except errors.DuplicateTable:
    pass

conn.commit()
conn.close()