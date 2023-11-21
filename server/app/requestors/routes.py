from app.requestors import bp
from flask import request, jsonify, g
import sqlite3
import uuid
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT * FROM requestors WHERE username = ?", (username,))
        existing_requestor = cur.fetchone()
        cur.execute("SELECT * FROM authors WHERE username = ?", (username,))
        existing_author = cur.fetchone()

        if existing_requestor or existing_author:
            return jsonify({'error': 'Username already exists'})
        
        requestor_id = str(uuid.uuid4())

        cur.execute("INSERT INTO requestors (requestor_id, username, password) VALUES (?, ?, ?)", (requestor_id, username, hashed_password))
        db.commit()
        print('hi',requestor_id)
        return jsonify({'message': 'Registration successful', 'requestor_id': requestor_id})
    except Exception as e:
        return jsonify({'error': 'An error occurred while registering.'})

    finally:
        db.close()