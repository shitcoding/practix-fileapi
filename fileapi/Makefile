FILEAPI_EXEC=docker compose exec fastapi-file sh -c

test:
	$(FILEAPI_EXEC) PYTHONPATH='.' pytest

# Export poetry dependencies to requirements.txt
requirements:
	poetry export --without-hashes -o requirements.txt

.PHONY: \
	test \
	requirements
