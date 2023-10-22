from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from app.requestors import bp as requestors_bp
from app.authors import bp as authors_bp

db = SQLAlchemy()
basic_auth = BasicAuth()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.requestors import bp as requestors_bp
    app.register_blueprint(requestors_bp, url_prefix='/requestors')   

    from app.authors import bp as authors_bp
    app.register_blueprint(authors_bp, url_prefix='/authors')   

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')    

    from app.sample import bp as sample_bp
    app.register_blueprint(sample_bp, url_prefix='/sample') 


    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    # db.init_app(app)

    # Basic Authentication settings
    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = '1234'
    basic_auth.init_app(app)

    @app.route('/test/')
    def test():
        return 'Hello world'
    
    return app