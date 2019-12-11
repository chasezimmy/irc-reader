from flask import Flask
from celery import Celery
from celery.utils.log import get_task_logger
from config import Config
from redis_client import redis_client
from irc.routes import irc
from data.routes import data
from irc.irc_listener import IRCListener


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
logger = get_task_logger(__name__)

def create_app():

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    #app.config['DEBUG'] = True
    app.register_blueprint(irc)
    app.register_blueprint(data)
    app.config.from_object(Config)
    celery.conf.update(app.config)
    
    return app


@celery.task(name='join_channel')
def join_channel(channel):
    redis_client.hset('channels', channel, 1)
    IRCListener(channel, redis_client, logger)
    return f'PARTING >> {channel}'
