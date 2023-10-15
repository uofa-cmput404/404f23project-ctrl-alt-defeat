from app.main import bp


@bp.route('/')
def index():
    return 'This is The Main Blueprint'