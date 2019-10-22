from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app
from app.scheduled_tasks import refresh_top_channels
from redis_client import redis_client

app = create_app()
redis_client.delete('channels')
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_top_channels, trigger='interval', seconds=20)
scheduler.start()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
