# -*- coding: utf-8 -*-

from conf import conf

# # # # # # # # # # # # # # # # # # # # # #

# Redis 데이터베이스
REDIS_URL = conf['redis']['url']

# 관계형 데이터베이스
SQLALCHEMY_DATABASE_URI = conf['db']['url']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# # # # # # # # # # # # # # # # # # # # # #

# 세션 용 시크릿 키
try:
    SECRET_KEY = open(".SECRET_KEY", mode="rb").read()
except FileNotFoundError:
    SECRET_KEY = getattr(__import__("SECRET_KEY"), "SECRET_KEY")

# 세션 쿠키 설정
SESSION_COOKIE_NAME = "s"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"

# # # # # # # # # # # # # # # # # # # # # #
