install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn hexlet_code.wsgi

start:
	python manage.py runserver
