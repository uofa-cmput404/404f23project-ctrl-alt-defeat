from app.authors import bp
import json
from flask import request, g, jsonify
import sqlite3
from app.dbase import get_db_connection
from random import randrange
from flask_bcrypt import Bcrypt

from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

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
        if check_password_hash(stored_password, password):
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
        hashed_password = generate_password_hash(new_password).decode('utf-8')
        cur.execute("UPDATE authors SET password = ? WHERE author_id = ?", (hashed_password, author_id))
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




@bp.route('/<author_id>/posts/<post_id>/comments', methods=['GET'])


def get_post_comments(author_id, post_id):
    comment_author_id = request.args.get('comment_author_id')
    if not comment_author_id:
        return jsonify({'comments': []})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT a.username, c.comment_text, c.comment_id
            FROM comments c
            INNER JOIN authors a ON c.comment_author_id = a.author_id
            WHERE c.post_id = ?
            AND c.author_id = ?
            AND (
                (c.status = 'public') OR
                (c.status = 'private' AND c.comment_author_id = ?) OR
                (c.status = 'private' AND c.author_id = ?)
                
            )
        """

        cursor.execute(query, (post_id, author_id, comment_author_id, comment_author_id ))
        comment_info = cursor.fetchall()
        conn.close()

        comments_list = [{'comment_name':comment[0],'comment_text': comment[1], 'comment_id':comment[2]} for comment in comment_info]
        return jsonify({'comments': comments_list})

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500



@bp.route('/<author_id>/posts/<post_id>/comments', methods=['POST'])
def send_comments(author_id, post_id):
    # Get attributes from HTTP body
    request_data = request.get_json()
    comment_author_id = request_data["comment_author_id"]
    comment_text = request_data["comment_text"]


    # Create comment_id ID
    # TODO: change method of randomization
    comment_id = str(randrange(0, 100000))

    data = ""
    try:
        conn = get_db_connection()

        # Check if the authors are friends
        check_friends_query = "SELECT COUNT(*) FROM friends " \
                              "WHERE author_followee = ? AND author_following = ? " \
                              "UNION " \
                              "SELECT COUNT(*) FROM friends " \
                              "WHERE author_followee = ? AND author_following = ?"
        friends_count = conn.execute(check_friends_query, (author_id, comment_author_id, comment_author_id, author_id)).fetchall()

        # Determine the status based on friendship
        status = 'private' if all(count[0] > 0 for count in friends_count) else 'public'

        query = "INSERT INTO comments " \
                "(comment_id, comment_author_id, " \
                "post_id, author_id, comment_text, status, date_commented) " \
                "VALUES (?, ?, ?, ?, ?, ? ,CURRENT_TIMESTAMP)" 
        
        conn.execute(query, (comment_id, comment_author_id, post_id, author_id, comment_text, status))

        data = "success"

        conn.commit()
        conn.close()


    except Exception as e:
        print("comment error: ", e)
        data = "error"
    
    return data



# Get Github username of author
@bp.route('/github/<author_id>', methods=['GET'])
def get_github(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn = get_db_connection()

        query = "SELECT github " \
                "FROM authors WHERE " \
                "author_id = ?"
        
        row = conn.execute(query, (author_id,)).fetchone();
        # print(str(github_username))
        if row is not None:
            row_values = [str(value) for value in row]
            row_string = ', '.join(row_values)
            data = row_string

    except Exception as e:
        print("Getting github username error: ", e)
        data = "error"
    
    return data


@bp.route('/github', methods=['POST'])
# Set Github username
def update_github():
    request_data = request.get_json()    
    github = request_data["github"]
    author_id = request_data["author_id"]
    
    data = ""
    try:
        conn = get_db_connection()        
        query = "UPDATE authors SET github = ? " \
                "WHERE author_id = ?"
        
        conn.execute(query, (github,author_id))

        data = "success"

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error trying to update github username: ", e)
        data = "error"
    return data


@bp.route('/<author_id>/posts/<post_id>/comments/<comment_id>/toggle-like', methods=['POST'])
def toggle_like(author_id, post_id, comment_id):
    request_data = request.get_json()
    like_comment_author_id = request_data["like_comment_author_id"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the like already exists
        cursor.execute("SELECT * FROM comment_likes WHERE like_comment_author_id = ? AND comment_id = ?", 
                       (like_comment_author_id, comment_id))
        like = cursor.fetchone()

        if like:
            # Like exists, so unlike it
            cursor.execute("DELETE FROM comment_likes WHERE like_comment_author_id = ? AND comment_id = ?", 
                           (like_comment_author_id, comment_id))
        else:
            # Like doesn't exist, so add it
            cursor.execute("INSERT INTO comment_likes (like_comment_author_id, comment_id, time_liked) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                           (like_comment_author_id, comment_id))

        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error toggling like: ", e)
        return jsonify({"error": str(e)}), 500




@bp.route('/<author_id>/posts/<post_id>/comments/<comment_id>/likes', methods=['GET'])


def get_comments_likes(comment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT a.username, c.time_liked
            FROM comment_likes c
            INNER JOIN authors a ON c.like_comment_author_id = a.author_id
            WHERE c.comment_id = ?
        """

        cursor.execute(query, (comment_id ))
        comment_info = cursor.fetchall()
        conn.close()

        comment_likes_list = [{'like_comment_author_id':comment[0],'time_liked': comment[1]} for comment in comment_info]
        return jsonify({'comment_likes': comment_likes_list})

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500


