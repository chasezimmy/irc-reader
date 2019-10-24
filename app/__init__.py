import threading
from flask import Flask, current_app
from celery import Celery
from config import Config
from redis_client import redis_client
from irc.irc import irc_routes
from irc.irc_listener import IRCListener
from data import data_routes

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
threads = {}

def create_app():

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    #app.config['DEBUG'] = True
    app.register_blueprint(irc_routes)
    app.register_blueprint(data_routes)
    app.config.from_object(Config)
    celery.conf.update(app.config)
    
    return app


@celery.task(name='join')
def join(channel):
    if channel not in threads or not threads[channel].is_alive():
        t = threading.Thread(target=IRCListener, args=(channel, redis_client))
        threads[channel] = t
        threads[channel].start()
        redis_client.hset('channels', channel, 1)
        return f'JOIN >> {channel}'
