# -*- coding: utf-8 -*-
from json import dumps
from hashlib import sha384

from flask import Blueprint
from flask import request
from flask import Response

from app import db
from models import Post, Comment


bp = Blueprint(
    name=__name__.split(".")[-1],
    import_name=__name__,
    url_prefix=f"/{__name__.split('.')[-1]}"
)


def send(obj, code=200):
    return Response(
        response=dumps(obj),
        mimetype="application/json"
    ), code


@bp.route("/get/<int:idx>")
def get(idx: int):
    cm_list = []
    for ctx in Comment.query.filter_by(post=idx).all():
        cm_list.append({
            "date": ctx.date.strftime("%Y-%m-%d %H:%M:%S"),
            "text": ctx.text,
            "comment": ctx.idx
        })

    return send(obj=cm_list)


@bp.route("/add/<int:idx>", methods=['POST'])
def add(idx: int):
    if Post.query.filter_by(idx=idx).first() is None:
        return send(obj={"msg": "등록되지 않은 게시글 입니다"},
                    code=400)

    text = request.form.get("text", "")
    password = request.form.get("password", "")

    if len(text) == 0:
        return send(obj={"msg": "댓글의 내용이 빈칸 입니다"})
    if len(password) == 0:
        return send(obj={"msg": "댓글의 비밀번호가 빈칸 입니다"})

    if len(Comment.query.filter_by(post=idx).all()) < 30:
        ctx = Comment(
            post=idx,
            text=text,
            password=sha384(password.encode()).hexdigest()
        )
        db.session.add(ctx)
        db.session.commit()

        return send(obj={"msg": "등록되었습니다"})
    else:
        return send(obj={"msg": "더 이상 댓글을 달 수 없습니다"})


@bp.route("/delete/<int:idx>/<int:comment>", methods=['POST'])
def delete(idx: int, comment: int):
    password = request.form.get("password", "")
    if len(password) == 0:
        return send(obj={"msg": "비밀번호를 입력해야 합니다"})

    ctx = Comment.query.filter_by(
        idx=comment,
        post=idx,
        password=sha384(password.encode()).hexdigest()
    ).first()

    if ctx is None:
        return send(obj={"msg": "댓글을 삭제하지 못함"})

    db.session.delete(ctx)
    db.session.commit()

    return send(obj={"msg": "댓글 삭제됨"})
