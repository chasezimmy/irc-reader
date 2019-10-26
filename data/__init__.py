import json
import time
from collections import Counter
from flask import Blueprint, jsonify
from redis_client import redis_client


data_routes = Blueprint('data_routes', __name__)

@data_routes.route('/trending/<list>', methods=['GET'])
def trending(list):

    spams = [json.loads(n.decode())['spam'] for n in redis_client.lrange(list, 0, -1)]

    trending = {}

    for spam in spams:
        if spam not in trending:
            trending[spam] = 0

        trending[spam] += 1

    c = Counter(trending)
    counter = []
    for n in Counter(el for el in c.elements() if c[el] >= 15).most_common():
        counter.append(f'{n}')

    return jsonify(counter)


@data_routes.route('/trending/channel/<list>', methods=['GET'])
def trending_channel(list):

    spams = [json.loads(n.decode())['channel'] for n in redis_client.lrange(list, 0, -1)]

    trending = {}

    for spam in spams:
        if spam not in trending:
            trending[spam] = 0

        trending[spam] += 1

    return jsonify(trending)
