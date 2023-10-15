from flask import Blueprint

bp = Blueprint('sample', __name__)


from app.sample import routes