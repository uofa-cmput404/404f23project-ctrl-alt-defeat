from flask import render_template
from app.posts import bp

@bp.route('/')
def index():
    return "Hi!"

@bp.route('/test/')
def categories():
    return "Test route for /posts"