from flask import Blueprint
from cache import redis_connection
from tasks.celery_tasks import join, threads
from irc.channel import Channel
from top_channels.top_channels import top_channels


irc_routes = Blueprint('irc_routes', __name__)

@irc_routes.route('/part/<channel>', methods=['GET'])
def part(channel):
    redis_connection.hset('channels', channel, 0)
    return f'LEFT {channel}'


@irc_routes.route('/channels', methods=['GET'])
def channels():
    print("THREADS")
    print(threads)
    print("REDIS")
    print(redis_connection.hgetall('channels'))
    return ''


@irc_routes.route('/deleteall')
def delete_all():
    redis_connection.flushdb()
    return redis_connection.hgetall('channels')


@irc_routes.route('/top/<limit>')
def top(limit):
    import ipdb; ipdb.set_trace()
    for channel in top_channels(limit):
        result = join.delay(channel)
        result.wait()
    return ''
