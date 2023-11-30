from flask import Blueprint

bp = Blueprint('sample', __name__)


from . import routes