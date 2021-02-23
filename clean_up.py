# -*- coding: utf-8 -*-

from redis import Redis

from conf import conf


redis = Redis.from_url(conf['redis']['url'])


for key in redis.keys("*"):
    redis.delete(key)
    print(f"삭제 : {key.decode()}")
