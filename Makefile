migrate:
	docker-compose exec api python manage.py migrate movies  0001 --fake 
	docker-compose exec api python manage.py collectstatic --no-input
	docker-compose exec api python manage.py migrate --no-input

create-admin:
	docker-compose exec api python manage.py createsuperuser --noinput --username admin --email ad@m.in || true

build:
	docker-compose up -d --build

load_data:
	docker cp ./sqlite_to_postgres/ project_api_1:/in_data/
	docker-compose exec api python3 /in_data/load_data.py

run:
	make build
	make migrate
	make create-admin