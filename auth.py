from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user

from aflat.models import User, Comment
from aflat.data import users_comments, new_painting, publish_painting, stonks_db, popular_db
from aflat.main import db

auth = Blueprint("auth", __name__)


@auth.route("/comment", methods=["POST"])
@login_required
def comment():
    comment = request.json
    user = current_user.username
    content = comment["comment"]
    if not content:
        return jsonify({"ok": False})
    id_ = comment["id"]
    new_comment = Comment(username=user, content=content, post_id=id_)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"ok": True})


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=["POST"])
def signup_():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Username taken")
        return redirect(url_for("auth.signup"))

    new_user = User(username=username, hash_password=password)

    db.session.add(new_user)
    db.session.commit()
    flash("Now you can log in")

    return redirect(url_for("auth.login"))


@auth.route('/login', methods=["POST"])
def login_():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        flash("Username or password incorrect")
        return redirect(url_for("auth.login"))

    login_user(user, remember=True)
    return redirect(url_for("main.index"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/management")
@login_required
def management():
    if current_user.username == "admin":
        return render_template("management.html", data=users_comments(), title="Admin panel")
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
    print(popular_db())
    try:
        id_ = int(request.json["post_id"])
    except:
        return {"ok": False}

    stonks_db(id_, current_user.username)
    return {"ok": True}
