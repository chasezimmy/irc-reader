import threading
from flask import current_app
from irc.irc_listener import IRCListener
from cache import redis_connection
from . import celery

threads = {}

@celery.task(name='join')
def join(channel):
    if channel not in threads or not threads[channel].is_alive():
        t = threading.Thread(target=IRCListener, args=(channel, redis_connection))
        threads[channel] = t
        threads[channel].start()
        redis_connection.hset('channels', channel, 1)
        return f'JOIN >> {channel}'