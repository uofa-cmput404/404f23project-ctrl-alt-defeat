from app.main import bp
from app.dbase import get_db_connection
from flask import abort, request, Response, redirect
from werkzeug.exceptions import HTTPException

@bp.route('/')
def index():
    return 'This is The Main Blueprint'


# adhering to API spec in requirements
@bp.route("/authors/<author_id>/posts/<post_id>/image/",methods=["GET"])
def get_image_as_base64(author_id, post_id):
    """
    An endpoint to retrieve an base64 encoded image.
    This is ready to be embedded in a <img> tag, such as in HTML or Markdown.
    :param author_id: A unique identifier for the author.
    :param post_id: A unique identifier for the post.
    :return: A base64 encoded JPEG/PNG, with data: URI.
    """
    final_message = Response(response="Nothing happened.",status=500)
    # check if post exists
    conn = get_db_connection()
    try:
        # the author_id is quite redundant as post_ids are unique.
        if author_id != "NONE":
            query = "SELECT post_id, content_type, visibility,content FROM posts WHERE post_id = ? AND author_id = ?"
            row = conn.execute(query, (post_id, author_id)).fetchall()
        else: # no author_id fallback
            query = "SELECT post_id, content_type, visibility,content FROM posts WHERE post_id = ?"
            row = conn.execute(query, (post_id,)).fetchall()
        print(row)
        if row is None:
            abort(404, "The post does not exist.")
        if len(row) > 1:
            abort(404, "Cannot disambiguate more than one post. Specify an author_id to narrow it down.")
        row = row[0]
        if row["visibility"] != "public":
            abort(404, "This is not public.")
        if row["content_type"] not in ["image/png;base64", "image/jpeg;base64"]:
            abort(404,"This is not a base64 encoded JPEG/PNG image.")

        content_type = row["content_type"]
        content = row["content"]
        final_message = f"data:{content_type},{content}"
        return redirect(final_message, code=302)
    except HTTPException as e:
        final_message = str(e)
        print(final_message)
    finally:
        conn.close()
        return final_message
