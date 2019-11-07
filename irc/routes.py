from flask import Blueprint, request, jsonify
from redis_client import redis_client


irc = Blueprint('irc', __name__)


@irc.route('/part/<channel>', methods=['GET'])
def part(channel):
    redis_client.hset('channels', channel, 0)
    return f'LEFT {channel}'


@irc.route('/channels', methods=['GET'])
def channels():
    print("REDIS - Channels")
    print(redis_client.hgetall('channels'))
    return ''


@irc.route('/deleteall')
def delete_all():
    redis_client.flushdb()
    return redis_client.hgetall('channels')


@irc.route('/shutdown')
def shutdown():
    redis_client.delete('channels')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({})
