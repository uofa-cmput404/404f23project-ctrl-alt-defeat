from . import bp
from . import get_db_connection
from flask import abort, request
from werkzeug.exceptions import HTTPException


@bp.route('/')
def index():
    return 'This is The Main Blueprint'

