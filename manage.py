from datetime import datetime
from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app
from app.scheduled_tasks import refresh_top_channels, remove_expired
from redis_client import redis_client


app = create_app()
manager = Manager(app)

redis_client.delete('channels')
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_top_channels)
scheduler.add_job(refresh_top_channels, trigger='interval', minutes=5)

# Redis Cache
scheduler.add_job(remove_expired, args=('5_min', 60*5))
scheduler.add_job(remove_expired, trigger='interval', args=('5_min', 60*5), minutes=1)
scheduler.add_job(remove_expired, args=('30_min', 60*30))
scheduler.add_job(remove_expired, trigger='interval', args=('30_min', 60*30), minutes=5)
scheduler.add_job(remove_expired, args=('1_hour', 60*60))
scheduler.add_job(remove_expired, trigger='interval', args=('1_hour', 60*60), minutes=5)

scheduler.start()

if __name__ == '__main__':
    manager.run()
