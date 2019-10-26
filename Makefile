run:
	python manage.py runserver

add_moonmoon:
	python manage.py test

tasks:
	ulimit -n 10000 && celery -A celery_worker.celery worker --loglevel=info --autoscale=1,100
	