import json
import time
from celery import group
from redis_client import redis_client
from . import join
from .top_channels import top_channels


def refresh_top_channels():
    print('Refresh top channels')
    
    current_threads = set()
    for k, n in redis_client.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels(100)

    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)

    print('add: ', to_add)
    group([join.s(channel) for channel in to_add]).apply_async()

    print('remove: ', to_remove)
    for channel in to_remove:
        redis_client.hdel('channels', channel)

    print('add: ', to_add)
    group([join.s(channel) for channel in to_add]).apply_async()
    


def remove_expired(cache, expire_time):
    spams = [json.loads(n.decode()) for n in redis_client.lrange(cache, 0, -1)]
    expired_count = 0
    for i, n in enumerate(spams):
        if time.time() - int(n.get('time', 0)) >= expire_time:
            expired_count += 1
            redis_client.lset('5_min', i, '__deleted__')
    print(f'REMOVED {cache}: {expired_count}')
    redis_client.lrem('5_min', expired_count, '__deleted__')
