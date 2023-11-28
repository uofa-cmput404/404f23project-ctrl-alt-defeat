from . import bp
import json
from flask import request, g, jsonify
import sqlite3
from ..dbase import get_db_connection
from random import randrange
from flask_bcrypt import Bcrypt

from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash



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
            item["github"] = ("https://github.com/" + r["github"]) if r["github"] != None else None
            item["profileImage"] = None # TODO: implement profile pics
            data["items"].append(item)
        
        

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
    
    print("data here")
    return jsonify(data)

# Get a specific author (REMOTE)
@bp.route('/authors/<author_id>/', methods=['GET'])
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

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
    
    return jsonify(data)

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
        if check_password_hash(stored_password, password):
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
        hashed_password = generate_password_hash(new_password).decode('utf-8')
        
        curr.execute("UPDATE authors SET password = %s WHERE author_id = %s", (hashed_password, author_id))
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

        data = payload
        conn.commit()
        conn.close()


    except Exception as e:
        print("Getting likes error: ", e)
        data = "error"
    
    return jsonify(data)

# Get a list of likes from other authors on AUTHOR_ID’s post POST_ID (REMOTE)
@bp.route('/authors/<author_id>/posts/<post_id>/likes', methods=['GET'])
def get_liked_posts(author_id, post_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn, cur = get_db_connection()

        query = "SELECT * " \
                "FROM likes l " \
                "JOIN authors a " \
                "ON l.like_author_id = a.author_id " \
                "WHERE " \
                "l.post_id = %s"
        
        cur.execute(query, (post_id,))
        likes = cur.fetchall()        

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

        # data = json.dumps(data, indent=2)

        conn.commit()
        conn.close()


    except Exception as e:
        print("Getting likes error: ", e)
        data = "error"
    
    return jsonify(data)

# SEND LIKE TO THE author_id OF THE POST (REMOTE)
@bp.route('/authors/<author_id>/inbox', methods=['POST'])
def send_like(author_id):
    # Get attributes from HTTP body
    print("reach")
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
    
    return jsonify(data)

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
    return jsonify(data)




@bp.route('/authors/<author_id>/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(author_id, post_id):
    comment_author_id = request.args.get('comment_author_id')
    if not comment_author_id:
        return jsonify({'comments': []})

    try:
        conn, cursor = get_db_connection()
        
        query = """
            SELECT a.username, c.comment_text, c.comment_id, 
                EXISTS (
                    SELECT 1 FROM comment_likes cl 
                    WHERE cl.comment_id = c.comment_id 
                    AND cl.like_comment_author_id = %s
                ) AS isLikedByCurrentUser
            FROM comments c
            INNER JOIN authors a ON c.comment_author_id = a.author_id
            WHERE c.post_id = %s
            AND c.author_id = %s
            AND (
                (c.status = 'public') OR
                (c.status = 'private' AND c.comment_author_id = %s) OR
                (c.status = 'private' AND c.author_id = %s)
            )
        """

        cursor.execute(query, (comment_author_id, post_id, author_id, comment_author_id, comment_author_id))
        comment_info = cursor.fetchall()
        comment_info = [dict(i) for i in comment_info]
        print(comment_info)
        conn.close()

        comments_list = [
            {
                'comment_name': comment['username'],
                'comment_text': comment['comment_text'], 
                'comment_id': comment['comment_id'],
                'isLikedByCurrentUser': comment['islikedbycurrentuser']
            } for comment in comment_info
        ]
        return jsonify({'comments': comments_list})

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500


@bp.route('/authors/<author_id>/posts/<post_id>/comments', methods=['POST'])
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
        conn, cur = get_db_connection()

        #Check if the authors are friends
        check_friends_query = """
        SELECT CASE WHEN (
                SELECT COUNT(*) FROM friends 
                WHERE author_followee = %s AND author_following = %s
                ) + (
                SELECT COUNT(*) FROM friends 
                WHERE author_followee = %s AND author_following = %s
                ) = 2 THEN 'private'
                ELSE 'public'
        END AS status
        """
        cur.execute(check_friends_query, (author_id, comment_author_id, comment_author_id, author_id))
        status = dict(cur.fetchone())['status']
        print(status)
        query = "INSERT INTO comments " \
                "(comment_id, comment_author_id, " \
                "post_id, author_id, comment_text, status, date_commented) " \
                "VALUES (%s, %s, %s, %s, %s, %s ,CURRENT_TIMESTAMP)" 
        cur.execute(query, (comment_id, comment_author_id, post_id, author_id, comment_text, status))


        data = "success"

        conn.commit()

        conn.close()

    except Exception as e:
        print("comment error: ", e)
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

        # data = json.dumps(row, indent=4, sort_keys=True, default=str)
        # print(data)
        data = row
        # if row is not None:
        #     row_values = [str(value) for value in row]
        #     row_string = ', '.join(row_values)
        #     data = row_string

    except Exception as e:
        print("Getting github username error: ", e)
        data = "error"
    
    return jsonify(data)


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
    return jsonify(data)    


@bp.route('/authors/<author_id>/posts/<post_id>/comments/<comment_id>/toggle-like', methods=['POST'])
def toggle_like(author_id, post_id, comment_id):
    request_data = request.get_json()
    like_comment_author_id = request_data["like_comment_author_id"]

    try:
        conn, cursor = get_db_connection()


        # Check if the like already exists
        cursor.execute("SELECT * FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                       (like_comment_author_id, comment_id))
        
        like = cursor.fetchone()
        

        if like:
            # Like exists, so unlike it
            cursor.execute("DELETE FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                           (like_comment_author_id, comment_id))
        else:
            # Like doesn't exist, so add it
            cursor.execute("INSERT INTO comment_likes (like_comment_author_id, comment_id, time_liked) VALUES (%s, %s, CURRENT_TIMESTAMP)", 
                           (like_comment_author_id, comment_id))

        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error toggling like: ", e)
        return jsonify({"error": str(e)}), 500




@bp.route('/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes', methods=['GET'])


def get_comments_likes(comment_id):
    try:
        conn, cursor = get_db_connection()
        
        query = """
            SELECT a.username, c.time_liked
            FROM comment_likes c
            INNER JOIN authors a ON c.like_comment_author_id = a.author_id
            WHERE c.comment_id = %s
        """

        cursor.execute(query, (comment_id ))
        comment_info = cursor.fetchall()
        conn.close()

        comment_likes_list = [{'like_comment_author_id':comment[0],'time_liked': comment[1]} for comment in comment_info]
        return jsonify({'comment_likes': comment_likes_list})

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500


