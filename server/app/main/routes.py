from app.main import bp
from app.db import get_db_connection
from flask import abort, request
from werkzeug.exceptions import HTTPException


@bp.route('/')
def index():
    return 'This is The Main Blueprint'


@bp.route('/service/authors/<author_id>/posts/<post_id>/image', methods=['GET'])
def get_image(author_id, post_id):
    # check if image exists
    try:
        pass
    except:
        pass
    return None


@bp.route('/service/authors/<author_id>/posts/<post_id>', methods=['POST'])
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
            abort(404)
    except HTTPException as e:
        print(e.code, " Can't find post_id.")
        final_message = str(e)

    # Get the new data.
    try:
        request_data = request.get_json()
    except Exception as e:
        print(e, "This is (probably) not a valid JSON file. Or it was sent as key/value pairs.")
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
    try:
        query = "UPDATE posts SET title = ?, content_type = ?,content = ?, img_id = ?, visibility = ? WHERE post_id = ? AND author_id = ?"
        conn.execute(query, (title, content_type, content, image_id, visibility, post_id, author_id))
        conn.commit()
    except Exception as e:
        print(e, "Data not written to database. Rolling back...")
        final_message = str(e)
        conn.rollback()
    finally:
        conn.close()

    return final_message
