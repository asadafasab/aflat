from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from aflat.main import db
from aflat.data import *
from aflat.models import User, Comment

noauth = Blueprint("main", __name__)


@noauth.route("/")
@noauth.route("/home")
def index():
    if "page" not in request.args:
        return render_template(
            "index.html",
            page=1,
            stonk=get_stonk,
            popular=popular_db(),
            paintings=paintings_db(),
            title="Home",
        )

    try:
        page = int(request.args.get("page"))
    except:
        return render_template(
            "index.html",
            page=1,
            stonk=get_stonk,
            paintings=paintings_db(),
            title="Home",
        )

    count_pages = int(paintings_count() / 5)
    if page > count_pages:
        page = count_pages
    return render_template(
        "index.html",
        page=page + 1,
        stonk=get_stonk,
        paintings=paintings_db(page),
        title="Home",
    )


@noauth.route("/painting")
def painting():
    login = current_user.is_authenticated
    if "id" not in request.args:
        return redirect(url_for("main.index"))

    try:
        id_ = int(request.args.get("id"))
    except:
        return redirect(url_for("main.index"))

    return render_template(
        "painting.html",
        popular=popular_db(),
        login=login,
        data=painting_db(id_),
        comments=comments(id_),
    )


@noauth.route("/about")
def about():
    return render_template("about.html", title="About")


@noauth.route("/account")
def account():
    return render_template("about.html", title="Account")
