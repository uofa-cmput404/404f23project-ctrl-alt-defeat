from app.authors import bp


@bp.route('/')
def index():
    return 'Authors is ready to go'