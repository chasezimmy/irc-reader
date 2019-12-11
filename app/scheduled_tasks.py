import time
import json
from celery import group
from redis_client import redis_client
from app import join_channel
from .top_channels import top_channels


def refresh_top_channels():
    print('Refresh top channels')
    
    current_threads = set()
    for k, n in redis_client.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels()
    
    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)

    print('curr: ', redis_client.hgetall('channels').items())
    print('add: ', to_add)
    group([join_channel.s(channel) for channel in to_add]).apply_async()

    print('remove: ', to_remove)
    for channel in to_remove:
        redis_client.hdel('channels', channel)


def remove_expired(cache, expire_time):
    spams = [json.loads(n.decode()) for n in redis_client.lrange(cache, 0, -1)]
    expired_count = 0
    for i, n in enumerate(spams):
        if not n.get('time'):
            redis_client.lset(cache, i, '__deleted__')
        if time.time() - int(n.get('time', 0)) >= expire_time:
            expired_count += 1
            redis_client.lset(cache, i, '__deleted__')
    print(f'REMOVED {cache}: {expired_count}')
    redis_client.lrem(cache, expired_count, '__deleted__')
