import os
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv

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

# # Open a cursor to perform database operations
# cur = connection.cursor()

with connection.cursor() as cursor:
    # Depending if this file is opened from the root folder,
    # `server`, or `server/app` folder, it will get 
    # the appropiate schema path.
    if os.path.exists(os.path.join(os.getcwd(), 'server/app')):
        schema_path = "server/app/schema2.sql"
    elif os.path.exists(os.path.join(os.getcwd(), 'app')):
        schema_path = "app/schema2.sql"
    else:
        schema_path = "schema2.sql"

    cursor.execute(open(schema_path, "r").read())

connection.commit()
connection.close()