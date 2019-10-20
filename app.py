import json
import requests
import threading
import redis
from top_channels.top_channels import top_channels
from flask import Flask, request
from irc.channel import Channel


app = Flask(__name__)
redis_connection = redis.Redis('localhost')
threads = {}


@app.route('/join/<channel>', methods=['GET'])
def join(channel):
    if channel not in threads or not threads[channel].is_alive():
        t = threading.Thread(target=Channel, args=(channel, redis_connection))
        threads[channel] = t
        threads[channel].start()
        redis_connection.hset('channels', channel, 1)
        return f'JOIN >> {channel}'
    return ''


@app.route('/part/<channel>', methods=['GET'])
def part(channel):
    redis_connection.hset('channels', channel, 0)
    return f'LEFT {channel}'


@app.route('/channels', methods=['GET'])
def channels():
    print("THREADS")
    print(threads)
    print("REDIS")
    print(redis_connection.hgetall('channels'))
    return ''


@app.route('/deleteall')
def delete_all():
    redis_connection.flushdb()
    return redis_connection.hgetall('channels')


@app.route('/top/<limit>')
def top(limit):
    for channel in top_channels(limit):
        requests.get(f'http://127.0.0.1:5000/join/{channel}')
    return ''


if __name__ == '__main__':
    app.run(debug=True)

