#import sys
#sys.path.append("..")

from datetime import datetime
from cache import redis_connection
from top_channels import top_channels
from celery_tasks import join

def hello_world():
    print('Hello Job! The time is: %s' % datetime.now())


def refresh_top_channels():
    # Current alive threads
    
    current_threads = set()
    for k, n in redis_connection.hgetall('channels').items():
        if n.decode() == '1':
            current_threads.add(k.decode())

    top = top_channels(10)

    to_remove = current_threads.difference(top)
    to_add = top.difference(current_threads)

    redis_connection.hdel('channel', *list(to_remove))


    for channel in to_add:
        result = join.delay(channel)
        result.wait()