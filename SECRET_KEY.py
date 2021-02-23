# -*- coding: utf-8 -*-
from os import path
from secrets import token_bytes


if not path.exists(".SECRET_KEY"):
    SECRET_KEY = token_bytes(32)

    with open(".SECRET_KEY", mode="wb") as fp:
        fp.write(SECRET_KEY)
else:
    print("'SECRET_KEY' 는 이미 만들어져 있습니다")
