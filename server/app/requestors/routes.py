from app.requestors import bp
from flask import request, jsonify, g
import sqlite3

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

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT * FROM requestors WHERE username = ?", (username,))
        existing_requestor = cur.fetchone()

        cur.execute("SELECT * FROM authors WHERE username = ?", (username,))
        existing_author = cur.fetchone()

        if existing_requestor or existing_author:
            return jsonify({'error': 'Username already exists'})
        
        cur.execute("INSERT INTO requestors (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while registering.'})

    finally:
        db.close()