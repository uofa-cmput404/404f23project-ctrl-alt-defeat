from . import bp
import json
from flask import request, g, jsonify
import sqlite3
from ..dbase import get_db_connection
from random import randrange



# Get all authors (REMOTE)
@bp.route('/authors/', methods=['GET'])
def get_authors():    
    page = request.args.get('page')
    size = request.args.get('size')
    data = ""
    try:
        conn, cur = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "ORDER BY author_id " \
                "LIMIT %s OFFSET %s"
        
        if page is not None:
            page = int(page)
        else: page = 1 # Set default 1
        
        if size is not None:
            size = int(size)
        else: size = 20 # Set default 20

        offset = (page - 1) * size
        cur.execute(query, (size, offset))
        row = cur.fetchall()
                
        res = [dict(i) for i in row]        

        data = dict()
        data["type"] = "authors"
        data["items"] = []
        
        for r in res:
            item = dict()
            item["type"] = "author"
            item["id"] = request.url_root + "api/authors/" + r["author_id"] 
            item["url"] = request.url_root + "api/authors/" + r["author_id"] 
            item["host"] = request.url_root
            item["displayName"] = r["username"]
            item["profileImage"] = None # TODO: implement profile pics
            data["items"].append(item)
        
        data = json.dumps(data, indent=2)
        

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
    
    return data

# Get a specific author (REMOTE)
@bp.route('/authors/<author_id>', methods=['GET'])
def get_author(author_id):
    data = ""
    try:
        conn, cur = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "WHERE author_id = %s " \
                
        cur.execute(query, (author_id,))
        row = cur.fetchall()
        print(row)
        res = [dict(i) for i in row][0]
        item = dict()
        item["type"] = "author"
        item["host"] = request.url_root
        item["id"] = request.url_root + "api/" + res["author_id"]
        item["url"] = request.url_root + "api/" + res["author_id"]
        item["displayName"] = res["username"]
        item["github"] = "http://github.com/" + res["github"] if res["github"] is not None else None
        item["profileImage"] = None

        data = item
        data = json.dumps(data, indent=2)

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
    
    return data

@bp.route('/authors/login', methods=['POST'])
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


@bp.route('/authors/update_username', methods=['POST'])
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


@bp.route('/authors/update_password', methods=['POST'])
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
@bp.route('/authors/<author_id>/liked', methods=['GET'])
def get_posts_liked(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE


    data = ""
    try:
        conn, curr = get_db_connection()

        query = "SELECT l.post_id, p.author_id,  a.username, a.github " \
                "FROM likes l " \
                "JOIN posts p " \
                "ON p.post_id = l.post_id " \
                "JOIN authors a " \
                "ON a.author_id = l.like_author_id " \
                "WHERE " \
                "like_author_id = %s "
        
        curr.execute(query, (author_id,))
        likes = curr.fetchall()
        likes = [dict(i) for i in likes]
        
        payload = dict()
        payload["type"] = "liked"
        payload["items"] = []

        for like in likes:
            item = dict()
            item["context"] = None
            item["summary"] = like["username"] + " Likes your post"
            item["type"] = "Like"
            item["author"] = dict()
                                    
            item["author"]["type"] = "author"
            item["author"]["id"] = request.root_url + "api/authors/" + like["author_id"]
            item["author"]["host"] = request.root_url
            item["author"]["displayName"] = like["username"]
            item["author"]["profileImage"] = None
            item["author"]["github"] = "http://github.com/" + like["github"] if like["github"] is not None else None

            item["object"] = request.root_url + "authors/" + like["author_id"] + "/posts/" + like["post_id"]
            payload["items"].append(item)

        data = json.dumps(payload, indent=2)

        conn.commit()
        conn.close()


    except Exception as e:
        print("Getting likes error: ", e)
        data = "error"
    
    return data

# Get a list of likes from other authors on AUTHOR_ID’s post POST_ID (REMOTE)
@bp.route('/authors/<author_id>/posts/<post_id>/likes', methods=['GET'])
def get_liked_posts(author_id, post_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn = get_db_connection()

        query = "SELECT * " \
                "FROM likes l " \
                "JOIN authors a " \
                "ON l.like_author_id = a.author_id " \
                "WHERE " \
                "l.post_id = ?"
        
        likes = conn.execute(query, (post_id,)).fetchall()        

        res = [dict(i) for i in likes]
    
        data = dict()
        data["count"] = len(res)
        data["results"] = []
        
        for r in res:
            item = dict()

            item["@context"] = None # What is this?
            item["summary"] = r["username"] + " Likes this post"
            item["type"] = "Like"
            item["author"] = dict()
            item["author"]["type"] = "author"
            item["author"]["id"] = request.root_url + "api/authors/" + r["author_id"]
            item["author"]["host"] = request.root_url
            item["author"]["displayName"] = r["username"]
            item["author"]["profileImage"] = None
            item["author"]["github"] = "http://github.com/" + r["github"] if r["github"] is not None else None

            r["object"] = request.root_url + "api/" + author_id + "/posts/" + post_id             
            data["results"].append(item)

        data = json.dumps(data, indent=2)

        conn.commit()
        conn.close()


    except Exception as e:
        print("Getting likes error: ", e)
        data = "error"
    
    return data

# SEND LIKE TO THE author_id OF THE POST (REMOTE)
@bp.route('/authors/<author_id>/inbox', methods=['POST'])
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

@bp.route('/authors/<author_id>/inbox/unlike', methods=['POST'])
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
@bp.route('/authors/github/<author_id>', methods=['GET'])
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
        
        # row = [dict(row) for row in row]

        data = json.dumps(row, indent=4, sort_keys=True, default=str)
        print(data)
        # if row is not None:
        #     row_values = [str(value) for value in row]
        #     row_string = ', '.join(row_values)
        #     data = row_string

    except Exception as e:
        print("Getting github username error: ", e)
        data = "error"
    
    return data


@bp.route('/authors/github', methods=['POST'])
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