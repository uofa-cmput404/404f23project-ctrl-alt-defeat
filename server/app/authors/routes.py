from app.authors import bp
import json
from flask import request, g, jsonify
import sqlite3
from app.db import get_db_connection

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
            print('Login succ')
        else:
            result = 'Wrong Password'
            print('Wrong Password')
    else:
        result = 'User not found'
        print('User not found')

    db.close()

    return jsonify({'message': result})

@bp.route('/<author_id>/liked', methods=['GET'])
# Get posts that the logged in author has liked
def get_liked_posts(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn = get_db_connection()

        query = "SELECT post_id " \
                "FROM likes WHERE " \
                "like_author_id = ?"
        
        likes = conn.execute(query, (author_id,)).fetchall()

        data = json.dumps([dict(i) for i in likes])
        print(data)

        conn.commit()
        conn.close()


    except Exception as e:
        print("liked error: ", e)
        data = "error"
    
    return data
