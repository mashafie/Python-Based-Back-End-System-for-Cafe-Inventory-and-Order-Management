from database import *
import pytest
from unittest.mock import patch, Mock
from database import get_connection, close_connection
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../docker_setup/.env')
host_name = os.getenv("MYSQL_HOST")
database_name = os.getenv("MYSQL_DB")
user_name = os.getenv("MYSQL_USER")
user_password = os.getenv("MYSQL_PASS")

@patch('pymysql.connect')
def test_get_connection_with_no_connection(mock_pymysql_connect):
    # Arrange
    global current_connection
    current_connection = None
    mock_connection = Mock()
    mock_pymysql_connect.return_value = mock_connection

    # Act
    connection = get_connection()

    # Assert
    mock_pymysql_connect.assert_called_once_with(
        host = host_name,
        database = database_name,
        user = user_name,
        password = user_password
    )
    assert connection == mock_connection

def test_close_connection_with_no_connection():
    # Arrange
    global current_connection
    current_connection = None

    # Act
    close_connection()

    # Assert
    assert current_connection is None
