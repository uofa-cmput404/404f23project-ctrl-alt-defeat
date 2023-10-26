from app.posts import bp
import json
from app.db import get_db_connection
from flask import request, abort
from werkzeug.exceptions import HTTPException
from random import randrange
from sqlite3 import DatabaseError


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


@bp.route('/authors/<author_id>/<post_id>/image/', methods=['GET'])
def get_image(author_id, post_id):
    conn = get_db_connection()
    final_message = "Nothing happened."
    # check if image exists
    try:
        query = "SELECT img_id, content_type from posts WHERE (post_id = ? AND img_id IS NOT NULL AND author_id = ?);"
        cursor = conn.cursor()
        conn.execute(query, (post_id, author_id))
        img_id = cursor.fetchone()
        if img_id[0] is None:
            abort(404, "The post with this image id does not exist.")
        print("Successfully found the post with this image id.")

        query = "SELECT img_url,visibility FROM image_post WHERE img_id = ?;"

        conn.execute(query, (img_id[0],))
        img_visibility = cursor.fetchone()
        if img_visibility is None:
            abort(404, "The post exists, but the image it references does not exist.")
        elif img_visibility["visibility"] != "public":
            abort(403, "This post exists, but the image contained is only visible to specific users.")

        content_type = img_id["content_type"]
        content = img_visibility["img_url"]
        final_message = f"data:{content_type},{content}"
        return final_message
    except HTTPException as e:
        final_message = str(e)
        print(final_message)
    finally:
        conn.close()
        return final_message


@bp.route('/authors/<author_id>/<post_id>/edit/', methods=['POST'])
def edit_post(author_id, post_id):
    final_message = ""
    conn = get_db_connection()
    try:
        # check if the post exists
        to_find = (post_id,)
        print(f"Attempting to find post with {post_id}")
        cursor = conn.cursor()
        query = "SELECT * FROM posts WHERE post_id = ?;"
        conn.execute(query, to_find)
        exists = cursor.fetchall()
        if exists is None:
            abort(404, "The post_id cannot be found.")

        # Check if valid JSON.
        try:
            request_data = request.get_json()
        except Exception:
            abort(400, "No JSON in request.")

        post_id = to_find[0]
        title = request_data["title"]

        # At the moment, I am assuming the content provided is of this content_type. Some entry validation might be needed.

        # TODO: Images will need to be updated as well in the image_post table.

        content_type = request_data["content_type"]
        content = request_data["content"]
        image_id = request_data["img_id"]
        image_id = "NULL" if image_id is None else image_id
        visibility = request_data["visibility"]

        # The things that will not change:
        # - Date posted
        # - Author ID
        # - Post ID

        # Overwrite the entry with the new data.
        # TODO: Only update what has changed. Comparison with old vs. new data needed.

        query = "UPDATE posts SET title = ?, content_type = ?,content = ?, img_id = ?, visibility = ? WHERE post_id = ? AND author_id = ?;"
        conn.execute(query, (title, content_type, content, image_id, visibility, post_id, author_id))
        final_message = "Post Updated Successfully"
        conn.commit()
    except HTTPException as e:
        final_message = str(e)
    except KeyError as e:
        final_message = str(e, "There are missing keys in the received JSON.")
    except DatabaseError as e:
        final_message = str(e, " Post unable to update. Rolling back database changes.")
        conn.rollback()
    except Exception as e:
        final_message = str(e)
    finally:
        conn.close()
        return final_message

@bp.route('/test/')
def categories():
    return "Test route for /posts"
