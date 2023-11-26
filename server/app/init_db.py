import os
import psycopg2
import urllib.parse as urlparse

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
    # printopen("schema.sql", "r").read()
    # Note this must be run from server/app ! Do not run from heroku
    cursor.execute(open("schema2.sql", "r").read())

connection.commit()
connection.close()
