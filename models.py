# -*- coding: utf-8 -*-

from sqlalchemy import func

from app import db


class Post(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    title = db.Column(
        db.String(90),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    password = db.Column(
        db.String(96),
        nullable=False
    )

    def __init__(self, title: str, text: str, password: str):
        self.title = title
        self.text = text
        self.password = password

    def __repr__(self):
        return f"<Post idx={self.idx}, title={self.title!r}>"


class Comment(db.Model):
    idx = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    post = db.Column(
        db.Integer,
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    password = db.Column(
        db.String(96),
        nullable=False
    )

    def __init__(self, post: int, text: str, password: str):
        self.post = post
        self.text = text
        self.password = password

    def __repr__(self):
        return f"<Post idx={self.idx}, post={self.post}>"
