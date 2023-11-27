from . import bp
from flask import request, jsonify, g
from ..dbase import get_db_connection
import sqlite3
import uuid


@bp.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn, cur = get_db_connection()
    # cur = db.cursor()

    try:
        print("here")
        cur.execute("SELECT * FROM requestors WHERE username = %s", (username,))
        existing_requestor = cur.fetchone()
        cur.execute("SELECT * FROM authors WHERE username = %s", (username,))
        existing_author = cur.fetchone()

        if existing_requestor or existing_author:
            return jsonify({'error': 'Username already exists'})
        
        requestor_id = str(uuid.uuid4())

        cur.execute("INSERT INTO requestors (requestor_id, username, password) VALUES (%s, %s, %s)", (requestor_id, username, password))
        conn.commit()
        print("here2")
        print('hi',requestor_id)
        print("done")
        return jsonify({'message': 'Registration successful', 'requestor_id': requestor_id})
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while registering.'})

    finally:
        conn.close()        