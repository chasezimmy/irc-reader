run:
	python manage.py runserver

add_moonmoon:
	python manage.py test

tasks:
	celery -A celery_worker.celery worker --loglevel=info
	