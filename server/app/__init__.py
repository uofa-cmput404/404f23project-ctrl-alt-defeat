from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin import expose
from markupsafe import Markup

db = SQLAlchemy()
admin = Admin()

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    passwd = db.Column(db.Text)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    images = db.relationship('Image', backref='author', lazy=True, cascade="all, delete-orphan")

class AuthorView(ModelView):
    can_delete = True
    form_columns = ["author_id", "username", "passwd"]
    column_list = ["author_id", "username", "passwd"]
    column_searchable_list = ['username']  

class Requester(db.Model):
    __tablename__ = "requesters"
    requester_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    passwd = db.Column(db.Text)


class RequesterView(ModelView):
    can_delete = True
    form_columns = ["requester_id", "username", "passwd"]
    column_list = ["requester_id", "username", "passwd"]

    @action('approve', 'Approve', 'Are you sure you want to approve selected requesters?')
    def action_approve(self, ids):
        for id in ids:
            requester = Requester.query.get(id)
            if requester:
                # Transfer requester to author
                new_author = Author(username=requester.username, passwd=requester.passwd)
                db.session.add(new_author)

                # Remove requester
                db.session.delete(requester)
                    
        db.session.commit()
        # navigate to the index_view of the RequesterView
        return redirect(url_for('.index_view'))
    


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
class PostView(ModelView):
    can_delete = True
    form_columns = ["post_id", "title", "content", "author_id"]
    column_list = ["post_id", "title", "content", "author_id"]  
    column_searchable_list = ["author_id","title"]

class Image(db.Model):
    __tablename__ = "image_post"
    img_id = db.Column(db.Text, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)  
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))

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

admin.add_view(AuthorView(Author, db.session))
admin.add_view(RequesterView(Requester, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(ImageView(Image, db.session))


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database.db"
    app.config["SECRET_KEY"] = "mysecret"

    db.init_app(app)
    admin.init_app(app)

    return app
