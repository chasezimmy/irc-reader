run:
	python manage.py runserver

tasks:
	celery -A celery_worker.celery worker --loglevel=info
	