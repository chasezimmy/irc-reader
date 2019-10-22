from redis_client import redis_client
from .top_channels import top_channels
from . import join


def refresh_top_channels():
    print('refresh top channels')
    
    current_threads = set()
    for k, n in redis_client.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels(100)

    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)

    print('add: ', to_add)
    for channel in to_add:
        result = join.delay(channel)
        result.wait()

    print('remove: ', to_remove)
    for channel in to_remove:
        redis_client.hdel('channels', channel)
