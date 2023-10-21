from flask import Blueprint

bp = Blueprint('new_post', __name__)


from app.new_post import routes