# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect, url_for

from models import Post


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("")
def search():
    query = request.args.get("query", "")

    if len(query) == 0:
        return redirect(url_for("index.index") + "?work=search&return=qn")

    context = Post.query.filter(
        Post.title.like(f"%{query}%")
    ).order_by(
        Post.idx.desc()
    ).limit(30).all()

    if len(context) == 0:
        return redirect(url_for("index.index") + "?work=search&return=rn")

    return render_template(
        "search/search.html",
        context=context
    )
