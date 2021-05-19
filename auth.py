from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user

from aflat.models import User, Comment, Post
from aflat.data import (
    users_comments_data,
    new_painting,
    publish_painting,
    publish_post,
    popular_data,
    stonks_db,
)
from aflat.main import db

auth = Blueprint("auth", __name__)


@auth.route("/comment", methods=["POST"])
@login_required
def add_comment():
    comment = request.json
    username = current_user.username
    content = comment["comment"]
    id_ = comment["id"]
    if not content or not id_:
        return jsonify({"ok": False, "error":"empty comment or id of post"})

    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(id=id_).first()
    new_comment = Comment(user_comment=user, content=content, post_comment=post)

    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"ok": True})


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/signup", methods=["POST"])
def signup():
    username = request.json["username"]
    password = request.json["password"]
    if not username or not password:
        return jsonify({"ok": False,"error":"Empty password or username"})
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"ok": False,"error":"Username taken"})

    new_user = User(username=username, hash_password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"ok": True})


@auth.route("/login", methods=["POST"])
def login_():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash("Username or password incorrect")
        return redirect(url_for("auth.login"))

    login_user(user, remember=True)
    return redirect(url_for("main.index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/management")
@login_required
def management():
    if current_user.username == "admin":
        return render_template(
            "management.html", data=users_comments_data(), title="Admin panel"
        )
    return redirect(url_for("main.index"))


@auth.route("/management", methods=["POST"])
@login_required
def management_():
    if current_user.username == "admin":
        delete = request.json
        User.query.filter_by(username=delete["username"]).delete()
        db.session.commit()
        return {"ok": True}

    return {"ok": False}


@auth.route("/generate")
@login_required
def generate_image():
    new_painting()
    return {"path": url_for("static", filename="generated/tmp.jpg")}


@auth.route("/publish")
@login_required
def publish_image():
    publish_painting()
    return {"ok": True}


@auth.route("/stonks", methods=["POST"])
@login_required
def stonks():
    try:
        id_ = int(request.json["post_id"])
    except:
        return {"ok": False}

    stonks_db(id_, current_user.username)
    return {"ok": True}


@auth.route("/new")
@login_required
def new_post():
    return render_template("new.html")


@auth.route("/new", methods=["POST"])
@login_required
def post_new_post():
    if publish_post():
        return redirect(url_for("main.index"))
    return redirect(url_for("auth.new_post"))
