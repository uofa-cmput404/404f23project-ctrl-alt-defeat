from app.requestors import bp
from flask import Flask, request, jsonify, g, render_template, redirect, url_for

import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    cur = db.cursor()

    # Check if the username is already taken
    cur.execute("SELECT * FROM authors WHERE username = ?", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'error': 'Username already exists'})

    # Insert the user into the requestors table
    cur.execute("INSERT INTO requestors (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    
    return jsonify({'message': 'Registration successful'})