import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="markm8",
        password="password")

    # conn.row_factory = sqlite3.Row

    return connection, connection.cursor(cursor_factory=RealDictCursor)