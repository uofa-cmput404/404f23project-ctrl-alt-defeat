
from flask import Flask, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin import expose
from markupsafe import Markup

from flask_cors import CORS, cross_origin

from flask_basicauth import BasicAuth


db = SQLAlchemy()
basic_auth = BasicAuth()
admin = Admin()

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

class Requestor(db.Model):
    __tablename__ = "requestors"
    requestor_id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)


class RequestorView(ModelView):
    can_delete = True
    form_columns = ["requestor_id", "username", "password"]
    column_list = ["requestor_id", "username"]

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

admin.add_view(AuthorView(Author, db.session))
admin.add_view(RequestorView(Requestor, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(ImageView(Image, db.session))


def create_app():
    app = Flask(__name__)

  
    # HUGE SECURITY ISSUE - DO NOT KEEP THIS IN PRODUCTION
    # Need this so that the API allows all urls to make requests.
    # Change it so that only our web client is allowed.
    CORS(app, resources={r"/*": {"origins": "*"}})


     # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.requestors import bp as requestors_bp
    app.register_blueprint(requestors_bp, url_prefix='/requestors')   
    from app.authors import bp as authors_bp
    app.register_blueprint(authors_bp, url_prefix='/authors')   

    from app.follow import bp as follow_bp
    app.register_blueprint(follow_bp, url_prefix='/follow') 

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database.db"
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

