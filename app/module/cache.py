# -*- coding: utf-8 -*-
from datetime import datetime
from json import dumps, loads

from app import redis


class Post:
    idx = 0
    title = ""
    text = ""
    date = None
    password = None


def add_cache(idx: int, title: str, text: str, date: datetime):
    cache = {
        "title": title,
        "text": text,
        "date": date.strftime("%Y-%m-%d %H:%M:%S")
    }

    redis.set(idx, dumps(cache))


def get_cache(idx: int):
    cache = redis.get(idx)
    if cache is None:
        return None

    cache = loads(cache)

    ctx = Post()
    ctx.idx = idx
    ctx.title = cache.get("title")
    ctx.text = cache.get("text")
    ctx.date = cache.get("date")

    return ctx
