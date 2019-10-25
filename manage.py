from datetime import datetime
from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app
from app.scheduled_tasks import refresh_top_channels, join_channel, remove_5_min, remove_30_min
from redis_client import redis_client


app = create_app()
manager = Manager(app)

redis_client.delete('channels')
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_top_channels)
scheduler.add_job(refresh_top_channels, trigger='interval', minutes=5)

scheduler.add_job(remove_5_min)
scheduler.add_job(remove_5_min, trigger='interval', minutes=1)
scheduler.add_job(remove_30_min)
scheduler.add_job(remove_30_min, trigger='interval', minutes=31)
#scheduler.add_job(join_channel)
scheduler.start()



if __name__ == '__main__':
    manager.run()
