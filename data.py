from typing import List, Dict
from hashlib import md5
import random
import os
import torch
import matplotlib.pyplot as plt

from flask import request, flash
from flask_login import current_user
from sqlalchemy import desc, func
from werkzeug.utils import secure_filename

from aflat.nn import Generator
from aflat.main import db
from aflat.models import User, Comment, Post, PostScore


gen = Generator(512, 512)
gen.load_state_dict(
    torch.load("./gan/generator.pth", map_location=torch.device("cpu"))["state_dict"]
)

TITLES = [
    "Painting in case of a zombie apocalypse",
    "Paintings technique that changed my life forever",
    "Paintings frying around",
    "Painting you’ll encounter during your next trip",
    "Painting from a dog’s perspective",
    "Never trust paintings",
    "Most footballers have paintings for breakfast",
    "Painting that will make you a painting",
    "Paintings’s adventure",
    "Demystifying paintings",
    "Keep calm and think about paintings",
    "Painting fail",
    "The prehistoric painting",
    "Zombie painting is better than sleeping",
]
EXTENSIONS = ["png", "jpg", "jpeg", "git", "avif"]
POSTS_PATH = "./static/generated/"


def comments_data(id_: int) -> List[Dict]:
    comments_json = []
    comments = Comment.query.filter_by(post_id=id_).all()

    for com in reversed(comments):
        comments_json.append(
            {
                "username": User.query.filter_by(id=com.user_id).first().username,
                "date": com.date,
                "content": com.content,
            }
        )
    return comments_json


def users_comments_data():
    users = User.query
    users_json = []
    for user in users.all():
        users_json.append({"id": user.id, "username": user.username})

    comments = Comment.query.all()
    comments_json = []
    for comment in reversed(comments):
        comments_json.append(
            {
                "date": comment.date,
                "post_id": comment.post_id,
                "username": users.filter_by(id=comment.user_id).first().username,
                "content": comment.content,
            }
        )
    return [users_json, comments_json]


def paintings_data(page=0) -> Dict:
    start = page * 5
    posts = Post.query.order_by(desc(Post.id))[start : start + 5]

    posts_json = []
    for post in posts:
        comment_count = Comment.query.filter_by(post_id=post.id).count()
        posts_json.append(
            {
                "id": post.id,
                "title": post.title,
                "filename": post.picture_filename,
                "comments_num": comment_count,
            }
        )
    return posts_json


def paintings_count_data():
    return Post.query.count()


def painting_data(id_) -> Dict:
    post = Post.query.get(id_)
    return {"id": post.id, "title": post.title, "filename": post.picture_filename}


def new_painting():
    noise = torch.randn(1, 512, 1, 1, dtype=torch.float32)
    with torch.no_grad():
        img = gen.forward(noise, 1, 6) * 0.5 + 0.5

    plt.imsave("./static/generated/tmp.jpg", img[0].permute(1, 2, 0).numpy())


def publish_painting():
    post = Post.query.order_by(Post.id.desc()).first()
    user = User.query.filter_by(username=current_user.username).first()
    if post:
        os.rename("./static/generated/tmp.jpg", f"./static/generated/{post.id+1}.jpg")
        new_post = Post(
            title=random.choice(TITLES),
            picture_filename=f"/generated/{post.id+1}.jpg",
            user_post=user,
        )
    else:
        os.rename("./static/generated/tmp.jpg", "./static/generated/1.jpg")
        new_post = Post(
            title=random.choice(TITLES),
            picture_filename="/generated/1.jpg",
            user_post=user,
        )
    db.session.add(new_post)
    db.session.commit()


def check_extension(fn):
    return fn.split(".")[-1] in EXTENSIONS


def new_filename(fn, file):
    extension = "." + fn.split(".")[-1]
    return md5(file).hexdigest() + extension


def generated_directory():
    if os.path.isdir("./static/generated/"):
        return True
    try:
        os.mkdir("./static/generated")
    except:
        return False
    return True


def publish_post():
    title = request.form.get("title")
    if title == "":
        flash("No title!")
        return False
    if "image" not in request.files:
        flash("No image")
        return False
    file = request.files["image"]

    if file.filename == "":
        flash("No image")
        return False
    if check_extension(file.filename):
        filename = secure_filename(file.filename)
        filename = new_filename(filename, file.stream.read())
        path = os.path.join(POSTS_PATH, filename)

        if not generated_directory():
            flash("Hmmm error or smth....")
            return False

        file.stream.seek(0)
        file.save(path)

        user = User.query.filter_by(username=current_user.username).first()
        new_post = Post(
            title=title, picture_filename="generated/" + filename, user_post=user
        )
        db.session.add(new_post)
        db.session.commit()
        return True

    flash("Wrong file!")
    return False


def stonks_db(id_, username):
    user = User.query.filter_by(username=current_user.username).first()
    stonk = PostScore.query.filter_by(post_score=user, post_id=id_).first()
    if not stonk:
        new_stonk = PostScore(user_stonk=user, post_id=id_)
        db.session.add(new_stonk)
        db.session.commit()
    else:
        db.session.delete(stonk)
        db.session.commit()


def get_stonk(id_, username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    stonk = PostScore.query.filter_by(user_id=user.id, post_id=id_).first()
    if stonk:
        return True
    return False


def popular_data():
    popular = (
        PostScore.query.with_entities(PostScore.post_id, func.count(PostScore.post_id))
        .group_by(PostScore.post_id)
        .all()
    )

    popular_json = []
    for post in sorted(popular, key=lambda k: k[1], reverse=True)[:10]:
        p = Post.query.filter_by(id=post[0]).first()
        popular_json.append(
            {"id": post[0], "title": p.title, "filename": p.picture_filename}
        )
    return popular_json
