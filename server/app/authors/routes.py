from app.authors import bp
from flask import request, g, jsonify
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
        if password == stored_password:
            result = 'Login successful'
        else:
            result = 'Wrong Password'
    else:
        result = 'User not found'

    db.close()

    return jsonify({'message': result})

@bp.route('/update_username', methods=['POST'])
def update_username():
    data = request.get_json()
    new_username = data.get('new_username')
    author_id = data.get('author_id')

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT author_id FROM authors WHERE username = ?", (new_username,))
        existing_username = cur.fetchone()

        if existing_username:
            return jsonify({'error': 'Username already exists'})

        cur.execute("UPDATE authors SET username = ? WHERE author_id = ?", (new_username, author_id))
        db.commit()

        return jsonify({'message': 'Username updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the username.'})
    finally:
        db.close()


@bp.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')
    author_id = data.get('author_id') 

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("UPDATE authors SET password = ? WHERE author_id = ?", (new_password, author_id))
        db.commit()

        return jsonify({'message': 'Password updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the password.'})
    finally:
        db.close()
