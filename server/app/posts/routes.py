from app.posts import bp
import json
from app.db import get_db_connection
from flask import request, abort, Response
from werkzeug.exceptions import HTTPException
from random import randrange
from sqlite3 import DatabaseError
import base64


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


@bp.route('/new/image/', methods=['POST'])
def new_image():
    final_message = ""
    conn = get_db_connection()
    try:
        request_data = request.get_json()
        try:
            # check JSON keys

            author_id = request_data["author_id"]
            title = request_data["title"]
            image_extension = request_data["content_type"]
            image = request_data["content"]
            print(image)
            visibility = request_data["visibility"]
        except KeyError:
            abort(400, "Invalid JSON provided. Check for missing keys/values, JSON formatting, etc.")

        # data validation

        if image_extension not in ["image/png;base64","image/jpeg;base64","application/base64"]:
            abort(400,"This is not an image.")

        # check if content is valid base64
        #
        try:
            # from StackOverflow
            # https://stackoverflow.com/a/45928164
            value = base64.b64encode(base64.b64decode(image)) == image
        except Exception:
            abort(400, "The image provided was not base64 encoded.")

        # replace later
        post_id = str(randrange(0, 100000))
        img_id = str(randrange(0,100000))
        insert_into_posts = 'INSERT INTO posts (post_id,author_id,title,content_type,content,img_id,visibility) VALUES (?,?,?,?,?,?,?);'
        conn.execute(insert_into_posts,(post_id,author_id,title,image_extension,image,img_id,visibility))
        conn.commit()
        add_to_image_table = 'INSERT INTO image_post (img_id,author_id,img_url,visibility,date_posted) SELECT img_id,author_id,content,visibility,date_posted FROM posts WHERE post_id = ?;'

        conn.execute(add_to_image_table,(post_id,))
        conn.commit()
        final_message = Response("Image successfully added.",201)
    except DatabaseError as e:
        conn.rollback()
        abort(500,"Unable to commit changes to database. Reverting changes.")
    except HTTPException as e:
        final_message = str(e)
    except Exception as e:
        final_message = Response(f"Some error caught, exception returned '{e}'",status = 500)
    finally:
        conn.close()
        return final_message


@bp.route('/<post_id>/image/', methods=['GET'])
def get_image(post_id):
    final_message = "Nothing happened."
    # check if image exists
    try:
        conn = get_db_connection()
        to_find = (post_id,)
        query = 'SELECT * FROM posts WHERE post_id = ?;'
        contents = conn.execute(query,to_find).fetchone()

        if contents is None:
            abort(404, "The post with this post_id does not exist.")
        elif contents["img_id"] is None or (contents["content_type"] == "text/plain" or contents["content_type"] == "text/markdown"):
            abort(404, f"The post exists, but it is not an image. Got {contents[1]}")
        elif contents["visibility"] != "public":
            abort(403, "This post exists, but it is only visible to specific users.")
        print("Successfully found the post with this image id.")

        query = "SELECT * FROM image_post WHERE img_id = ?;"

        img_visibility = conn.execute(query, (contents["img_id"],)).fetchone()
        if img_visibility is None:
            abort(404, "The post exists, but the image it references does not exist.")
        elif img_visibility["visibility"] != "public":
            abort(403, "This post exists, but the image contained is only visible to specific users.")

        content_type = contents["content_type"]
        content = img_visibility["img_url"]
        #display as HTML for testing
        #final_message = f"<img src=\"data:{content_type},{content}\"/>"
        final_message = f"data:{content_type},{content}"
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

        if image_id == "NULL":
            query = "DELETE from image_post WHERE img_id = ?;"
            conn.execute(query,(image_id,))
        else:
            # check for existence
            query = "SELECT * from image_post WHERE img_id = ? AND img_url <> ?"


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
