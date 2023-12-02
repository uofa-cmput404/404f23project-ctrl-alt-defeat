from flask import render_template
from . import bp

@bp.route('/')
def index():
    return "Hi from sample"

@bp.route('/test/')
def categories():
    return "Test route for /sample"