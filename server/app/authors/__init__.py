from flask import Blueprint

bp = Blueprint('authors', __name__)

from app.authors import routes