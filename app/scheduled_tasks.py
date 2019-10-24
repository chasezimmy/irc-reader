import json
import time
from redis_client import redis_client
from .top_channels import top_channels
from . import join


def refresh_top_channels():
    print('refresh top channels')
    
    current_threads = set()
    for k, n in redis_client.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels()

    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)

    print('add: ', to_add)
    for channel in to_add:
        result = join.delay(channel)
        result.wait()

    print('remove: ', to_remove)
    for channel in to_remove:
        redis_client.hdel('channels', channel)


def join_channel():
    res = join.delay('moonmoon')
    res.wait()


def remove_5_min():
    spams = [json.loads(n.decode()) for n in redis_client.lrange('5_min', 0, -1)]
    print("Remove 5 minute old spam")
    expired_count = 0
    FIVE_MINUTES = 300

    for i, n in enumerate(spams):
        
        if time.time() - int(n['time']) >= FIVE_MINUTES:
            expired_count += 1
            redis_client.lset('5_min', i, '_______')
    print("REMOVED: ", expired_count)
    redis_client.lrem('5_min', expired_count, '_______')
