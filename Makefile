install:
	uv pip install -e .

collectstatic:
	uv run manage.py collectstatic --noinput

migrate:
	uv run manage.py migrate

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi
