from app.authors import bp
import json
from flask import request, g, jsonify
import sqlite3
from app.dbase import get_db_connection
from random import randrange

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

    cur.execute("SELECT author_id, password FROM authors WHERE username = ?", (username,))
    author = cur.fetchone()

    if author:
        stored_password = author['password']
        if password == stored_password:
            result = {'message': 'Login successful', 'author_id': author['author_id']}
        else:
            result = {'message': 'Wrong Password'}
    else:
        result = {'message': 'User not found'}

    db.close()

    return jsonify(result)

@bp.route('/update_username', methods=['POST'])
def update_username():
    data = request.get_json()
    new_username = data.get('new_username')
    author_id = data.get('authorId')

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
    author_id = data.get('authorId') 

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
        
# Get posts that the logged in author has liked
@bp.route('/<author_id>/liked', methods=['GET'])
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
        print("Getting likes error: ", e)
        data = "error"
    
    return data

# SEND LIKE TO THE author_id OF THE POST
@bp.route('/<author_id>/inbox', methods=['POST'])
def send_like(author_id):
    # Get attributes from HTTP body
    request_data = request.get_json()
    like_author_id = request_data["like_author_id"]
    post_id = request_data["post_id"]

    # Create like ID
    # TODO: change method of randomization
    like_id = str(randrange(0, 100000))

    data = ""
    try:
        conn = get_db_connection()

        query = "INSERT INTO likes " \
                "(like_id, like_author_id, " \
                "post_id, time_liked) " \
                "VALUES (?, ?, ?, " \
                "CURRENT_TIMESTAMP)"
        
        conn.execute(query, (like_id, like_author_id, post_id))

        data = "success"

        conn.commit()
        conn.close()


    except Exception as e:
        print("liked error: ", e)
        data = "error"
    
    return data

@bp.route('/<author_id>/inbox/unlike', methods=['POST'])
# DELETE LIKE
def delete_like(author_id):
    request_data = request.get_json()
    like_author_id = request_data["like_author_id"]
    post_id = request_data["post_id"]
    
    data = ""
    try:
        conn = get_db_connection()

        query = "DELETE FROM likes " \
                "WHERE like_author_id = ? AND post_id = ?"
        
        conn.execute(query, (like_author_id, post_id))

        data = "success"

        conn.commit()
        conn.close()


    except Exception as e:
        print("liked error: ", e)
        data = "error"
    
    return data