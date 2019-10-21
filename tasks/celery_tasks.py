import threading
from irc.channel import Channel
from cache import redis_connection
from tasks.celery_init import celery


threads = {}

@celery.task(name='join')
def join(channel):
    if channel not in threads or not threads[channel].is_alive():
        t = threading.Thread(target=Channel, args=(channel, redis_connection))
        threads[channel] = t
        threads[channel].start()
        redis_connection.hset('channels', channel, 1)
        return f'JOIN >> {channel}'
