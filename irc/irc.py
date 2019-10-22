from flask import Blueprint
from cache import redis_connection


irc_routes = Blueprint('irc_routes', __name__)

@irc_routes.route('/part/<channel>', methods=['GET'])
def part(channel):
    redis_connection.hset('channels', channel, 0)
    return f'LEFT {channel}'


@irc_routes.route('/channels', methods=['GET'])
def channels():
    print("REDIS")
    print(redis_connection.hgetall('channels'))
    return ''


@irc_routes.route('/deleteall')
def delete_all():
    redis_connection.flushdb()
    return redis_connection.hgetall('channels')

