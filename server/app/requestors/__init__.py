from flask import Blueprint

bp = Blueprint('requestors', __name__)

from app.requestors import routes