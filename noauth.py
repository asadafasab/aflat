from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from aflat.data import (
    comments_data,
    popular_data,
    painting_data,
    paintings_data,
    get_stonk,
    paintings_count_data,
)

noauth = Blueprint("main", __name__)


@noauth.route("/")
@noauth.route("/home")
def index():
    if "page" not in request.args:
        return render_template(
            "index.html",
            page=1,
            stonk=get_stonk,
            popular=popular_data(),
            paintings=paintings_data(),
            title="Home",
        )

    try:
        page = int(request.args.get("page"))
    except:
        return render_template(
            "index.html",
            page=1,
            stonk=get_stonk,
            popular=popular_data(),
            paintings=paintings_data(),
            title="Home",
        )

    count_pages = int(paintings_count_data() / 5)
    if page > count_pages:
        page = count_pages
    return render_template(
        "index.html",
        page=page + 1,
        stonk=get_stonk,
        popular=popular_data(),
        paintings=paintings_data(page),
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
        popular=popular_data(),
        login=login,
        data=painting_data(id_),
        comments=comments_data(id_),
    )


@noauth.route("/about")
def about():
    return render_template("about.html", title="About")


@noauth.route("/account")
def account():
    return render_template("about.html", title="Account")
