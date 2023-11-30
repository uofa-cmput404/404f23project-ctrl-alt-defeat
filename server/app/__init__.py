
from flask import Flask, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin import expose
from markupsafe import Markup
from flask_swagger_ui import get_swaggerui_blueprint

from flask_cors import CORS, cross_origin

from flask_httpauth import HTTPBasicAuth
import urllib.parse as urlparse
import os
from dotenv import load_dotenv
from .dbase import get_db_connection # Used in verify_backend_access
from flask_basicauth import BasicAuth
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()
basic_auth = HTTPBasicAuth()
admin = Admin()

# This is to verify back-end access for nodes.
@basic_auth.verify_password
def verify_backend_access(username, password):
    print("verifying...")
    response = None # equivalent to 401 Unauthorized
    conn, cur = get_db_connection()

    if username == "front-end": # TODO: remove this in future
        return {'message': 'Authenticated through origin front-end'}

    query = "SELECT node_id, password FROM nodes WHERE username = %s"
    cur.execute(query, (username,))
    node = cur.fetchone()

    if node:
        stored_password = node['password']
        if password == stored_password:
            response = {'message': "Authenticated", 'node_id': node['node_id']}
    conn.close()

    return response

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    images = db.relationship('Image', backref='author', lazy=True, cascade="all, delete-orphan")

class AuthorView(ModelView):
    can_delete = True
    form_columns = ["author_id", "username", "password"]
    column_list = ["author_id", "username"]
    column_searchable_list = ['username'] 

    def on_model_change(self, form, model, is_created):
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(model.password).decode('utf-8')
        model.password = hashed_password 

class Requestor(db.Model):
    __tablename__ = "requestors"
    requestor_id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)


class RequestorView(ModelView):
    can_delete = True
    form_columns = ["requestor_id", "username", "password"]
    column_list = ["requestor_id", "username"]

    def on_model_change(self, form, model, is_created):
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(model.password).decode('utf-8')
        model.password = hashed_password

    @action('approve', 'Approve', 'Are you sure you want to approve selected requesters?')
    def action_approve(self, ids):
        for id in ids:
            requestor = Requestor.query.get(id)
            if requestor:
                # Transfer requestor to author
                new_author = Author(author_id=requestor.requestor_id, username=requestor.username, password=requestor.password)
                db.session.add(new_author)

                # Remove requestor
                db.session.delete(requestor)
                    
        db.session.commit()
        # navigate to the index_view of the RequestorView
        return redirect(url_for('.index_view'))



class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Text, db.ForeignKey('authors.author_id'))
class PostView(ModelView):
    can_delete = True
    form_columns = ["post_id", "title", "content", "author_id"]
    column_list = ["post_id", "title", "content", "author_id"]  
    column_searchable_list = ["author_id","title"]

class Image(db.Model):
    __tablename__ = "image_post"
    img_id = db.Column(db.Text, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)  
    author_id = db.Column(db.Text, db.ForeignKey('authors.author_id'))

class ImageView(ModelView):
    can_delete = True
    form_columns = ["img_id", "img_url", "author_id"]
    column_list = ["img_id", "author_id", "view_button"]
    column_searchable_list = ["author_id"]
    def view_button(view, context, model, name):
        return Markup(f'<a href="{model.img_url}" target="_blank">View</a>')
    
    column_formatters = {
        'view_button': view_button
    }
    column_labels = dict(view_button='View Image')
class Friend(db.Model):
    __tablename__ = 'friends'
    author_followee = db.Column(db.Text, db.ForeignKey('authors.author_id'), primary_key=True)
    author_following = db.Column(db.Text, db.ForeignKey('authors.author_id'), primary_key=True)

class Node(db.Model):
    __tablename__ = "nodes"
    node_id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.Text)    
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

class NodeView(ModelView):
    can_delete = True
    form_columns = ["node_id", "node_name", "username", "password"]
    column_list = ["node_id", "node_name", "username"]
    column_searchable_list = ["node_name"]  

admin.add_view(AuthorView(Author, db.session))
admin.add_view(RequestorView(Requestor, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(NodeView(Node, db.session))


def create_app():
    app = Flask(__name__)

    load_dotenv()

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

  
    # HUGE SECURITY ISSUE - DO NOT KEEP THIS IN PRODUCTION
    # Need this so that the API allows all urls to make requests.
    # Change it so that only our web client is allowed.
    CORS(app, resources={r"/*": {"origins": "*"}})

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = os.environ['URL'] + "/swagger"  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Ctrl + Alt + Defeat Social Distribution"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

  
    # HUGE SECURITY ISSUE - DO NOT KEEP THIS IN PRODUCTION
    # Need this so that the API allows all urls to make requests.
    # Change it so that only our web client is allowed.
    CORS(app, resources={r"/*": {"origins": "*"}})


     # Register blueprints here
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .requestors import bp as requestors_bp
    app.register_blueprint(requestors_bp, url_prefix='/api/requestors')  # The only route that doesn't get affect is requestors
    
    from .authors import bp as authors_bp
    app.register_blueprint(authors_bp, url_prefix='/api')   

    from .follow import bp as follow_bp
    app.register_blueprint(follow_bp, url_prefix='/api') 

    from .posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/api')

    @app.route("/swagger")
    def swagger_json():
        # Depending if this file is opened from the root folder,
        # or `server` folder, it will get 
        # the appropiate swagger.json path.
        if os.path.exists(os.path.join(os.getcwd(), 'server/app')):
            swagger_path = "swagger.json"
        else:
            swagger_path = "../swagger.json"
        # Load your Swagger JSON file here
        with open(swagger_path, 'r') as f:
            swagger_json = f.read()
        return swagger_json


    app.register_blueprint(swaggerui_blueprint)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%s:%s@%s:%d/%s" % (user, password, host, port, dbname)
    app.config["SECRET_KEY"] = "mysecret"

    # New route for fetching friends' posts
    @app.route('/<author_id>/friends_posts')
    def get_friends_posts(author_id):
        # Fetch friends of the given author
        friends_ids = db.session.query(Friend.author_following).filter(Friend.author_followee == author_id).all()
        friends_ids += db.session.query(Friend.author_followee).filter(Friend.author_following == author_id).all()

        # Flatten the list of tuples to a list of IDs
        friends_ids = [fid[0] for fid in friends_ids]

        # Fetch posts made by friends
        friends_posts = db.session.query(Post).filter(Post.author_id.in_(friends_ids)).all()

        # Format and return the posts
        posts_data = [{'post_id': post.post_id, 'title': post.title, 'content': post.content} for post in friends_posts]
        return jsonify(posts_data)

    db.init_app(app)
    admin.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)