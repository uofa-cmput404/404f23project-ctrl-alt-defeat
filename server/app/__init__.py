from flask import Flask


def create_app():
    app = Flask(__name__)

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')    

    from app.sample import bp as sample_bp
    app.register_blueprint(sample_bp, url_prefix='/sample') 

    @app.route('/test/')
    def test():
        return 'Hello world'
    

    return app