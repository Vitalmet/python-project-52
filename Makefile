.PHONY: install lint collectstatic migrate build render-start start

install:
	uv sync

lint:
	uv run ruff check task_manager/ hexlet_code/

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
