from flask import Blueprint
from redis_client import redis_client


irc_routes = Blueprint('irc_routes', __name__)

@irc_routes.route('/part/<channel>', methods=['GET'])
def part(channel):
    redis_client.hset('channels', channel, 0)
    return f'LEFT {channel}'


@irc_routes.route('/channels', methods=['GET'])
def channels():
    print("REDIS")
    print(redis_client.hgetall('channels'))
    return ''


@irc_routes.route('/deleteall')
def delete_all():
    redis_client.flushdb()
    return redis_client.hgetall('channels')

