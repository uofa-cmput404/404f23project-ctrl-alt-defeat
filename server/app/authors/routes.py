from app.authors import bp
from flask import Flask, request, g, jsonify
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM authors WHERE username = ?", (username,))
    author = cur.fetchone()

    if author:
        stored_password = author['password']
        print(stored_password)
        if password == stored_password:
            result = 'Login successful'
            print('Login succ')
        else:
            result = 'Wrong credentials'
            print('Wrong cred')
    else:
        result = 'User not found'
        print('User not found')

    db.close()

    return jsonify({'message': result})


