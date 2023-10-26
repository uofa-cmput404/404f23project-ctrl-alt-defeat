from app.posts import bp
import json
from app.db import get_db_connection
from flask import request, abort
from werkzeug.exceptions import HTTPException
from random import randrange


# VIEW POSTS
@bp.route('/', methods=['POST'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")
        request_data = request.get_json()
        author_id = request_data['author_id']

        conn = get_db_connection()

        # Get all the posts from people who I'm following + posts who are public
        query = "SELECT username, post_id, date_posted, title, content_type, content, img_id, visibility FROM posts " \
                "INNER JOIN authors ON posts.author_id = authors.author_id " \
                "WHERE posts.author_id in " \
                "(SELECT author_following FROM friends WHERE author_followee = ?) " \
                "OR visibility = 'public' " \
                "ORDER by date_posted DESC"

        posts = conn.execute(query, (author_id,)).fetchall()
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])

    except Exception as e:
        print(e)
        data = str(e)

    return data  # data


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
        content_type = request_data["content_type"]

        # validate the content_type is of the following,
        try:
            found = ["text/plain", "text/markdown", "application/base64", "image/png;base64",
                     "image/jpeg;base64"].index(content_type)
        except ValueError:
            print("Not a valid content type.")
            abort(412)

        # Check for image OR image post
        # TODO: add image posting, attaching images to posts
        image_id = request_data["image_id"]

        if image_id == None:  # JSON `null` turns into Python `None`
            image_id = "NULL"  # Change for SQL syntax

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

    return data  # data



@bp.route('/test/')
def categories():
    return "Test route for /posts"
