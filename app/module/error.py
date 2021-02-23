# -*- coding: utf-8 -*-

from flask import render_template


def render(title, message, code):
    return render_template(
        "error/error.html",
        title=title,

        message=message
    ), code


def bad_request(error):
    title = "잘못된 요청"
    message = "잘못된 요청입니다"

    code = getattr(error, "code")

    return render(title, message, code)


def page_not_found(error):
    title = "페이지를 찾을 수 없음"
    message = "해당 페이지를 찾을 수 없습니다"

    code = getattr(error, "code")

    return render(title, message, code)


def method_not_allowed(error):
    title = "잘못된 요청"
    message = "순서가 잘못되었습니다"

    code = getattr(error, "code")

    return render(title, message, code)


def internal_server_error(error):
    title = "스크립트 오류 발생"
    message = "내부 스크립트 오류가 발생하였습니다"

    code = getattr(error, "code")

    return render(title, message, code)
