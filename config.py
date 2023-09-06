import os

# MySQL Settings
MYSQL_HOST = os.getenv('MYSQL_HOST')
try:
    MYSQL_PORT = int(os.getenv('MYSQL_PORT'))
except TypeError:
    print("MYSQL_PORT is not set, use default port 3306")
    MYSQL_PORT = 3306
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
