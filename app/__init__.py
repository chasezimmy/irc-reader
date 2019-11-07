from flask import Flask
from celery import Celery
from config import Config
from redis_client import redis_client
from irc.routes import irc
from data.routes import data


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    #app.config['DEBUG'] = True
    app.register_blueprint(irc)
    app.register_blueprint(data)
    app.config.from_object(Config)
    celery.conf.update(app.config)
    
    return app
