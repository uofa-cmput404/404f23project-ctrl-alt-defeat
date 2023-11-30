import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.parse as urlparse
import os
from dotenv import load_dotenv

load_dotenv()

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

def get_db_connection():
    connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
                )

    # conn.row_factory = sqlite3.Row

    return connection, connection.cursor(cursor_factory=RealDictCursor)