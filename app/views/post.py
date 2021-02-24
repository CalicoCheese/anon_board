# -*- coding: utf-8 -*-
from hashlib import sha384
from secrets import token_bytes

from flask import Blueprint
from flask import request, session, g
from flask import render_template
from flask import abort
from flask import redirect, url_for

from app import db
from app.module.cache import add_cache, get_cache
from models import Post


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


@bp.route("/", methods=['GET', 'POST'])
def write():
    if request.method == "GET":
        session['csrf_token'] = token_bytes(32).hex()

        g.use_markdown = True
        return render_template(
            "post/write.html",
            csrf_token=session['csrf_token']
        )

    if request.method == "POST":
        if request.referrer is None:
            abort(400)

        title = request.form.get("title")
        text = request.form.get("text")
        password = request.form.get("password")

        if len(title) == 0:
            return redirect(url_for(".write") + "?missing=title")

        if len(text) == 0:
            return redirect(url_for(".write") + "?missing=text")

        if len(password) == 0:
            return redirect(url_for(".write") + "?missing=password")

        if request.form.get("csrf_token") != session.get("csrf_token"):
            return redirect(url_for(".write") + "?wrong=csrf")

        ctx = Post(
            title=title,
            text=text,
            password=sha384(password.encode()).hexdigest()
        )

        db.session.add(ctx)
        db.session.commit()

        del session['csrf_token']

        return redirect(url_for("index.index") + f"?work=write&idx={ctx.idx}")


@bp.route("/<int:idx>")
def read(idx: int):
    ctx = get_cache(idx=idx)
    if ctx is None:
        ctx = Post.query.filter_by(
            idx=idx
        ).first()

        if ctx is None:
            abort(404)
        else:
            add_cache(
                idx=idx,
                title=ctx.title,
                text=ctx.text,
                date=ctx.date
            )

    g.use_markdown = True
    return render_template(
        "post/read.html",
        ctx=ctx
    )


@bp.route("/delete/<int:idx>", methods=['POST'])
def delete(idx: int):
    if request.referrer is None:
        abort(400)

    ctx = Post.query.filter_by(
        idx=idx,
        password=sha384(request.form.get("password").encode()).hexdigest()
    ).first()

    if ctx is None:
        return redirect(url_for("index.index") + "?work=delete&return=fail")
    else:
        db.session.delete(ctx)
        db.session.commit()
        return redirect(url_for("index.index") + "?work=delete&return=ok")
