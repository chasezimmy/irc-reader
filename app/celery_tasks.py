from app import celery
from redis_client import redis_client
from irc.irc_listener import IRCListener


@celery.task(name='join')
def join(channel):
    redis_client.hset('channels', channel, 1)
    IRCListener(channel, redis_client)
    return f'PARTING >> {channel}'
