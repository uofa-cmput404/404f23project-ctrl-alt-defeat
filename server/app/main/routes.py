from . import bp
from flask import abort, request
from werkzeug.exceptions import HTTPException


@bp.route('/')
def index():
    return "/admin for admin dashboard.<br>/author_id/friends_posts for getting the posts of an author's friends."

