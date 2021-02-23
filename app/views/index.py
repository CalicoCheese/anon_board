# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import render_template

from models import Post


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/ok")
def ok():
    return "OK", 200


@bp.route("/")
def index():
    try:
        page = int(request.args.get("page", "1"))

        if page < 1:
            page = 1
    except ValueError:
        page = 1

    context = Post.query.order_by(
        Post.idx.desc()
    ).paginate(page)

    return render_template(
        "index/index.html",
        context=context
    )
