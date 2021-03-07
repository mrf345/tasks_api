service=docker-compose exec web

lint:
	$(service) black --check .
format:
	$(service) isort --profile black .
	$(service) black .
test:
	$(service) coverage run --source='.' manage.py test
	$(service) coverage report
manage:
	$(service) python manage.py $(x)
