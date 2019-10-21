from flask import Flask
from celery import Celery
from config import Config


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():
    from irc.irc import irc_routes

    app = Flask(__name__)
    app.register_blueprint(irc_routes)
    app.config.from_object(Config)
    celery.conf.update(app.config)

    return app