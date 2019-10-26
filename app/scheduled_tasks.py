import json
import time
from redis_client import redis_client
from .top_channels import top_channels
from . import join
from celery import group


def refresh_top_channels():
    print('refresh top channels')
    
    current_threads = set()
    for k, n in redis_client.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels(100)

    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)


    print('remove: ', to_remove)
    for channel in to_remove:
        redis_client.hdel('channels', channel)

    print('add: ', to_add)
    group([join.s(channel) for channel in to_add]).apply_async()
    


def join_channel():
    res = join.delay('moonmoon')
    res.wait()


def remove_5_min():
    spams = [json.loads(n.decode()) for n in redis_client.lrange('5_min', 0, -1)]
    expired_count = 0
    FIVE_MINUTES = 300

    for i, n in enumerate(spams):
        
        if time.time() - int(n['time']) >= FIVE_MINUTES:
            expired_count += 1
            redis_client.lset('5_min', i, '_______')
    print("REMOVED 5_min: ", expired_count)
    redis_client.lrem('5_min', expired_count, '_______')


def remove_30_min():
    spams = [json.loads(n.decode()) for n in redis_client.lrange('30_min', 0, -1)]
    expired_count = 0
    FIVE_MINUTES = 60*30

    for i, n in enumerate(spams):
        
        if time.time() - int(n['time']) >= FIVE_MINUTES:
            expired_count += 1
            redis_client.lset('30_min', i, '_______')
    print("REMOVED 30_min: ", expired_count)
    redis_client.lrem('30_min', expired_count, '_______')
