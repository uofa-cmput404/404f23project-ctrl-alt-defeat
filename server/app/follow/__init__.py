from flask import Blueprint

bp = Blueprint('follow', __name__)

from . import routes