from app.posts import bp
import json
from app.db import get_db_connection
from flask import request
from random import randrange
import sqlite3

@bp.route("/restrict", methods=["POST"])
def restrict_user():
    request_data = request.get_json()
    post_id = request_data['post_id']
    username = request_data['username']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn = get_db_connection()        
        
        # Grab the username first
        query = "SELECT author_id FROM authors WHERE username = ?"

        # Use a parameterized query to insert values safely
        result = conn.execute(query,
                    (username, ))

        author_id = [dict(i) for i in result][0]['author_id']
        
        query = "INSERT INTO post_restrictions (post_id, restricted_author_id) " \
                    "VALUES (?, ?)"
        
        # # Use a parameterized query to insert values safely
        conn.execute(query,
                    (post_id, author_id))

        conn.commit()
        conn.close()

        data = "success"
    except sqlite3.IntegrityError as e:
        # Handle the UNIQUE constraint failure
        print(f"UNIQUE constraint failed: {e}")
        data = "duplicate"
        # You can log the error, notify the user, or take other appropriate actions
        
    except Exception as e:        
        print(e)
        data = "error"

    return data # data

@bp.route("/visibility", methods=["POST"])
def change_visibility():
    request_data = request.get_json()
    post_id = request_data['post_id']
    visibility = request_data['visibility']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn = get_db_connection()
        query = "UPDATE posts " \
                "SET visibility = ? " \
                "WHERE post_id = ? "
        conn.execute(query, (visibility, post_id))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route("/delete", methods=["POST"])
def delete_post():
    request_data = request.get_json()
    post_id = request_data['post_id']
    data = ""

    try:
        conn = get_db_connection()
        query = f"DELETE FROM posts " \
                f"WHERE post_id = ? "
        conn.execute(query, (post_id, ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/manage', methods=['POST'])
def get_my_posts():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("manage")
        request_data = request.get_json()
        author_id = request_data['author_id']
                    
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = "SELECT * FROM posts " \
                "WHERE posts.author_id = ? " \
                "ORDER by date_posted DESC"
        
        posts = conn.execute(query, (author_id, )).fetchall()                                
        print(posts)
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/', methods=['POST'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")
        request_data = request.get_json()
        author_id = request_data['author_id']
                
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public + posts that are mine
        # Do not include posts that I'm restricted from
        query = "SELECT username, posts.post_id, date_posted, title, content_type, content, img_id, visibility " \
                "FROM posts " \
                "INNER JOIN authors ON posts.author_id = authors.author_id " \
                "LEFT JOIN post_restrictions pr ON posts.post_id = pr.post_id " \
                "WHERE " \
                    "(posts.author_id IN (SELECT author_following FROM friends WHERE author_followee = 1) " \
                    "OR posts.visibility = 'public' " \
                    "OR posts.author_id = ?) " \
                    "AND (pr.post_id IS NULL OR pr.restricted_author_id != ?) " \
                "ORDER BY date_posted DESC; " 
        
        posts = conn.execute(query, (author_id, author_id)).fetchall()                                
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])
    
    except Exception as e:
        print(e)
        data = str(e)

    return data # data

# MAKE POSTS
@bp.route('/new/', methods=['POST'])
def new_post():
    data = ""
    try:
        # Retrieve post data from the request's JSON body
        # to get author_id, title, content, visibility
        print("NEW POST data")
        request_data = request.get_json()
        author_id = request_data["author_id"]
        title = request_data["title"]
        content = request_data["content"]
        visibility = request_data["visibility"]

        # Assign random post ID - TODO: change method of randomization
        post_id = str(randrange(0, 100000))

        # Determine type of content
        # TODO: only plain text for now, add markdown
        content_type = "text/plain"
        
        # Check for image OR image post
        # TODO: add image posting, attaching images to posts
        image_id = request_data["image_id"]
        
        if image_id == None: # JSON `null` turns into Python `None`
            image_id = "NULL" # Change for SQL syntax
                
        conn = get_db_connection()
        
        query = "INSERT INTO posts (post_id, author_id, title, content_type, content, img_id, visibility) " \
                    "VALUES (?, ?, ?, ?, ?, ?, ?)"
        
        # Use a parameterized query to insert values safely
        conn.execute(query,
                    (post_id, author_id, title, content_type, content, image_id, visibility))

        conn.commit()
        conn.close()
    
    except Exception as e:
        print(e)
        data = str(e)

    return data # data

@bp.route('/test/')
def categories():
    return "Test route for /posts"