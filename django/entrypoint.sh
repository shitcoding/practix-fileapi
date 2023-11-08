#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123qwe \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true

gunicorn config.wsgi:application --bind 0.0.0.0:8000 -p 8000 --reload --log-level 'info'

exec "$@" 