import sqlite3
# Creates a database (based on our schema) file in the server folder

connection = sqlite3.connect('../database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()