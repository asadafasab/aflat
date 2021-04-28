import datetime
import bcrypt

from flask_login import UserMixin

from aflat.main import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(127))

    def check_password(self, password):
        if bcrypt.checkpw(password.encode(), self.password):
            return True
        return False

    @property
    def passwd():
        return self.password

    @passwd.setter
    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    username = db.Column(db.String(127))
    content = db.Column(db.String(2048))
    date = db.Column(db.Date, default=datetime.datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    picture_filename = db.Column(db.String(512))


class PostScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127))
    post_id = db.Column(db.Integer)
