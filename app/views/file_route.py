# -*- coding: utf-8 -*-

from flask import Blueprint, send_file

bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix="/"
)


@bp.route("/robots.txt")
def robots():
    return send_file(
        "static/robots.txt",
        mimetype="text/plain"
    )
