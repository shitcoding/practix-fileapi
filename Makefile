load_data:
	docker-compose exec django sh -c "cd /in_data/ && python3 load_data.py"

install-pytest:
	. venv/bin/activate && pip install pytest

test-fastapi: install-pytest
	. venv/bin/activate && cd fastapi-solution && pytest