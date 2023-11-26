from app.authors import bp
import json
from flask import request, g, jsonify
import sqlite3
from app.dbase import get_db_connection
from random import randrange



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn, cur = get_db_connection()

    cur.execute("SELECT author_id, password FROM authors WHERE username = %s", (username,))
    author = cur.fetchone()
    print(author)

    if author:
        stored_password = author['password']
        if password == stored_password:
            result = {'message': 'Login successful', 'author_id': author['author_id']}
        else:
            result = {'message': 'Wrong Password'}
    else:
        result = {'message': 'User not found'}

    conn.close()

    return jsonify(result)


@bp.route('/update_username', methods=['POST'])
def update_username():
    data = request.get_json()
    new_username = data.get('new_username')
    author_id = data.get('authorId')

    conn, curr = get_db_connection()

    try:
        curr.execute("SELECT author_id FROM authors WHERE username = %s", (new_username,))
        existing_username = curr.fetchone()

        if existing_username:
            return jsonify({'error': 'Username already exists'})

        curr.execute("UPDATE authors SET username = %s WHERE author_id = %s", (new_username, author_id))
        conn.commit()

        return jsonify({'message': 'Username updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the username.'})
    finally:
        conn.close()


@bp.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')
    author_id = data.get('authorId') 

    conn, curr = get_db_connection()    

    try:
        curr.execute("UPDATE authors SET password = %s WHERE author_id = %s", (new_password, author_id))
        conn.commit()

        return jsonify({'message': 'Password updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the password.'})
    finally:
        conn.close()


# Get posts that the logged in author has liked
@bp.route('/<author_id>/liked', methods=['GET'])
def get_liked_posts(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn, curr = get_db_connection()

        query = "SELECT post_id " \
                "FROM likes WHERE " \
                "like_author_id = %s"
        
        curr.execute(query, (author_id,))
        likes = curr.fetchall()


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
        conn, curr = get_db_connection()

        query = "INSERT INTO likes " \
                "(like_id, like_author_id, " \
                "post_id, time_liked) " \
                "VALUES (%s, %s, %s, " \
                "CURRENT_TIMESTAMP)"
        
        curr.execute(query, (like_id, like_author_id, post_id))

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
        conn, curr = get_db_connection()

        query = "DELETE FROM likes " \
                "WHERE like_author_id = %s AND post_id = %s"
        
        curr.execute(query, (like_author_id, post_id))

        data = "success"

        conn.commit()
        conn.close()
    except Exception as e:
        print("liked error: ", e)
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
        conn, curr = get_db_connection()

        query = "SELECT github " \
                "FROM authors WHERE " \
                "author_id = %s"
        
        curr.execute(query, (author_id,))
        row = curr.fetchone()
        
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
        conn, curr = get_db_connection()        
        query = "UPDATE authors SET github = %s " \
                "WHERE author_id = %s"
        
        curr.execute(query, (github,author_id))

        data = "success"

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error trying to update github username: ", e)
        data = "error"
    return data