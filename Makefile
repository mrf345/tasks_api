docker:=$(shell docker ps -q --no-trunc | grep $(shell docker-compose ps -q web))

ifdef docker
	service=docker-compose exec web
endif

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
