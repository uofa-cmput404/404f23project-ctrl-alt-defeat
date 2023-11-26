import os
import psycopg2

connection = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="hueygonzales",
        password="password")
        # user=os.environ['DB_USERNAME'],
        # password=os.environ['DB_PASSWORD'])

# # Open a cursor to perform database operations
# cur = connection.cursor()

with connection.cursor() as cursor:
    # printopen("schema.sql", "r").read()
    cursor.execute(open("schema2.sql", "r").read())

connection.commit()
connection.close()
