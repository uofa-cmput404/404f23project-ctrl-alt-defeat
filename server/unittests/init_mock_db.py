# Initalizes a fake database
import os
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv

def init_mock_db():
    load_dotenv()

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
                )    

    with connection.cursor() as cursor:        
            schema_path = "mock_schema.sql"

            cursor.execute(open(schema_path, "r").read())

    connection.commit()
    connection.close()
