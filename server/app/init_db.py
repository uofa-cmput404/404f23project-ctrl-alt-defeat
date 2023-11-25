import sqlite3
import os

# Path to the database
db_path = 'server/database.db'

# Delete the database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Now create a new database connection
connection = sqlite3.connect(db_path)

with open('server/app/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()
