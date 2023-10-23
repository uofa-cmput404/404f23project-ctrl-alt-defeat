from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    
    # HUGE SECURITY ISSUE - DO NOT KEEP THIS IN PRODUCTION
    # Need this so that the API allows all urls to make requests.
    # Change it so that only our web client is allowed.
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.authors import bp as authors_bp
    app.register_blueprint(authors_bp, url_prefix='/authors')

    from app.sample import bp as sample_bp
    app.register_blueprint(sample_bp, url_prefix='/sample') 

    @app.route('/test/')
    def test():
        return 'Hello world'    

    return app