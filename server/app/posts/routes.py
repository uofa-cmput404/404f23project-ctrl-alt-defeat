from app.posts import bp
import json
from app.db import get_db_connection
from flask import request, abort
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
        content_type = "text/plain"

        # Check for image OR image post
        # TODO: add image posting, attaching images to posts
        image_id = request_data["image_id"]

        if image_id is None:  # JSON `null` turns into Python `None`
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


@bp.route('/edit/<int:post_id>', methods=['POST'])
def edit_post():
    conn = get_db_connection()
    try:
        # assert the post_id exists
        to_find = request.args.get("post_id")
        print(f"Attempting to find post with {to_find}")
        query = f'SELECT COUNT(1) FROM posts WHERE post_id = ?'
        conn.execute(query, (to_find))
        exists = conn.fetchone()
        if exists is None:
            raise Exception("Post Does Not Exist Error")
    except Exception as e:
        print(e, " Can't find post_id.")
        abort()

    # Get the new data.
    request_data = request.get_json()
    post_id = to_find
    title = request_data["title"]

    # At the moment, I am assuming the content provided is of this content_type. Some entry validation might be needed.
    content_type = request_data["content_type"]
    content = request_data["content"]
    image_id = request_data["image_id"]
    image_id = "NULL" if image_id is None else image_id
    visibility = request_data["visibility"]

    # The things that will not change:
    # - Date posted
    # - Author ID
    # - Post ID

    # Overwrite the entry with the new data.
    try:
        query = ("UPDATE posts"
                 "SET title = ?, content_type = ?,content, img_id = ?, visibility = ? "
                 "WHERE post_id = ?")
        conn.execute(query, (title, content_type, content, image_id, visibility))
        conn.commit()
    except Exception as e:
        #
        print(e, "Data not written to database. Rolling back...")
        conn.rollback()
    finally:
        conn.close()


@bp.route('/test/')
def categories():
    return "Test route for /posts"
