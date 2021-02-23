# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from app.module import error
from conf import conf


db = SQLAlchemy()
migrate = Migrate()
redis = FlaskRedis()


def create_app():
    app = Flask(__name__)
    app.config.from_object(obj=__import__("config"))

    @app.before_request
    def set_global():
        g.title = conf['app']['title']

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"            # Clickjacking
        response.headers['X-XSS-Protection'] = "1"              # Cross-site scripting
        response.headers['X-Content-Type-Options'] = "nosniff"  # Check MIMETYPE

        if request.path.endswith(".css"):
            response.headers['Content-Type'] = "text/css; charset=utf-8"
        if request.path.endswith(".txt"):
            response.headers['Content-Type'] = "text/plain; charset=utf-8"

        if request.path.endswith(".json"):
            response.headers['Content-Type'] = "application/json; charset=utf-8"
        if request.path.endswith(".js"):
            response.headers['Content-Type'] = "application/javascript; charset=utf-8"

        response.headers['X-Powered-By'] = "chick_0"
        return response

    # DB 모델 등록
    __import__("models")

    # ORM 등록 & 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    # Redis 초기화
    redis.init_app(app)

    from app import views
    for view_point in views.__all__:
        try:
            app.register_blueprint(   # 블루프린트 등록시도
                blueprint=getattr(getattr(views, view_point), "bp")
            )
        except AttributeError:        # 블루프린트 객체가 없다면
            print(f"[!] '{view_point}' 는 뷰 포인트가 아닙니다")

    # 오류 핸들러
    app.register_error_handler(403, error.page_not_found)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(405, error.method_not_allowed)

    app.register_error_handler(500, error.internal_server_error)

    return app
