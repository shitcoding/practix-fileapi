load_data:
	docker-compose exec django sh -c "cd /in_data/ && python3 load_data.py"
