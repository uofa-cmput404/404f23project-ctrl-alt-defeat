from flask import Blueprint

bp = Blueprint('authors', __name__)

from . import routes