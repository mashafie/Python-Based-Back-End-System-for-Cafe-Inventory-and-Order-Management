# Imports
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../docker_setup/.env')
host_name = os.getenv("MYSQL_HOST")
database_name = os.getenv("MYSQL_DB")
user_name = os.getenv("MYSQL_USER")
user_password = os.getenv("MYSQL_PASS")

# Establish connection to DB
current_connection = None

def get_connection():
    global current_connection
    if current_connection == None:
        current_connection = pymysql.connect(
            host = host_name,
            database = database_name,
            user = user_name,
            password = user_password
        )
    return current_connection

# close connection
def close_connection():
    global current_connection
    if current_connection is not None:
        current_connection.close()
        current_connection = None