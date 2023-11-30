from flask import Blueprint

bp = Blueprint('requestors', __name__)

from . import routes