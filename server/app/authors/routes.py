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

# Get all authors (REMOTE)
@bp.route('/authors', methods=['GET'])
def get_authors():    
    page = request.args.get('page')
    size = request.args.get('size')
    data = ""
    try:
        conn = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "ORDER BY author_id " \
        
        if page is not None and size is not None:
            page = int(page)
            size = int(size)

            offset = (page - 1) * size
            query += "LIMIT ? OFFSET ?"

            row = conn.execute(query, (size, offset)).fetchall();
        
        else: row = conn.execute(query).fetchall();
        
        # res = json.dumps([dict(i) for i in row])
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
        conn = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "WHERE author_id = ? " \
        
        print(query)
        row = conn.execute(query, (author_id,)).fetchall()
        
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


@bp.route('/authors/update_username', methods=['POST'])
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


@bp.route('/authors/update_password', methods=['POST'])
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
@bp.route('/authors/<author_id>/liked', methods=['GET'])
def get_posts_liked(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    # TODO: Use this query to actually match the spec requirement
    #       can't do it rn because its going to mess the front end a lot

    '''SELECT l.post_id, p.author_id 
    FROM likes l 
    JOIN posts p
    ON p.post_id = l.post_id
    WHERE 
    like_author_id = "ae58521a-9aaf-4df3-89a7-ab52757f7f63'''

    data = ""
    try:
        conn = get_db_connection()

        query = "SELECT post_id " \
                "FROM likes WHERE " \
                "like_author_id = ?"
        
        likes = conn.execute(query, (author_id,)).fetchall()


        data = json.dumps([dict(i) for i in likes], indent=2)
        print(data)

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


# Get Github username of author
@bp.route('/authors/github/<author_id>', methods=['GET'])
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


@bp.route('/authors/github', methods=['POST'])
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