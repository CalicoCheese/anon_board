#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path, mkdir
from datetime import datetime
from logging import getLogger, FileHandler

from waitress import serve
from paste.translogger import TransLogger

import app
from conf import conf


LOG_PATH = path.join("log")

if __name__ == "__main__":
    if not path.isdir(path.join(LOG_PATH)):
        mkdir(LOG_PATH)

    logger = getLogger(
        name="wsgi"
    )

    logger.addHandler(
        hdlr=FileHandler(
            filename=path.join(LOG_PATH, f"{datetime.today().strftime('%Y-%m-%d %Hh %Mm %Ss')}.log")
        )
    )

    app = app.create_app()
    serve(
        app=TransLogger(
            application=app,
            setup_console_handler=True
        ),
        port=conf['server']['port']
    )
