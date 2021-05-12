import datetime
import bcrypt

from flask_login import UserMixin

from aflat.main import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(127))
    posts = db.relationship("Post", backref="user_post")
    stonks = db.relationship("PostScore", backref="user_stonk")
    comments = db.relationship("Comment", backref="user_comment")

    def check_password(self, password):
        if bcrypt.checkpw(password.encode(), self.password):
            return True
        return False

    @property
    def passwd(self):
        return self.password

    @passwd.setter
    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    content = db.Column(db.String(2048))
    date = db.Column(db.Date, default=datetime.datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment = db.relationship("Comment", backref="post_comment")
    score = db.relationship("PostScore", backref="post_score")
    title = db.Column(db.String(255))
    picture_filename = db.Column(db.String(512))


class PostScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
