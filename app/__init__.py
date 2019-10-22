from flask import Flask
from celery import Celery
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from irc.irc import irc_routes
from .scheduled_tasks import refresh_top_channels


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():

    app = Flask(__name__)
    #app.config['DEBUG'] = True
    app.register_blueprint(irc_routes)
    app.config.from_object(Config)
    celery.conf.update(app.config)
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_top_channels, trigger='interval', seconds=5)
    scheduler.start()

    return app
