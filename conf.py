# -*- coding: utf-8 -*-
from os import path, mkdir, listdir
from configparser import ConfigParser

if not path.exists("conf"):
    mkdir("conf")

conf = ConfigParser()
conf.read(
    filenames=[path.join("conf", f) for f in listdir(path.join("conf")) if f.endswith(".ini")],
    encoding="utf-8"
)
