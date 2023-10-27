from flask import Blueprint

bp = Blueprint('follow', __name__)

from app.follow import routes